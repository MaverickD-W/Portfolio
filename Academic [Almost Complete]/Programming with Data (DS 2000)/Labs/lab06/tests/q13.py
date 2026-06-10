OK_FORMAT = True

test = {
  'name': 'q13',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> my_large_data.num_rows == 100
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
