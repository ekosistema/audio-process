"""
Audio Process Tool
------------------
A modular Python package for audio processing.

Author: CeleroLab
License: MIT
"""

import sys
import shutil
from pathlib import Path
from tqdm import tqdm
from .track import AudioTrack
from .exceptions import AudioProcessError

def shuffle_audio(input_folder, min_duration=0, max_duration=0, num_chunks=8):
    """
    Shuffle audio files in the input folder.

    Args:
        input_folder (str): Path to input folder.
        min_duration (float): Minimum duration to process.
        max_duration (float): Maximum duration to process (trim).
        num_chunks (int): Number of chunks for shuffling.
    """
    in_path = Path(input_folder or Path.cwd())
    out_path = in_path / "shuffled"
    out_path.mkdir(exist_ok=True)

    # Filter for audio files
    audio_files = [f for f in in_path.iterdir() if f.suffix.lower() in ('.mp3', '.wav', '.ogg', '.flac')]

    try:
        for file_path in tqdm(audio_files, desc="Shuffling Files"):
            try:
                track = AudioTrack(file_path)
                
                if track.duration < min_duration:
                    tqdm.write(f"Skipping {file_path.name} (duration: {track.duration:.2f}s < minimum: {min_duration}s)")
                    continue

                (track
                    .trim(max_duration)
                    .shuffle(num_chunks)
                    .save(out_path / f"shuffled_{file_path.name}")
                )

            except AudioProcessError as e:
                tqdm.write(f"Error processing {file_path.name}: {e}")
            except Exception as e:
                tqdm.write(f"Unexpected error on {file_path.name}: {e}")
                
        print("Audio shuffling completed successfully!")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user (Ctrl+C). Exiting...")
        return

def auto_fade(input_folder, max_duration=0, fade_duration=1):
    """
    Apply auto-fade to audio files.

    Args:
        input_folder (str): Path to input folder.
        max_duration (float): Maximum duration (trim).
        fade_duration (float): Duration of fade in/out.
    """
    in_path = Path(input_folder or Path.cwd())
    out_path = in_path / "faded"
    out_path.mkdir(exist_ok=True)

    audio_files = [f for f in in_path.iterdir() if f.suffix.lower() in ('.mp3', '.wav', '.ogg', '.flac')]

    try:
        for file_path in tqdm(audio_files, desc="Fading Files"):
            try:
                track = AudioTrack(file_path)
                
                (track
                    .trim(max_duration)
                    .fade(fade_duration, direction="both")
                    .save(out_path / f"faded_{file_path.name}")
                )
                
            except AudioProcessError as e:
                tqdm.write(f"Error processing {file_path.name}: {e}")
                
        print("Auto-fading completed successfully!")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user (Ctrl+C). Exiting...")
        return

def auto_loop(input_folder, min_duration=0, max_duration=0, iterations=4, fade_duration=1):
    """
    Loop audio files.

    Args:
        input_folder (str): Input folder path.
        min_duration (float): Minimum duration filter.
        max_duration (float): Max duration to trim before looping.
        iterations (int): Number of loops.
        fade_duration (float): Fade duration.
    """
    in_path = Path(input_folder or Path.cwd())
    out_path = in_path / 'looped'
    out_path.mkdir(exist_ok=True)
    
    audio_files = [f for f in in_path.iterdir() if f.suffix.lower() in ('.mp3', '.wav', '.ogg', '.flac')]
    
    try:
        for file_path in tqdm(audio_files, desc="Looping Files"):
            try:
                track = AudioTrack(file_path)

                if track.duration < min_duration:
                    tqdm.write(f"Skipping {file_path.name} (duration less than minimum)")
                    continue
                    
                (track
                    .trim(max_duration)
                    .loop(iterations)
                    .fade(fade_duration) 
                    .save(out_path / f"looped_{file_path.name}")
                )
                
            except AudioProcessError as e:
                tqdm.write(f"Error processing {file_path.name}: {e}")

        print("Auto-looping completed successfully!")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user (Ctrl+C). Exiting...")
        return

def add_silence(input_folder, silence_duration, position):
    """
    Add silence to audio files.

    Args:
        input_folder (str): Input folder path.
        silence_duration (float): Silence duration in seconds.
        position (str): 'a' (start), 'd' (end), 'b' (both).
    """
    in_path = Path(input_folder or Path.cwd())
    out_path = in_path / "silenced"
    out_path.mkdir(exist_ok=True)

    audio_files = [f for f in in_path.iterdir() if f.suffix.lower() in ('.mp3', '.wav', '.ogg', '.flac')]
    
    pos_map = {'a': 'start', 'd': 'end', 'b': 'both'}
    new_pos = pos_map.get(position, 'start')

    try:
        for file_path in tqdm(audio_files, desc="Adding Silence"):
            try:
                track = AudioTrack(file_path)
                
                (track
                    .add_silence(silence_duration, position=new_pos)
                    .save(out_path / f"silenced_{file_path.name}")
                )
                
            except AudioProcessError as e:
                tqdm.write(f"Error processing {file_path.name}: {e}")

        print("Silence addition completed successfully!")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user (Ctrl+C). Exiting...")
        return
