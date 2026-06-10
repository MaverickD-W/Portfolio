OK_FORMAT = True
test = {
  'name': 'q13',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> with_commas
          'Eats, Shoots, and Leaves'
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> without_commas
          'Eats Shoots and Leaves'
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
