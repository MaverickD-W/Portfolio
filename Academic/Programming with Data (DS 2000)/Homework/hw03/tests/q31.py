OK_FORMAT = True
test = {
  'name': 'q31',
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> np.isclose(bos_avg, 16.5025) 
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> np.isclose(manila_avg, 33.7432) 
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
