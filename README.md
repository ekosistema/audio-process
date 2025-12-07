# 🎛️ Audio Process Tool ![v1.0.0](https://img.shields.io/badge/version-1.0.0-blue)

This project provides a modular set of Python utilities designed to simplify batch audio processing. Whether you are a musician, a developer, or a sound enthusiast, we hope this tool saves you valuable time by automating repetitive editing tasks. 🚀

The tool is designed to be flexible: it can be used directly from the command line for quick tasks or imported as a library to integrate into your own Python applications.

---

## 📑 Table of Contents

1. [Overview](#1-overview-)
2. [Installation & Setup](#2-installation--setup-%EF%B8%8F)
3. [Module Guide](#3-module-guide-%EF%B8%8F)
4. [Usage](#4-usage-)
5. [Troubleshooting](#5-troubleshooting-)
6. [Project Structure](#6-project-structure-)
7. [License](#7-license-)

---

## 1. Overview 🎧

**Audio Process Tool** is a straightforward solution for batch audio manipulation. It is designed to handle common tasks that would otherwise require manual editing of multiple files.

Key capabilities include:
*   **Batch Processing**: Apply changes to entire folders of audio files (`.mp3`, `.wav`, `.flac`, `.ogg`).
*   **Automation**: Streamline tasks like fading, looping, or adding silence.
*   **Creative Tools**: Features like "Shuffle" allow for experimental sound design.
*   **Dual Mode**: Use it as a CLI (Command Line Interface) or a Python library.

---

## 2. Installation & Setup 🛠️

### Prerequisites

To ensure the tool runs correctly, please verify you have the following installed:

1.  **Python 3.6+**: The package is built using Python.
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

> **Note for Python 3.13+ Users**: If you are using a very recent version of Python, the standard `audioop` module may be missing. You may need to install the compatibility package:
> `pip install audioop-lts`

---

## 3. Module Guide 🎚️

Below is a detailed description of the available functions to help you understand how they affect your audio files.

### 🔀 Shuffle Audio (`shuffle_audio`)
*   **Description**: Divides an audio file into multiple segments ("chunks"), randomizes their order, and rejoins them with crossfades.
*   **Use Case**: Ideal for creative sound design, generating glitch textures, or creating variations of drum loops.
*   **Key Parameters**:
    *   `num_chunks`: The number of segments to divide the audio into.
    *   `min_duration`: Prevents processing files that are too short to be effectively split.

### 📉 Auto Fade (`auto_fade`)
*   **Description**: Applies a smooth Fade In and Fade Out to audio files. It can also trim files that exceed a specified maximum duration.
*   **Use Case**: Essential for cleaning up samples, preparing audio libraries, or ensuring smooth transitions.

### 🔁 Auto Loop (`auto_loop`)
*   **Description**: Repeats an audio file a specific number of times and exports it as a new, single file.
*   **Use Case**: Useful for extending short textures or creating longer rhythmic beds from one-shots.

### 🔇 Add Silence (`add_silence`)
*   **Description**: Inserts digital silence into the audio file.
*   **Options**:
    *   `'a'` (After): Adds silence at the end.
    *   `'d'` (During/Before): Adds silence at the beginning.
    *   `'b'` (Both): Adds silence at both the beginning and the end.
*   **Use Case**: Helpful for separating tracks in a playlist, preparing samples for hardware that requires a lead-in, or standardized spacing.

---

## 4. Usage 🚀

### Command Line Interface (CLI)

If you prefer an interactive experience, simply run the command in your terminal:

```bash
audioprocess
```
*(Or `python audio_process.py` if the package is not installed globally)*

You will be presented with a menu. Simply follow the on-screen prompts to select an operation and target folder.

### Python Library

You can import `audioprocess` into your own scripts to leverage its functionality programmatically:

```python
import audioprocess

# Example: Process a folder of recordings by adding 2 seconds of silence at the start
audioprocess.add_silence(
    input_folder="./my_recordings", 
    silence_duration=2, 
    position='d' # 'd' denotes 'during' or before
)

# Example: Shuffle drum samples for a creative effect
audioprocess.shuffle_audio(
    input_folder="./drums", 
    num_chunks=8
)
```

---

## 5. Troubleshooting 🔧

If you encounter issues, please check the following common solutions:

**🔴 Error: `FileNotFoundError: [WinError 2] The system cannot find the file specified`**
*   **Cause**: This usually indicates that **FFmpeg** is not installed or not found in your system's PATH.
*   **Solution**: Please refer to the [Installation](#installation--setup-%EF%B8%8F) section to ensure FFmpeg is correctly configured. Verifying with `ffmpeg -version` in your terminal should return the version information.

**🔴 Error: `ModuleNotFoundError: No module named 'audioop'`**
*   **Cause**: This occurs on Python 3.13 or newer due to the removal of the module from the standard library.
*   **Solution**: Install the support package by running: `pip install audioop-lts`.

**🔴 Permission Errors**
*   **Cause**: The script may not have permission to write to certain system folders.
*   **Solution**: Ensure you are running the script in a user-writable directory (like Documents or a project folder). On some systems, running as Administrator or using `sudo` may be required, though it is generally safer to change the working directory.

---

## 6. Project Structure 📂

*   `audioprocess/`: Contains the source code.
    *   `processing.py`: Core logic for audio manipulations.
    *   `cli.py`: Handles the interactive command-line menu.
*   `setup.py`: Configuration file for package installation.
*   `install.sh`: A helper script for Linux/macOS installation.

---

## 7. License ✨

Developed by **CeleroLab**.
This project is open-source and licensed under the **MIT License**. You are free to use, modify, and distribute it.