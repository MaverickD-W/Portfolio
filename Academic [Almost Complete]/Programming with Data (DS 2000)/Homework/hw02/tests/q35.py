OK_FORMAT = True
test = {
  'name': 'q35',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> round(sum(celsius_temperature_ranges))
          768487
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> len(celsius_temperature_ranges)
          65000
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> celsius_temperature_ranges.item(1)
          10.0
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
