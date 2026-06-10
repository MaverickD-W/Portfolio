OK_FORMAT = True
test = {
  'name': 'q42',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> type(cumulative_sum_answer) == int
          True
          """,
          'hidden': False,
          'locked': False
        },
        {       
          'code': r"""
          >>> cumulative_sum_answer
          2
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
