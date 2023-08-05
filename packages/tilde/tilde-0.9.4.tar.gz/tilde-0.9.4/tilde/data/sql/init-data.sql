
-- hierarchy_groups (GUI)

INSERT INTO hierarchy_groups (hgroup_id, name, landing_group, settings_group) VALUES (1, 'physical properties', 1, 1);
INSERT INTO hierarchy_groups (hgroup_id, name, landing_group, settings_group) VALUES (2, 'atomic structure', 1, 1);
INSERT INTO hierarchy_groups (hgroup_id, name, landing_group, settings_group) VALUES (3, 'modeling method', 1, 1);
INSERT INTO hierarchy_groups (hgroup_id, name, landing_group, settings_group) VALUES (4, 'modeling precision', 0, 1);
INSERT INTO hierarchy_groups (hgroup_id, name, landing_group, settings_group) VALUES (5, 'modeling package', 1, 1);
INSERT INTO hierarchy_groups (hgroup_id, name, landing_group, settings_group) VALUES (6, 'other metadata', 0, 1);
INSERT INTO hierarchy_groups (hgroup_id, name, landing_group, settings_group) VALUES (7, 'journal articles', 0, 1);
INSERT INTO hierarchy_groups (hgroup_id, name, landing_group, settings_group) VALUES (9, 'all the rest', 0, 0);

-- hierarchy (core) terms, enter hierarchy groups (as one-to-one)

INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1, 'chemical formula', 'standard', '', '', '',                                                                                 2, 0, 0, 1, 1, 0, 1, 1, 0, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (2, 'elements', 'elements', '', '', '',                                                                                         1, 1, 0, 1, 0, 1, 1, 0, 0, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (3, 'compound', 'nelem', '', '', '',                                                                                           30, 0, 0, 1, 1, 1, 1, 0, 1, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (4, 'formula units', 'expanded', '', '', '',                                                                                   40, 0, 0, 0, 0, 0, 0, 0, 1, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1501, 'lattice a', 'lata', '', 'Lattice a, &#8491;', '',                                                                       4, 0, 0, 0, 1, 0, 0, 0, 1, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1502, 'lattice b', 'latb', '', 'Lattice b, &#8491;', '',                                                                       5, 0, 0, 0, 1, 0, 0, 0, 1, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1503, 'lattice c', 'latc', '', 'Lattice c, &#8491;', '',                                                                       6, 0, 0, 0, 1, 0, 0, 0, 1, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1504, 'lattice alpha', 'latalpha', '', '', '',                                                                                7, 0, 0, 0, 1, 0, 0, 0, 1, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1505, 'lattice beta', 'latbeta', '', '', '',                                                                                   8, 0, 0, 0, 1, 0, 0, 0, 1, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1506, 'lattice gamma', 'latgamma', '', '', '',                                                                                 9, 0, 0, 0, 1, 0, 0, 0, 1, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1001, 'number of atoms', 'natom', '', 'N,,atoms__', '',                                                                       50, 0, 0, 1, 1, 0, 0, 0, 1, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (5, 'periodic boundary conditions', 'periodicity', '', '', '',                                                                130, 0, 0, 0, 0, 1, 1, 0, 0, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (9, 'crystal system', 'symmetry', '', '', '',                                                                                 140, 0, 0, 1, 1, 1, 1, 0, 0, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (10, 'point group', 'pg', 'Result point group', '', '',                                                                       150, 0, 0, 1, 1, 1, 1, 0, 0, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (11, 'space group (Sch.)', 'sg', 'Result space group (Schoenflis notation)', '', '',                                          160, 0, 0, 1, 1, 0, 1, 0, 0, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (12, 'space group (int)', 'ng', 'Result space group (international notation)', '', '',                                        170, 0, 0, 1, 1, 0, 0, 0, 0, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (13, 'layer group (int)', 'dg', 'Result layer group (international notation)', '', '',                                        180, 0, 1, 0, 0, 0, 0, 0, 0, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (50, 'space group', 'spg', 'Result space group (both international and Schoenflis notations)', '', '',                        181, 0, 0, 1, 1, 0, 1, 0, 0, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (8, 'system type', 'tags', '', '', '',                                                                                         60, 1, 1, 1, 0, 1, 1, 0, 0, 2);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (106, 'data type', 'dtype', '', '', '',                                                                                       269, 0, 0, 1, 0, 1, 1, 0, 0, 1);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (6, 'property', 'calctypes', '', '', '',                                                                                      270, 1, 0, 1, 0, 1, 1, 0, 0, 1);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (7, 'xc treatment', 'H', '', 'XC treatment', '',                                                                              190, 0, 1, 1, 1, 0, 1, 0, 0, 3);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (75, 'xc treatment', 'H_types', '', 'XC treatment type', '',                                                                  195, 1, 0, 0, 0, 1, 1, 0, 0, 3);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (15, 'spin-polarized', 'spin', '', '', '',                                                                                    210, 0, 0, 1, 1, 1, 1, 0, 0, 3);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (150, 'geometry optimization', 'optgeom', '', '', '',                                                                         209, 0, 0, 1, 1, 1, 1, 0, 0, 9);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (17, 'k-grid', 'k', '', '', '',                                                                                               220, 0, 1, 1, 1, 0, 1, 0, 1, 4);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (19, 'phonon magnitude', 'dfp_magnitude', '', '', '',                                                                         230, 0, 1, 0, 1, 0, 1, 0, 1, 4);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (20, 'phonon disp.number', 'dfp_disps', '', '', '',                                                                           240, 0, 1, 0, 1, 0, 0, 0, 1, 4);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (21, 'phonon k-grid', 'n_ph_k', '', '', '',                                                                                   250, 0, 1, 0, 1, 0, 0, 0, 1, 4);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (22, 'code family', 'framework', '', '', '',                                                                                  320, 0, 0, 1, 1, 1, 1, 0, 0, 5);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (23, 'code version', 'prog', '', '', '',                                                                                      330, 0, 0, 1, 1, 0, 0, 0, 0, 5);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (24, 'modeling time, hr', 'duration', '', '', '',                                                                             340, 0, 1, 1, 1, 0, 0, 0, 1, 5);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (25, 'parsing time, sc', 'perf', '', '', '',                                                                                  350, 0, 1, 1, 1, 0, 0, 0, 1, 5);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (26, 'conductivity', 'etype', '', '', '',                                                                                     280, 0, 0, 1, 1, 1, 1, 0, 0, 9);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (27, 'min.band gap', 'bandgap', '', 'Min.band gap{{units-energy}}', 'Electrons.gap',                                          290, 0, 0, 1, 1, 0, 0, 0, 1, 1);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (28, 'band gap type', 'bandgaptype', '', '', '',                                                                              300, 0, 0, 1, 0, 0, 1, 0, 0, 1);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (510, 'vacancy content', 'vac', '', '', '',                                                                                    70, 0, 0, 1, 0, 0, 1, 0, 1, 9);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (511, 'impurity', 'impurities', '', '', '',                                                                                    80, 1, 0, 1, 0, 0, 1, 1, 0, 9);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (520, 'planes number', 'layers', '', '', '',                                                                                   90, 0, 1, 1, 1, 0, 0, 0, 1, 9);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (521, 'adsorbent', 'adsorbent', '', '', '',                                                                                   100, 0, 1, 1, 1, 0, 0, 1, 0, 9);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (522, 'surface termination', 'termination', '', '', '',                                                                       110, 0, 1, 1, 1, 0, 0, 1, 0, 9);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (501, 'basis set', 'bs', '', '', '',                                                                                          260, 1, 1, 1, 0, 0, 0, 0, 0, 3);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (80, 'basis set', 'ansatz', '', '', '',                                                                                       185, 0, 0, 0, 1, 1, 1, 0, 0, 3);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1002, 'total energy', 'energy', '', 'E,,el.tot__/cell{{units-energy}}', '',                                                  310, 0, 0, 1, 1, 0, 0, 0, 1, 1);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1003, 'cell volume', 'dims', '', 'Cell, &#8491;^^3**', '',                                                                    10, 0, 0, 1, 1, 0, 0, 0, 1, 9);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1006, 'finished', 'finished', '', 'Finished?', '',                                                                           370, 0, 0, 1, 1, 0, 1, 0, 0, 5);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1005, 'source file', 'location', '', '', '',                                                                                 380, 0, 0, 0, 1, 0, 0, 0, 0, 6);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1701, 'authors', 'authors', '', '', '',                                                                                        1, 1, 1, 0, 1, 1, 1, 0, 0, 7);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1702, 'year', 'year', '', '', '',                                                                                              2, 0, 1, 0, 1, 1, 1, 0, 0, 7);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1703, 'article title', 'article_title', '', '', '',                                                                            3, 0, 1, 0, 1, 1, 1, 0, 0, 7);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1704, 'DOI', 'doi', '', '', '',                                                                                                4, 0, 1, 0, 1, 1, 1, 0, 0, 7);
INSERT INTO hierarchy (cid, name, source, legend, html, slider, sort, multiple, optional, has_summary_contrb, has_column, has_facet, has_topic, chem_formula, plottable, hgroup_id) VALUES
                      (1705, 'publication', 'pubdata', '', '', '',                                                                                    5, 0, 1, 0, 1, 1, 1, 0, 0, 7);

-- hierarchy values, make hierarchy per se

INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 0, 'unknown');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 1, 'unary');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 2, 'binary');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 3, 'ternary');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 4, 'quaternary');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 5, 'quinary');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 6, 'senary');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 7, 'septenary');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 8, 'octary');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 9, 'nonary');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 10, 'decenary');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 11, '11-ary');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 12, '12-ary');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 13, '13-ary');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 14, '14-ary');
INSERT INTO hierarchy_values (cid, num, name) VALUES (3, 15, '15-ary');

