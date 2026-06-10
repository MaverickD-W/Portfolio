OK_FORMAT = True
test = {   'name': 'q61',
      'points': 1,
       'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> shortest
          43
          """,
          'hidden': False,
          'locked': False
        }, 
        {
          'code': r"""
          >>> longest
          96
          """,
          'hidden': False,
          'locked': False
        }, 
        {
          'code': r"""
          >>> np.isclose(average, 70.89705)
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
                