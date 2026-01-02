"""
Audio Process Tool
------------------
CLI interface for the audioprocess package.

Author: CeleroLab
License: MIT
"""

import os
from .processing import shuffle_audio, auto_fade, auto_loop, add_silence

def get_int_input(prompt, default=0):
    while True:
        try:
            user_input = input(prompt)
            if user_input.strip() == '':
                return default
            return int(user_input)
        except ValueError:
            print("Please enter a valid integer.")

def get_float_input(prompt, default=0.0):
    while True:
        try:
            user_input = input(prompt)
            if user_input.strip() == '':
                return default
            return float(user_input)
        except ValueError:
            print("Please enter a valid number.")

def main_menu():
    try:
        while True:
            print("\nAudio Processing Menu")
            print("1. Shuffle Audio")
            print("2. Auto Fade")
            print("3. Auto Loop")
            print("4. Add Silence")
            print("5. Exit")
            
            try:
                choice = input("Enter your choice (1-5): ")
            except EOFError:
                # Handle EOF (Ctrl+Z/D) as exit
                print("\nExiting...")
                break
            
            if choice == '1':
                input_folder = input("Enter input folder path (press Enter for current folder): ") or os.getcwd()
                min_dur = get_int_input("Enter minimum duration in seconds (default: 0): ", 0)
                max_dur = get_int_input("Enter maximum duration to trim (optional, press Enter to skip): ", 0)
                num_chunks = get_int_input("Enter number of chunks to split (default: 8): ", 8)
                
                shuffle_audio(input_folder, min_duration=min_dur, max_duration=max_dur, num_chunks=num_chunks)
                
            elif choice == '2':
                input_folder = input("Enter input folder path (press Enter for current folder): ") or os.getcwd()
                max_dur = get_int_input("Enter maximum duration in seconds (optional, press Enter to skip): ", 0)
                fade_dur = get_int_input("Enter fade duration in seconds (default: 1): ", 1)
                
                auto_fade(input_folder, max_duration=max_dur, fade_duration=fade_dur)
                
            elif choice == '3':
                input_folder = input("Enter input folder path (press Enter for current folder): ") or os.getcwd()
                min_dur = get_float_input("Enter minimum duration in seconds (default: 0): ", 0)
                max_dur = get_float_input("Enter maximum duration in seconds (optional, press Enter to skip): ", 0)
                iters = get_int_input("Enter number of iterations (default: 4): ", 4)
                fade_dur = get_float_input("Enter fade duration in seconds (default: 1): ", 1)
                
                auto_loop(input_folder, min_duration=min_dur, max_duration=max_dur, iterations=iters, fade_duration=fade_dur)
                
            elif choice == '4':
                input_folder = input("Enter input folder path (press Enter for current folder): ") or os.getcwd()
                sil_dur = get_int_input("Enter silence duration in seconds: ")
                pos = input("Enter silence position (a: before, d: after, b: both): ").lower()
                
                if pos not in ['a', 'd', 'b']:
                    print("Invalid position. Please enter 'a', 'd', or 'b'.")
                    continue
                
                add_silence(input_folder, silence_duration=sil_dur, position=pos)
                
            elif choice == '5':
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    except KeyboardInterrupt:
        print("\n\nProgram terminated by user. Goodbye!")
