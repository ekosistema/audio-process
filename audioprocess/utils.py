"""
Audio Process Tool
------------------
Utility functions for audio processing.

Author: CeleroLab
License: MIT
"""

import subprocess

def get_audio_duration(file_path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)
