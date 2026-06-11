OK_FORMAT = True

test = {
  'name': 'q18',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> 21 <= burritos_less_than_6 <= 27
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> 40 <= burritos_between_6_and_7 <= 44
          True
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
