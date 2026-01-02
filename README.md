# 🎛️ Audio Process Tool ![v1.1.0](https://img.shields.io/badge/version-1.1.0-blue)

This project provides a modular set of Python utilities designed to simplify audio processing. Whether you are a musician, a developer, or a sound enthusiast, I hope this tool saves you valuable time by automating repetitive editing tasks. 🚀

The tool is designed to be flexible: it can be used directly from the command line for quick batch tasks or imported as a modern object-oriented library to integrate into your own Python applications.

---

## 📑 Table of Contents

1. [Overview](#1-overview-)
2. [Installation & Setup](#2-installation--setup-%EF%B8%8F)
3. [Library Usage (New)](#3-library-usage-new-%EF%B8%8F)
4. [Module Guide](#4-module-guide-%EF%B8%8F)
5. [CLI Usage](#5-cli-usage-)
6. [Troubleshooting](#6-troubleshooting-)
7. [Project Structure](#7-project-structure-)
8. [License](#8-license-)

---

## 1. Overview 🎧

**Audio Process Tool** is a robust solution for audio manipulation. It is designed to handle common tasks that would otherwise require manual editing.

Key capabilities include:
*   **Method Chaining**: Use the new `AudioTrack` class for a Fluent Interface (e.g., `track.trim().fade().export()`).
*   **Batch Processing**: Apply changes to entire folders of audio files (`.mp3`, `.wav`, `.flac`, `.ogg`).
*   **Automation**: Streamline tasks like fading, looping, or adding silence.
*   **Creative Tools**: Features like "Shuffle" allow for experimental sound design.
*   **Dual Mode**: Use it as a CLI (Command Line Interface) or a Python library.

---

## 2. Installation & Setup 🛠️

### Prerequisites

To ensure the tool runs correctly, please verify you have the following installed:

1.  **Python 3.10+**: The package utilizes modern Python features.
2.  **FFmpeg**: ⚠️ **Important**: This is the underlying engine used for audio processing. The tool will not function without it.

#### Installing FFmpeg
*   **Windows**: Download the executable from [ffmpeg.org](https://ffmpeg.org/), extract it, and add the `bin` folder to your system's **PATH**.
*   **macOS**: The easiest method is via Homebrew: `brew install ffmpeg`.
*   **Linux (Ubuntu/Debian)**: Run `sudo apt-get install ffmpeg`.

### Package Installation

You can install the package by cloning this repository:

```bash
git clone https://github.com/ekosistema/audio-process.git
cd audio-process
pip install .
```

For developers who wish to modify the source code:

```bash
pip install -e .
```

> **Note**: This project uses `pyproject.toml` for configuration. Pip will automatically handle the build process.

> **Note for Python 3.13+ Users**: If you are using a very recent version of Python, the standard `audioop` module may be missing. You may need to install the compatibility package:
> `pip install audioop-lts`

---

## 3. Library Usage (New) 🏗️

The library has been refactored to use a modern **Fluent Interface** pattern. You can now perform complex chains of operations on individual files with ease.

### The `AudioTrack` Class

```python
from audioprocess import AudioTrack, AudioProcessError

try:
    # process a single file
    (AudioTrack("guitar.wav")
        .trim(max_duration=15.0)       # Crop to 15 seconds
        .loop(iterations=2)            # Loop it twice
        .fade(duration=2.0)            # Fade in and out
        .add_silence(1.0, 'end')       # Add 1s silence at the end
        .export("guitar_processed.wav") # Save result
    )
    print("Processing complete!")

except AudioProcessError as e:
    print(f"An error occurred: {e}")
```

### Key Methods

*   **`load(path)`**: Load a new file into the track.
*   **`trim(max_duration)`**: Cut the audio if it exceeds the duration.
*   **`fade(duration, direction="both")`**: Apply fade in/out.
*   **`loop(iterations)`**: Repeat the audio.
*   **`add_silence(duration, position="start")`**: Insert silence ('start', 'end', 'both').
*   **`shuffle(num_chunks)`**: Randomize the audio segments.
*   **`save(path)`** / **`export(path, format)`**: Write the result to disk.

---

## 4. Module Guide 🎚️

Legacy batch processing functions are also available for processing entire folders at once. These now utilize the `AudioTrack` class internally.

### 🔀 Shuffle Audio (`shuffle_audio`)
*   **Description**: Divides an audio file into multiple segments ("chunks"), randomizes their order, and rejoins them with crossfades.
*   **Use Case**: Ideal for creative sound design, generating glitch textures, or creating variations of drum loops.

### 📉 Auto Fade (`auto_fade`)
*   **Description**: Applies a smooth Fade In and Fade Out to audio files. It can also trim files that exceed a specified maximum duration.
*   **Use Case**: Essential for cleaning up samples, preparing audio libraries, or ensuring smooth transitions.

### 🔁 Auto Loop (`auto_loop`)
*   **Description**: Repeats an audio file a specific number of times and exports it as a new, single file.
*   **Use Case**: Useful for extending short textures or creating longer rhythmic beds from one-shots.

### 🔇 Add Silence (`add_silence`)
*   **Description**: Inserts digital silence into the audio file.
*   **Use Case**: Helpful for separating tracks in a playlist, preparing samples for hardware that requires a lead-in, or standardized spacing.

---

## 5. CLI Usage 🚀

If you prefer an interactive experience, simply run the command in your terminal:

```bash
audioprocess
```
*(Or `python audio_process.py` if the package is not installed globally)*

You will be presented with a menu to select an operation and target folder.

---

## 6. Troubleshooting 🔧

If you encounter issues, please check the following common solutions:

**🔴 Error: `FileNotFoundError: [WinError 2] The system cannot find the file specified`**
*   **Cause**: This usually indicates that **FFmpeg** is not installed or not found in your system's PATH.
*   **Solution**: Please refer to the [Installation](#installation--setup-%EF%B8%8F) section to ensure FFmpeg is correctly configured. Verifying with `ffmpeg -version` in your terminal should return the version information.

**🔴 Error: `ModuleNotFoundError: No module named 'audioop'`**
*   **Cause**: This occurs on Python 3.13 or newer due to the removal of the module from the standard library.
*   **Solution**: Install the support package by running: `pip install audioop-lts`.

---

## 7. Project Structure 📂

*   `audioprocess/`: Contains the source code.
    *   `track.py`: **[NEW]** The core `AudioTrack` class with Fluent Interface.
    *   `exceptions.py`: **[NEW]** Custom error definitions.
    *   `processing.py`: Batch processing logic (refactored).
    *   `cli.py`: Handles the interactive command-line menu.
*   `pyproject.toml`: Modern configuration file for package installation (replacing `setup.py`).

---

## 8. License ✨

Developed by **CeleroLab**.
This project is open-source and licensed under the **MIT License**. You are free to use, modify, and distribute it.