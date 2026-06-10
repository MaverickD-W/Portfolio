OK_FORMAT = True

test = {   'name': 'q11',
    'points': 1,
    'suites': [   {   'cases': [   {'code': '>>> job_titles.num_columns\n2', 'hidden': False, 'locked': False},
                                   {'code': '>>> job_titles.num_rows\n6', 'hidden': False, 'locked': False},
                                   {   'code': '>>> # Make sure that you have the correct column labels!\n>>> np.asarray(job_titles.labels).item(1) != "Job full_array"\nTrue',
                                       'hidden': False,
                                       'locked': False},
                                   {'code': '>>> # Make sure that you have the correct column labels!\n>>> np.asarray(job_titles.labels).item(1) == "Jobs"\nTrue', 'hidden': False, 'locked': False}],
                      'scored': True,
                      'setup': '',
                      'teardown': '',
                      'type': 'doctest'}]}
