OK_FORMAT = True

test = {
  'name': 'q24',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> 1000 <= total_score <= 10000
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
