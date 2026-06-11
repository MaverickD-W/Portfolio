OK_FORMAT = True

test = {
  'name': 'q35',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> num_ceos_more_than_30_million == 5
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
