#!/bin/bash

# Generate RSA keys using OpenSSL
generateKeys () {
  openssl genrsa -out private.pem 2048
  echo "Private key generated."
  openssl rsa -pubout -in  private.pem -out public.pem
  echo "Public key generated."
}

# Check if openssl is already installed
echo "Check for OpenSSL installation..."
if command -v openssl > /dev/null 2>&1; then
  echo "OpenSSL is installed. Proceeding with generating keys..."
  generateKeys
  exit 0
fi

# Detect package manager and install OpenSSL
if [ -f /etc/debian_version ]; then
  echo "Detected Debian-based system (e.g., Ubuntu). Installing OpenSSL using apt..."
  sudo apt update
  sudo apt install -y openssl
elif [ -f /etc/redhat-release ]; then
  echo "Detected Red Hat-based system (e.g., CentOS, Fedora). Installing OpenSSL using yum/dnf..."
  if command -v dnf > /dev/null 2>&1; then
    sudo dnf install -y openssl
  else
    sudo yum install -y openssl
  fi
else
  echo "Unsupported Linux distribution. Please install OpenSSL manually before proceeding."
  exit 1
fi

# Verify installation
if command -v openssl > /dev/null 2>&1; then
  echo "OpenSSL installation was successful. Proceeding with generating keys..."
  generateKeys
else
  echo "OpenSSL installation failed. Please install OpenSSL manually before proceeding."
  exit 1
fi
