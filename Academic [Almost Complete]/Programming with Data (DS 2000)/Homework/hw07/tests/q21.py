OK_FORMAT = True
test = {
  'name': 'q21',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # The array should have length 2;
          >>> len(deck_model_probabilities) == 2
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # The elements in the array should add up to 1.;
          >>> sum(deck_model_probabilities) == 1
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> deck_model_probabilities.item(0) == 4/13
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> deck_model_probabilities.item(1) == 9/13
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
