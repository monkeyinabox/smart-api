"""Model test functions. 

.. moduleauthor:: Mobile App Team
"""

import unittest
from api.errors import InvalidVertexException
from api.models import Token
from jsonschema.exceptions import ValidationError


class TokenTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_functions(self):
        """Tests the functionality of all token functions

        """
        token = Token()
        token.generate_token()
        self.assertTrue(isinstance(token.token, str))

        token2 = Token()
        token2.generate_token()
        self.assertNotEqual(token.token, token2.token)


if __name__ == '__main__':
    unittest.main()