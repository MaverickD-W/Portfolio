OK_FORMAT = True

test = {
  'name': 'q12',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> my_small_data.num_rows == 44
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
