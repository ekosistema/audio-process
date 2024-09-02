import os
import random
import subprocess
from pydub import AudioSegment
from tqdm import tqdm

def get_audio_duration(file_path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

def shuffle_audio(args):
    input_folder = args["input_folder"]
    min_duration = args["min_duration"]
    max_duration = args["max_duration"]
    num_chunks = args["num_chunks"]

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

def auto_fade(args):
    input_folder = args["input_folder"]
    max_duration = args["max_duration"]
    fade_duration = args["fade_duration"]

    temp_folder = "./.temp"
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
    
    print("Auto-fading completed successfully!")

def auto_loop(args):
    input_folder = args["input_folder"]
    min_duration = args["min_duration"]
    max_duration = args["max_duration"]
    iterations = args["iterations"]
    fade_duration = args["fade_duration"]

    output_folder = os.path.join(input_folder, 'looped')
    os.makedirs(output_folder, exist_ok=True)
    
    audio_files = [f for f in os.listdir(input_folder) if f.endswith(('.mp3', '.wav', '.ogg', '.flac'))]
    
    for audio_file in tqdm(audio_files, desc="Looping Files"):
        input_path = os.path.join(input_folder, audio_file)
        output_path = os.path.join(output_folder, f"looped_{audio_file}")
        
        duration = get_audio_duration(input_path)
        
        if duration < min_duration:
            print(f"Skipping {audio_file} (duration less than minimum)")
            continue
        
        if max_duration and duration > max_duration:
            print(f"Trimming {audio_file} to {max_duration} seconds")
            temp_path = os.path.join(output_folder, f"temp_{audio_file}")
            fade_out = min(1, max_duration / 8)
            subprocess.run(['ffmpeg', '-i', input_path, '-t', str(max_duration), '-af', f'afade=t=out:st={max_duration-fade_out}:d={fade_out}', temp_path])
            input_path = temp_path
        
        concat_list = "|".join([input_path] * iterations)
        subprocess.run(['ffmpeg', '-i', f"concat:{concat_list}", '-af', f'afade=t=in:st=0:d={fade_duration},afade=t=out:st={iterations*duration-fade_duration}:d={fade_duration}', output_path])
        
        if 'temp_' in input_path:
            os.remove(input_path)
    
    print("Auto-looping completed successfully!")

def main_menu():
    while True:
        print("\nAudio Processing Menu")
        print("1. Shuffle Audio")
        print("2. Auto Fade")
        print("3. Auto Loop")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            args = {
                "input_folder": input("Enter input folder path: "),
                "min_duration": int(input("Enter minimum duration in seconds (default: 0): ") or 0),
                "max_duration": int(input("Enter maximum duration to trim (optional, press Enter to skip): ") or 0),
                "num_chunks": int(input("Enter number of chunks to split (default: 8): ") or 8)
            }
            shuffle_audio(args)
        elif choice == '2':
            args = {
                "input_folder": input("Enter input folder path: "),
                "max_duration": int(input("Enter maximum duration in seconds (optional, press Enter to skip): ") or 0),
                "fade_duration": int(input("Enter fade duration in seconds (default: 1): ") or 1)
            }
            auto_fade(args)
        elif choice == '3':
            args = {
                "input_folder": input("Enter input folder path: "),
                "min_duration": float(input("Enter minimum duration in seconds (default: 0): ") or 0),
                "max_duration": float(input("Enter maximum duration in seconds (optional, press Enter to skip): ") or 0),
                "iterations": int(input("Enter number of iterations (default: 4): ") or 4),
                "fade_duration": float(input("Enter fade duration in seconds (default: 1): ") or 1)
            }
            auto_loop(args)
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
