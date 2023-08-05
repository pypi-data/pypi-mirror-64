#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Client for the MarryTTS Text-To-Speech System

This module contains the class representation of the client's interface.
"""

import urllib

import requests

from marytts_cli.response import MaryTTSResponse
from marytts_cli.defaults import (
    DEFAULT_AUDIO,
    DEFAULT_INPUT_TYPE,
    DEFAULT_LOCALE,
    DEFAULT_OUTPUT_TYPE,
    DEFAULT_QUERY_URL,
    DEFAULT_VOICE,
)

class MaryTTSClient():
    """Client interface for the MarryTTS Text-To-Speech System

    This class provides capabilities for connecting to the MaryTTS server via
    HTTP(S), making querries and returning the corresponding results.
    """

    def __init__(self, url=DEFAULT_QUERY_URL):
        """Initialize class variables"""
        self._url = urllib.parse.urlparse(url)
        self._input_type = DEFAULT_INPUT_TYPE
        self._output_type = DEFAULT_OUTPUT_TYPE
        self._audio = DEFAULT_AUDIO
        self._locale = DEFAULT_LOCALE
        self._voice = DEFAULT_VOICE

    def query(self, message):
        """Query MaryTTS server via HTTP(S)

        Sends a POST request to '/process' on the MaryTTS server and returns
        the corresponding result afterwards.
        """
        params = {
            'AUDIO': self.audio(),
            'INPUT_TEXT': message,
            'INPUT_TYPE': self.input_type(),
            'LOCALE': self.locale(),
            'OUTPUT_TYPE': self.output_type(),
            'VOICE': self.voice(),
        }
        response = requests.post(
            self.url().geturl(),
            headers=dict(),
            params=params,
        )
        return MaryTTSResponse(
            content=response.content,
            headers=response.headers,
            ok=response.ok,
            reason=response.reason,
            status=response.status_code,
        )

    def _xet(self, member_name, member_value=None):
        """Getter and Setter for class members

        Returns the value of a class member if member_value is None,
        otherwise sets and returns the value of the class member.
        """
        if member_value:
            setattr(self, member_name, member_value)
        member_value = getattr(self, member_name)
        return member_value

    def input_type(self, input_type=None):
        """Alias for _xet('_input_type', value)"""
        return self._xet('_input_type', input_type)

    def output_type(self, output_type=None):
        """Alias for _xet('_output_type', value)"""
        return self._xet('_output_type', output_type)

    def audio(self, audio=None):
        """Alias for _xet('_audio', value)"""
        return self._xet('_audio', audio)

    def locale(self, locale=None):
        """Alias for _xet('_locale', value)"""
        return self._xet('_locale', locale)

    def voice(self, voice=None):
        """Alias for _xet('_voice', value)"""
        return self._xet('_voice', voice)

    def url(self, url=None):
        """Alias for _xet('_url', value)"""
        return self._xet('_url', url)