INSERT INTO hierarchy_values (cid, num, name) VALUES (5, 0, 'unknown');
INSERT INTO hierarchy_values (cid, num, name) VALUES (5, 1, '1d');
INSERT INTO hierarchy_values (cid, num, name) VALUES (5, 2, '2d');
INSERT INTO hierarchy_values (cid, num, name) VALUES (5, 3, '3d');
INSERT INTO hierarchy_values (cid, num, name) VALUES (5, 4, '0d');
INSERT INTO hierarchy_values (cid, num, name) VALUES (5, 5, 'isolated atom');

INSERT INTO hierarchy_values (cid, num, name) VALUES (6, 0, 'unknown properties');
INSERT INTO hierarchy_values (cid, num, name) VALUES (6, 1, 'total energy');
INSERT INTO hierarchy_values (cid, num, name) VALUES (6, 2, 'electron structure');
INSERT INTO hierarchy_values (cid, num, name) VALUES (6, 3, 'geometry optimization');
INSERT INTO hierarchy_values (cid, num, name) VALUES (6, 4, 'charges');
INSERT INTO hierarchy_values (cid, num, name) VALUES (6, 5, 'magnetic moments');
INSERT INTO hierarchy_values (cid, num, name) VALUES (6, 6, 'phonons');
INSERT INTO hierarchy_values (cid, num, name) VALUES (6, 7, 'phonon dispersion');
INSERT INTO hierarchy_values (cid, num, name) VALUES (6, 8, 'static dielectric constant');
INSERT INTO hierarchy_values (cid, num, name) VALUES (6, 9, 'elastic properties');

INSERT INTO hierarchy_values (cid, num, name) VALUES (8, 1, 'organic molecule');
INSERT INTO hierarchy_values (cid, num, name) VALUES (8, 2, 'vacancy defect');
INSERT INTO hierarchy_values (cid, num, name) VALUES (8, 3, 'adsorption');
INSERT INTO hierarchy_values (cid, num, name) VALUES (8, 4, 'perovskite');

