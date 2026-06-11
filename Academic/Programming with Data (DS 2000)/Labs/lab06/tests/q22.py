OK_FORMAT = True

test = {
  'name': 'q22',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> 100 <= one_hundred_rolls() <= 600
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
