#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data structure to represent responses received from the MaryTTS server"""

import collections

PROPERTIES = [
    'content',
    'headers',
    'ok',
    'reason',
    'status'
]

class MaryTTSResponse(collections.namedtuple('MaryTTSResponse', PROPERTIES)):
    """Representation of a response from the MaryTTS server"""