INSERT INTO hierarchy_values (cid, num, name) VALUES (106, 0, 'ab initio calculation');
INSERT INTO hierarchy_values (cid, num, name) VALUES (106, 1, 'journal article');

INSERT INTO hierarchy_values (cid, num, name) VALUES (15, 0, 'unknown');
INSERT INTO hierarchy_values (cid, num, name) VALUES (15, 1, 'non-magnetic');
INSERT INTO hierarchy_values (cid, num, name) VALUES (15, 2, 'magnetic');

INSERT INTO hierarchy_values (cid, num, name) VALUES (22, 0, 'unknown code');
INSERT INTO hierarchy_values (cid, num, name) VALUES (22, 1, 'WIEN2K');
INSERT INTO hierarchy_values (cid, num, name) VALUES (22, 2, 'VASP');
INSERT INTO hierarchy_values (cid, num, name) VALUES (22, 3, 'CRYSTAL');
INSERT INTO hierarchy_values (cid, num, name) VALUES (22, 4, 'Quantum ESPRESSO');

INSERT INTO hierarchy_values (cid, num, name) VALUES (26, 0, 'unknown conductivity');
INSERT INTO hierarchy_values (cid, num, name) VALUES (26, 1, 'insulator');
INSERT INTO hierarchy_values (cid, num, name) VALUES (26, 2, 'conductor');

INSERT INTO hierarchy_values (cid, num, name) VALUES (28, 0, 'unknown band gap');
INSERT INTO hierarchy_values (cid, num, name) VALUES (28, 1, 'no band gap');
INSERT INTO hierarchy_values (cid, num, name) VALUES (28, 2, 'direct');
INSERT INTO hierarchy_values (cid, num, name) VALUES (28, 3, 'indirect');

INSERT INTO hierarchy_values (cid, num, name) VALUES (75, 0, 'unknown potential');
INSERT INTO hierarchy_values (cid, num, name) VALUES (75, 1, 'LDA');
INSERT INTO hierarchy_values (cid, num, name) VALUES (75, 2, 'GGA');
INSERT INTO hierarchy_values (cid, num, name) VALUES (75, 3, 'meta-GGA');
INSERT INTO hierarchy_values (cid, num, name) VALUES (75, 4, 'hybrid');
INSERT INTO hierarchy_values (cid, num, name) VALUES (75, 5, 'Hartree-Fock');
INSERT INTO hierarchy_values (cid, num, name) VALUES (75, 6, 'DFT+U');
INSERT INTO hierarchy_values (cid, num, name) VALUES (75, 7, 'vdW');
INSERT INTO hierarchy_values (cid, num, name) VALUES (75, 8, 'MP');
INSERT INTO hierarchy_values (cid, num, name) VALUES (75, 9, 'CC');
INSERT INTO hierarchy_values (cid, num, name) VALUES (75, 10, 'CI');
INSERT INTO hierarchy_values (cid, num, name) VALUES (75, 11, 'GW');

INSERT INTO hierarchy_values (cid, num, name) VALUES (80, 0, 'unknown basis set');
INSERT INTO hierarchy_values (cid, num, name) VALUES (80, 1, 'LAPW');
INSERT INTO hierarchy_values (cid, num, name) VALUES (80, 2, 'plane waves');
INSERT INTO hierarchy_values (cid, num, name) VALUES (80, 3, 'gaussians');
INSERT INTO hierarchy_values (cid, num, name) VALUES (80, 4, 'numeric AOs');

INSERT INTO hierarchy_values (cid, num, name) VALUES (1006, 0, 'unknown finalization');
INSERT INTO hierarchy_values (cid, num, name) VALUES (1006, 1, 'not finalized');
INSERT INTO hierarchy_values (cid, num, name) VALUES (1006, 2, 'finalized');
