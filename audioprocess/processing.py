"""
Audio Process Tool
------------------
A modular Python package for audio processing.

Author: CeleroLab
License: MIT
"""

import os
import random
from pydub import AudioSegment
from tqdm import tqdm
from .utils import get_audio_duration

def shuffle_audio(input_folder, min_duration=0, max_duration=0, num_chunks=8):
    if input_folder is None:
         input_folder = os.getcwd()

    temp_folder = os.path.join(input_folder, ".temp")
    output_folder = os.path.join(input_folder, "shuffled")
    
    os.makedirs(temp_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    audio_files = [f for f in os.listdir(input_folder) if f.endswith(('.mp3', '.wav', '.ogg', '.flac'))]
    
    for file in tqdm(audio_files, desc="Shuffling Files"):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f"shuffled_{file}")
        
        duration = get_audio_duration(input_path)
        
        if duration < min_duration:
            print(f"Skipping {file} (duration: {duration}s < minimum: {min_duration}s)")
            continue
        
        audio = AudioSegment.from_file(input_path)
        
        if max_duration and duration > max_duration:
            audio = audio[:int(max_duration * 1000)]
        
        chunk_duration = len(audio) // num_chunks
        chunks = [audio[i*chunk_duration:(i+1)*chunk_duration] for i in range(num_chunks)]
        
        fade_duration = len(audio) // 20
        chunks = [chunk.fade_out(duration=fade_duration) for chunk in chunks]
        
        chunk_files = []
        for i, chunk in enumerate(chunks):
            chunk_path = os.path.join(temp_folder, f"chunk_{i}_{file}")
            chunk.export(chunk_path, format=file.split('.')[-1])
            chunk_files.append(chunk_path)
        
        random.shuffle(chunk_files)
        shuffled_audio = AudioSegment.empty()
        for chunk_file in chunk_files:
            shuffled_audio += AudioSegment.from_file(chunk_file)
        
        shuffled_audio = shuffled_audio.fade_in(50).fade_out(50)
        
        shuffled_audio.export(output_path, format=file.split('.')[-1])
        
        for chunk_file in chunk_files:
            os.remove(chunk_file)
    
    os.rmdir(temp_folder)
    print("Audio shuffling completed successfully!")

def auto_fade(input_folder, max_duration=0, fade_duration=1):
    if input_folder is None:
         input_folder = os.getcwd()

    temp_folder = os.path.join(input_folder, ".temp") 

    output_folder = os.path.join(input_folder, "faded")
    os.makedirs(temp_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    audio_files = [f for f in os.listdir(input_folder) if f.endswith(('.mp3', '.wav', '.ogg', '.flac'))]
    
    for file in tqdm(audio_files, desc="Fading Files"):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f"faded_{file}")
        
        audio = AudioSegment.from_file(input_path)
        
        if max_duration and len(audio) > max_duration * 1000:
            audio = audio[:int(max_duration * 1000)]
            fade_out_duration = int(len(audio) * 0.125)
            audio = audio.fade_out(fade_out_duration)
        
        audio = audio.fade_in(int(fade_duration * 1000)).fade_out(int(fade_duration * 1000))
        audio.export(output_path, format=file.split('.')[-1])
    
    try:
        os.rmdir(temp_folder)
    except OSError:
        pass # Directory might not be empty or not exist
        
    print("Auto-fading completed successfully!")

def auto_loop(input_folder, min_duration=0, max_duration=0, iterations=4, fade_duration=1):
    if input_folder is None:
         input_folder = os.getcwd()

    output_folder = os.path.join(input_folder, 'looped')
    os.makedirs(output_folder, exist_ok=True)
    
    audio_files = [f for f in os.listdir(input_folder) if f.endswith(('.mp3', '.wav', '.ogg', '.flac'))]
    
    for audio_file in tqdm(audio_files, desc="Looping Files"):
        input_path = os.path.join(input_folder, audio_file)
        output_path = os.path.join(output_folder, f"looped_{audio_file}")
        
        audio = AudioSegment.from_file(input_path)
        duration = len(audio) / 1000.0  # Convert to seconds
        
        if duration < min_duration:
            print(f"Skipping {audio_file} (duration less than minimum)")
            continue
        
        if max_duration and duration > max_duration:
            print(f"Trimming {audio_file} to {max_duration} seconds")
            audio = audio[:int(max_duration * 1000)]
        
        # Create the looped audio
        looped_audio = audio * iterations
        
        # Apply fade in and fade out
        fade_duration_ms = int(fade_duration * 1000)
        looped_audio = looped_audio.fade_in(fade_duration_ms).fade_out(fade_duration_ms)
        
        # Export the looped audio
        looped_audio.export(output_path, format=audio_file.split('.')[-1])
    
    print("Auto-looping completed successfully!")

def add_silence(input_folder, silence_duration, position):
    if input_folder is None:
         input_folder = os.getcwd()

    output_folder = os.path.join(input_folder, "silenced")
    os.makedirs(output_folder, exist_ok=True)

    audio_files = [f for f in os.listdir(input_folder) if f.endswith(('.mp3', '.wav', '.ogg', '.flac'))]
    
    for file in tqdm(audio_files, desc="Adding Silence"):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, f"silenced_{file}")
        
        audio = AudioSegment.from_file(input_path)
        silence = AudioSegment.silent(duration=silence_duration * 1000)  # Convert to milliseconds
        
        if position == 'a':
            modified_audio = silence + audio
        elif position == 'd':
            modified_audio = audio + silence
        elif position == 'b':
            modified_audio = silence + audio + silence
        else:
            modified_audio = audio
        
        modified_audio.export(output_path, format=file.split('.')[-1])
    
    print("Silence addition completed successfully!")
