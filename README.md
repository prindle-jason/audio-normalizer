# Audio Normalizer

A simple dockerized Python script to normalize audio file loudness using broadcast standards.

## Features

- Batch processing of audio files
- Preserves directory structure
- Normalizes to -14 LUFS (broadcast standard)
- Supports MP3, WAV, OGG formats
- Docker-based - no local Python setup required

## Quick Start

1. **Clone this repository**
   ```bash
   git clone <repo-url>
   cd audio-normalizer
   ```

2. **Add your audio files to the `input/` folder**
   - Supports subdirectories
   - Formats: `.mp3`, `.wav`, `.ogg`

3. **Run the normalizer**
   
   **Windows:** Double-click `run.bat`
   
   **Linux/Mac:** Run `./run.sh`
   
   **Manual:** `docker-compose up --build`

4. **Find normalized files in `output/`**
   - Directory structure is preserved
   - Files already processed are skipped

## Settings

- **Target:** -14 LUFS (broadcast standard)
- **True Peak:** -1.5 dBTP  
- **Sample Rate:** 48kHz
- **MP3/OGG Bitrate:** 192k

## Requirements

- Docker and Docker Compose

## License

See LICENSE file for details.
