# Lightweight Web Radio

A lightweight Flask-based web radio server that can host multiple radio stations, each playing music from different directories.

## Features

- Host multiple radio stations from a single server
- Each radio station has its own URL path and playlist
- Supports MP3, WAV, and OGG audio formats
- Simple web interface showing currently playing track
- Configure radio stations using a CSV file
- Automatic playlist management and continuous playback

## Requirements

- Python 3.6+
- Flask
- Pygame

## Configuration

Create a CSV file (e.g., `radios.csv`) with your radio configurations, with the following format:

```
name,path,url_prefix
Radio 1,music/radio1,radio1
Radio 2,music/radio2,radio2
```

Fields:
- `name`: Display name of the radio station
- `path`: Full path to the directory containing music files
- `url_prefix`: URL path where the radio will be accessible

## Usage

1. Create your `radios.csv` file with radio configurations
2. Run the server:
   ```bash
   python src/main.py radios.csv
   ```
3. Access your radio stations at:
   - http://localhost:5000/rock
   - http://localhost:5000/jazz
   - http://localhost:5000/classical
   (URLs depend on your configured url_prefixes)

## Project Structure

```
lightweight-web-radio/
├── src/
│   ├── __init__.py
│   ├── main.py          # Entry point and CSV parsing
│   └── web_radio.py     # Core radio functionality
├── requirements.txt     # Project dependencies
├── radios.csv          # Radio configurations
└── README.md
```

## Development

To enable debug mode, set `DEBUG = True` in `src/web_radio.py`.

## Supported Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- OGG (.ogg)

Make sure you have the necessary audio codecs installed on your system for pygame to play these formats.

## Notes

- The server runs on localhost (127.0.0.1) by default
- Each radio station automatically loops through its playlist
- New audio files are detected when the playlist refreshes
- The web interface updates the currently playing track in real-time