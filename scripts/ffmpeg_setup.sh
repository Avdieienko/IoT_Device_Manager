#!/bin/bash

# Function to install ffmpeg on Ubuntu/Debian
install_ffmpeg_ubuntu() {
  echo "Installing ffmpeg on Ubuntu/Debian..."
  sudo apt update
  sudo apt install -y ffmpeg
}

# Function to install ffmpeg on Windows using Chocolatey
install_ffmpeg_windows() {
  echo "Installing ffmpeg on Windows using Chocolatey..."

  # Check if the script is running with admin rights using PowerShell
  is_admin=$(powershell -Command "([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)")

  if [ "$is_admin" != "True" ]; then
    echo "Error: This script must be run as Administrator."
    echo "Please run the script in an elevated PowerShell session."
    exit 1
  fi

  # Check if Chocolatey is installed
  if ! command -v choco &> /dev/null; then
    echo "Error: Chocolatey is not installed. Please install Chocolatey first."
    echo "You can install Chocolatey by following instructions at https://chocolatey.org/install"
    exit 1
  fi

  # Install ffmpeg using Chocolatey
  choco install ffmpeg -y
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

# Function to check if ffmpeg is installed
check_ffmpeg_installed() {
  if command -v ffmpeg &> /dev/null; then
    echo "ffmpeg is already installed."
    ffmpeg -version
    exit 0
  fi
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
  if ! command -v ffmpeg &> /dev/null; then
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