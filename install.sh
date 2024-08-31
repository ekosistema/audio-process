#!/bin/bash

set -e

echo "Audio Processor Tool Installer"
echo "==============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv audio_process_env
source audio_process_env/bin/activate

# Install required Python packages
echo "Installing required Python packages..."
pip install pydub tqdm

# Install system dependencies
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Installing system dependencies for Linux..."
    sudo apt-get update
    sudo apt-get install -y ffmpeg
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Installing system dependencies for macOS..."
    if ! command -v brew &> /dev/null; then
        echo "Homebrew is not installed. Please install Homebrew and try again."
        exit 1
    fi
    brew install ffmpeg
else
    echo "Unsupported operating system. Please install ffmpeg manually."
    exit 1
fi

# Download the main script from GitHub
echo "Downloading the main script from GitHub..."
curl -O https://raw.githubusercontent.com/ekosistema/audio-process/main/audio_process.py

# Make the script executable
chmod +x audio_process.py

# Create a wrapper script
echo "Creating a wrapper script..."
cat << EOF > audio_process
#!/bin/bash
source $(pwd)/audio_process_env/bin/activate
python3 $(pwd)/audio_process.py "\$@"
EOF

chmod +x audio_process

# Add the script to PATH
echo "Adding the script to PATH..."
mkdir -p ~/.local/bin
mv audio_process ~/.local/bin/

if ! grep -q "export PATH=\$PATH:~/.local/bin" ~/.bashrc; then
    echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
    echo "PATH has been updated. Please restart your terminal or run 'source ~/.bashrc' to apply changes."
fi

echo "Installation completed successfully!"
echo "You can now run the Audio Processor Tool by typing 'audio_process' in your terminal."
