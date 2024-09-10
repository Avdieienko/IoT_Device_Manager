#!/bin/bash

# Function to install ffmpeg on Ubuntu/Debian
install_ffmpeg_ubuntu() {
  echo "Installing ffmpeg on Ubuntu/Debian..."
  sudo apt update
  sudo apt install -y ffmpeg
}

# Function to install ffmpeg on Windows using Winget
install_ffmpeg_windows() {
  echo "Installing ffmpeg on Windows using wget..."

  # Check if the script is running with admin rights using PowerShell
  is_admin=$(powershell -Command "([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)")

  if [ "$is_admin" != "True" ]; then
    echo "Error: This script must be run as Administrator."
    echo "Please run the script in an elevated PowerShell session."
    exit 1
  fi

  # Install ffmpeg using Winget
  winget install "FFmpeg (Essentials Build)"

  echo "Installation complete. Restart your terminal, camera-app(if started from vscode terminal - restart vs code) and try again."
}

# Function to install ffmpeg on macOS using Homebrew
install_ffmpeg_macos() {
  echo "Installing ffmpeg on macOS using Homebrew..."
  if ! command -v brew &> /dev/null; then
    echo "Error: Homebrew is not installed. Please install Homebrew first."
    exit 1
  fi
  brew install ffmpeg
}

# Detect operating system and install ffmpeg accordingly
install_ffmpeg() {
  OS="$(uname)"
  
  if [ "$OS" = "Linux" ]; then
    # Check if the system is Ubuntu/Debian-based (for simplicity)
    if [ -f /etc/debian_version ]; then
      install_ffmpeg_ubuntu
    else
      echo "This script only supports Ubuntu/Debian-based systems for Linux."
      exit 1
    fi
  elif [ "$OS" = "Darwin" ]; then
    install_ffmpeg_macos
  elif echo "$OS" | grep -q "MINGW64_NT"; then
    install_ffmpeg_windows
  else
    echo "Unsupported operating system: $OS"
    exit 1
  fi
}

# Function to check if ffmpeg is installed
check_ffmpeg() {
  if ! ffmpeg -version >/dev/null 2>&1; then
    echo "Ffmpeg is not installed."
    install_ffmpeg
  else
    echo "Ffmpeg is already installed."
    ffmpeg -version
    exit 0
  fi
}

# Check if ffmpeg is installed
check_ffmpeg