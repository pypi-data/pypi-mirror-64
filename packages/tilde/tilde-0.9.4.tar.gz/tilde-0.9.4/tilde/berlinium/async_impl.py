
# implementation of thread pool for asynchronous websocket connections
# with dynamically re-created DB sessions

import logging
import multiprocessing
from functools import partial

from concurrent.futures import ThreadPoolExecutor

from tornado import ioloop
from sockjs.tornado import SockJSConnection

import ujson as json

from tilde.berlinium.impl import GUIProviderMockup, Client
from tilde.core.settings import settings, connect_database


thread_pool = ThreadPoolExecutor(max_workers=4*multiprocessing.cpu_count())

class Connection(SockJSConnection):
    Type = 'asynchronous'
    Clients = {}
    GUIProvider = GUIProviderMockup

    def on_open(self, info):
        self.Clients[ getattr(self.session, 'session_id', self.session.__hash__()) ] = Client()
        logging.info("Server connected %s-th client" % len(self.Clients))

    def on_message(self, message):
        logging.debug("Server got: %s" % message)
        try:
            message = json.loads(message)
            message.get('act')
        except: return self.send(json.dumps({'act':'login', 'error':'Not a valid JSON!'}))

        frame = {
            'client_id': getattr(self.session, 'session_id', self.session.__hash__()),
            'act': message.get('act', 'unknown'),
            'req': message.get('req', ''),
            'error': '',
            'result': ''
        }

        # security check: a client must be authorized
        if not self.Clients[frame['client_id']].authorized and frame['act'] != 'login': return self.close()

        if not hasattr(self.GUIProvider, frame['act']):
            frame['error'] = 'No server handler for action: %s' % frame['act']
            return self.respond(frame)

        def worker(frame):
            db_session = connect_database(settings, default_actions=False, no_pooling=True)
            logging.debug("New DB connection to %s" % (
                settings['db']['default_sqlite_db']
                if settings['db']['engine'] == 'sqlite'
                else settings['db']['dbname'] + '@' + settings['db']['engine']
            ))

            frame['result'], frame['error'] = getattr(self.GUIProvider, frame['act'])( frame['req'], frame['client_id'], db_session )

            # must explicitly close db connection inside a thread
            db_session.close()
            del db_session
            logging.debug("DB connection closed")

            return frame

        def callback(res):
            return self.respond(res.result())

        thread_pool.submit( partial(worker, frame) ).add_done_callback(
            lambda future: ioloop.IOLoop.instance().add_callback(
                partial(callback, future)
            )
        )

    def respond(self, output):
        del output['client_id']
        if not output['error'] and not output['result']:
            output['error'] = "Handler %s has returned an empty result!" % output['act']

        logging.debug("Server responds: %s" % output)
        self.send(json.dumps(output))

    def on_close(self):
        logging.info("Server will close connection with %s-th client" % len(self.Clients))
        client_id = getattr(self.session, 'session_id', self.session.__hash__())
        del self.Clients[client_id]
