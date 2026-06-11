OK_FORMAT = True
test = {
  'name': 'q11',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> np.allclose(weird_numbers, np.array([-2.,  0.93203909,  1.73205081,  6.89864831]), rtol=1e-03, atol=1e-03)
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
