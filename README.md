# Audio Process Tool

## Table of Contents
1. Introduction
2. Installation
3. Usage
   3.1 Shuffle Audio
   3.2 Auto Fade
   3.3 Auto Loop
4. Troubleshooting
5. File Descriptions

## 1. Introduction

The Audio Process Tool is a versatile command-line application that allows you to perform various operations on audio files, including shuffling, fading, and looping. This manual will guide you through the installation process and explain how to use each feature of the tool.

## 2. Installation

To install the Audio Process Tool directly from GitHub, follow these steps:

1. Open a terminal.
2. Run the following command:
   ```
   bash <(curl -s https://raw.githubusercontent.com/ekosistema/audio-process/main/install.sh)
   ```
3. Follow the on-screen prompts to complete the installation.

The installer will:
- Check for Python 3 installation
- Create a virtual environment
- Install required Python packages
- Install system dependencies (ffmpeg)
- Download the main script
- Create a wrapper script
- Add the tool to your system PATH

After installation, restart your terminal or run `source ~/.bashrc` to apply the PATH changes.

## 3. Usage

To start the Audio Process Tool, open a terminal and type:

```
audio_process
```

You will be presented with a menu offering four options:

1. Shuffle Audio
2. Auto Fade
3. Auto Loop
4. Exit

### 3.1 Shuffle Audio

This option allows you to shuffle audio files by splitting them into chunks and randomly rearranging them.

When selected, you'll need to provide:
- Input folder path
- Minimum duration in seconds
- Maximum duration to trim (optional)
- Number of chunks to split the audio into (default: 8)

The shuffled audio files will be saved in a "shuffled" subfolder within the input folder.

### 3.2 Auto Fade

This option applies a fade-in and fade-out effect to your audio files.

When selected, you'll need to provide:
- Input folder path
- Maximum duration in seconds (optional)
- Fade duration in seconds

The processed audio files will be saved in a "faded" subfolder within the input folder.

### 3.3 Auto Loop

This option allows you to create looped versions of your audio files.

When selected, you'll need to provide:
- Input folder path
- Minimum duration in seconds
- Maximum duration in seconds (optional)
- Number of iterations (default: 4)
- Fade duration in seconds

The looped audio files will be saved in a "looped" subfolder within the input folder.

## 4. Troubleshooting

- If you encounter a "command not found" error when trying to run `audio_process`, make sure you've restarted your terminal or run `source ~/.bashrc` after installation.
- If you get errors related to missing dependencies, try running the installation command again.
- For issues with processing specific audio files, ensure that ffmpeg is correctly installed and that the files are in a supported format (.mp3, .wav, .ogg, or .flac).
- If you have problems with the installation script, make sure you have an active internet connection and that you can access GitHub.

## 5. File Descriptions

The Audio Process Tool consists of two main files:

1. `install.sh`: This bash script handles the installation of the tool, including setting up the environment and dependencies. It is hosted on GitHub and can be run directly using curl.

2. `audio_process.py`: This Python script contains the main functionality of the Audio Process Tool, including the shuffle_audio, auto_fade, and auto_loop functions, as well as the main menu interface. It is downloaded during the installation process.

These files work together to provide a seamless audio process experience. The installer script sets up everything needed to run the Python script, and the Python script handles the actual audio processing tasks.
