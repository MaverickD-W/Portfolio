OK_FORMAT = True

test = {
  'name': 'q22',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> shorter_than_five == 73761
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> between_five_and_nine == 41019
          True
          """,
          'hidden': False,
          'locked': False
        },
           {
          'code': r"""
          >>> between_ten_and_fourteen == 6794
          True
          """,
          'hidden': False,
          'locked': False
        },
           {
          'code': r"""
          >>> longer_than_fourteen == 219
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
