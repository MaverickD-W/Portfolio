OK_FORMAT = True
test = {
  'name': 'q34',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> isinstance(strongest_earthquake_magnitude, float)
          True
          """,
          'hidden': False,
          'locked': False
        },
        {  
         'code': r"""
          >>> np.isclose(strongest_earthquake_magnitude, 8.0)
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
