OK_FORMAT = True
test = {
  'name': 'q34',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # It looks like you multiplied and subtracted in the wrong;
          >>> # order.;
          >>> sum(celsius_max_temperatures_rounded) != 356705.0
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> sum(celsius_max_temperatures_rounded)
          1280677.0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> len(celsius_max_temperatures_rounded)
          65000
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> celsius_max_temperatures_rounded.item(2003)
          20.0
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
