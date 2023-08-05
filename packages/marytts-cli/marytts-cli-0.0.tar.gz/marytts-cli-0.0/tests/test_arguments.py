import unittest

import argparse
import marytts_cli.arguments

CLI_ARGUMENTS = [
    '--audio',
    '--input',
    '--locale',
    '--output',
    '--url',
    '--voice',
]
class TestArgs(unittest.TestCase):

    def test_arguments(self):
        argparser = marytts_cli.arguments.setup_argparser()
        self.assertEqual(type(argparser), argparse.ArgumentParser)
        for argument in CLI_ARGUMENTS:
            args = argparser.parse_args([argument, 'test'])
            argument_value = getattr(args, argument[2:])
            self.assertEqual(argument_value, 'test')

    def test_param_audio(self):
        pass

    def test_param_input_type(self):
        pass

    def test_param_locale(self):
        pass

    def test_param_output_type(self):
        pass

    def test_param_url(self):
        pass

    def test_param_voice(self):
        pass

if __name__ == '__main__':
    unittest.main()
