OK_FORMAT = True

test = {
  'name': 'q16',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Number of columns of the resulting table should be 3;
          >>> best_restaurant 
          'Mikes Taco Club'
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
