"""
Core AudioTrack class implementing the Fluent Interface pattern.
"""
from __future__ import annotations

import random
import pathlib
import shutil
from typing import Union, List, Optional
from pydub import AudioSegment  # type: ignore

from .exceptions import AudioProcessError

class AudioTrack:
    """
    A class representing an audio track with fluent interface for chaining operations.

    Attributes:
        audio (AudioSegment): The underlying pydub AudioSegment object.
        path (pathlib.Path | None): The path to the loaded audio file.
    """

    def __init__(self, path: Union[str, pathlib.Path, None] = None):
        """
        Initialize the AudioTrack.

        Args:
            path: Optional path to an audio file to load immediately.
        """
        self.audio: Optional[AudioSegment] = None
        self.path: Optional[pathlib.Path] = None
        
        if path:
            self.load(path)

    @classmethod
    def from_file(cls, path: Union[str, pathlib.Path]) -> 'AudioTrack':
        """
        Alternative constructor to create an AudioTrack from a file.
        
        Args:
            path: Path to the audio file.
            
        Returns:
            AudioTrack: A new instance with the loaded audio.
        """
        return cls(path)

    @property
    def duration(self) -> float:
        """
        Get the duration of the track in seconds.

        Returns:
            float: Duration in seconds.
        """
        if self.audio is None:
            return 0.0
        return len(self.audio) / 1000.0

    def load(self, path: Union[str, pathlib.Path]) -> 'AudioTrack':
        """
        Load an audio file.

        Args:
            path: Path to the audio file.

        Returns:
            self: For method chaining.

        Raises:
            AudioProcessError: If the file does not exist or cannot be loaded.
        """
        self.path = pathlib.Path(path)
        if not self.path.exists():
            raise AudioProcessError(f"File not found: {self.path}")

        try:
            self.audio = AudioSegment.from_file(str(self.path))
        except Exception as e:
            raise AudioProcessError(f"Failed to load audio file {self.path}: {e}")

        return self

    def trim(self, max_duration: float) -> 'AudioTrack':
        """
        Trim the audio to a maximum duration.

        Args:
            max_duration: Maximum duration in seconds.

        Returns:
            self: For method chaining.
        """
        if self.audio is None:
            raise AudioProcessError("No audio loaded.")

        if max_duration > 0 and self.duration > max_duration:
            self.audio = self.audio[:int(max_duration * 1000)]
        
        return self

    def fade(self, duration: float, direction: str = "both") -> 'AudioTrack':
        """
        Apply fade in and/or fade out.

        Args:
            duration: Fade duration in seconds.
            direction: 'in', 'out', or 'both'.

        Returns:
            self: For method chaining.
        """
        if self.audio is None:
            raise AudioProcessError("No audio loaded.")

        fade_ms = int(duration * 1000)
        
        if direction in ("in", "both"):
            self.audio = self.audio.fade_in(fade_ms)
        
        if direction in ("out", "both"):
            self.audio = self.audio.fade_out(fade_ms)
            
        return self

    def loop(self, iterations: int) -> 'AudioTrack':
        """
        Loop the audio a specified number of times.

        Args:
            iterations: Number of times to loop.

        Returns:
            self: For method chaining.
        """
        if self.audio is None:
            raise AudioProcessError("No audio loaded.")
            
        if iterations > 1:
            self.audio = self.audio * iterations
            
        return self

    def add_silence(self, duration: float, position: str = "start") -> 'AudioTrack':
        """
        Add silence to the track.

        Args:
            duration: Duration of silence in seconds.
            position: 'start', 'end', or 'both' (adds to both start and end).

        Returns:
            self: For method chaining.
        """
        if self.audio is None:
            raise AudioProcessError("No audio loaded.")

        silence = AudioSegment.silent(duration=int(duration * 1000))
        
        if position == 'start':
            self.audio = silence + self.audio
        elif position == 'end':
            self.audio = self.audio + silence
        elif position == 'both':
            self.audio = silence + self.audio + silence
            
        return self

    def shuffle(self, num_chunks: int = 8) -> 'AudioTrack':
        """
        Shuffle the audio by slicing it into chunks and reordering them.

        Args:
            num_chunks: Number of chunks to split the audio into.

        Returns:
            self: For method chaining.
        """
        if self.audio is None:
            raise AudioProcessError("No audio loaded.")

        if num_chunks <= 1:
            return self

        chunk_duration = len(self.audio) // num_chunks
        chunks = [self.audio[i*chunk_duration:(i+1)*chunk_duration] for i in range(num_chunks)]
        
        # Apply slight crossfade to chunks to avoid clicks
        fade_duration = len(self.audio) // (num_chunks * 20) # heuristic from legacy code
        chunks = [chunk.fade_out(duration=max(1, fade_duration)) for chunk in chunks]
        
        random.shuffle(chunks)
        
        shuffled_audio = AudioSegment.empty()
        for chunk in chunks:
            shuffled_audio += chunk
            
        self.audio = shuffled_audio
        # Smooth out the result
        self.audio = self.audio.fade_in(50).fade_out(50)
        
        return self

    def export(self, output_path: Union[str, pathlib.Path], format: str = "wav") -> 'AudioTrack':
        """
        Export the audio to a file.

        Args:
            output_path: Path to save the file.
            format: Audio format (e.g., 'wav', 'mp3').

        Returns:
            self: For method chaining.
        """
        if self.audio is None:
            raise AudioProcessError("No audio loaded.")

        out_path = pathlib.Path(output_path)
        
        # Ensure directory exists
        out_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            self.audio.export(str(out_path), format=format)
        except Exception as e:
            raise AudioProcessError(f"Failed to export audio to {out_path}: {e}")
            
        return self

    def save(self, output_path: Union[str, pathlib.Path]) -> 'AudioTrack':
        """
        Alias for export, inferring format from file extension if possible.

        Args:
            output_path: Path to save the file.

        Returns:
            self: For method chaining.
        """
        path_obj = pathlib.Path(output_path)
        fmt = path_obj.suffix.lstrip('.')
        if not fmt:
            fmt = "wav" # Default
            
        return self.export(output_path, format=fmt)
