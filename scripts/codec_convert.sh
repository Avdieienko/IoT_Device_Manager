#!/bin/bash

# Function to check if ffmpeg is installed
check_ffmpeg() {
    if ! command -v ffmpeg &> /dev/null; then
        echo "Error: ffmpeg is not installed."
        exit 1
    fi
}

# Function to convert mp4v to h264
convert_video() {
    input_file="$1"
    output_file="$2"

    # Check if input file exists
    if [ ! -f "$input_file" ]; then
        echo "Error: Input file '$input_file' does not exist."
        exit 1
    fi

    # Perform the conversion
    echo "Converting $input_file to $output_file using H.264 codec..."
    ffmpeg -i "$input_file" -c:v libx264 -c:a copy "$output_file"

    # Check if the conversion was successful
    if [ $? -eq 0 ]; then
        echo "Conversion successful! Output file: $output_file"
    else
        echo "Error during conversion."
    fi
}

# Main script starts here
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_file> <output_file>"
    exit 1
fi

# Check if ffmpeg is installed
check_ffmpeg

# Convert the video
convert_video "$1" "$2"
