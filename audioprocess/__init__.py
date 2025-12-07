"""
Audio Process Tool
------------------
A modular Python package for audio processing.

Author: CeleroLab
License: MIT
"""

__author__ = "CeleroLab"
__version__ = "0.1.0"
__license__ = "MIT"

from .utils import get_audio_duration
from .processing import shuffle_audio, auto_fade, auto_loop, add_silence
