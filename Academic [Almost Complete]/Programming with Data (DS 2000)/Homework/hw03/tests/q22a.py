OK_FORMAT = True
test = {
  'name': 'q22a',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> type(migration_rates) == tables.Table
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> migration_rates.select('REGION', 'NAME', '2015', '2016', 'BIRTHS', 'DEATHS', 'MIGRATION', 'OTHER', 'Migration-Rate').take(0)
          REGION | NAME    | 2015      | 2016      | BIRTHS | DEATHS | MIGRATION | OTHER | Migration-Rate
          3      | Alabama | 4,853,875 | 4,863,300 | 58,556 | 52,405 | 3,874     | -600  | 0.000798125

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
