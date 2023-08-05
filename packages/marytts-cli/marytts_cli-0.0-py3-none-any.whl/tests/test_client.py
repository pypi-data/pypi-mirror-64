import unittest

import marytts_cli.client

class TestArgs(unittest.TestCase):

    def test_client(self):
        client = marytts_cli.client.MaryTTSClient()

if __name__ == '__main__':
    unittest.main()
