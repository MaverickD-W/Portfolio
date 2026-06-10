OK_FORMAT = True

test = {
  'name': 'q25',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> len(distances) == 10000
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
