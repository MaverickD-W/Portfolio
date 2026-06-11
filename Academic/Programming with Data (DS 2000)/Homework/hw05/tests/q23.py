OK_FORMAT = True

test = {
  'name': 'q23',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> top_ten.item(0) == 'Eric Mika'
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> top_ten.item(9) == 'Jonah Bolden'
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
