#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Argument parsing of the MaryTTS command-line client

This module contains the setup function for the argument parser of the
command-line client.
"""

import argparse

def setup_argparser():
    """Setup argument parser"""
    parser = argparse.ArgumentParser(
        prog='marytts-cli',
        description=str(
            'A command-line client for the HTTP server '
            'of the MaryTTS Text-To-Speech System.',
        ),
    )
    parser.add_argument(
        '--audio',
        type=str,
        metavar='AUDIO',
        help='set format of MaryTTS audio output',
    )
    parser.add_argument(
        '--input',
        type=str,
        metavar='INPUT',
        help='set type of MaryTTS input',
    )
    parser.add_argument(
        '--locale',
        type=str,
        metavar='LOCALE',
        help='set identifier of Locale',
    )
    parser.add_argument(
        '--output',
        type=str,
        metavar='OUTPUT',
        help='set type of MaryTTS output',
    )
    parser.add_argument(
        '--url',
        type=str,
        metavar='URL',
        help='set request URL',
    )
    parser.add_argument(
        '--voice',
        type=str,
        metavar='VOICE',
        help='set name of MaryTTS voice',
    )
    return parser
