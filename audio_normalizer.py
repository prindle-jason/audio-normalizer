#!/usr/bin/env python3
"""
Simple audio normalization script using ffmpeg-normalize.
Processes all audio files in source_dir (recursive) and outputs to output_dir (matching directory structure).
"""

from pathlib import Path
from ffmpeg_normalize import FFmpegNormalize
import sys

# File Configuration
SOURCE_DIR = "input"
OUTPUT_DIR = "output"
AUDIO_EXTENSIONS = {".mp3", ".ogg", ".wav"}

# Normalization Configuration
AUDIO_BITRATE = "192k"
TARGET_LUFS = -14.0
TRUE_PEAK = -1.5
LOUDNESS_RANGE_TARGET = 11.0
SAMPLE_RATE = 48000
PRINT_STATS = False

# Codec configuration mapping, shouldn't need modified unless you add new extensions
CODEC_CONFIG = {
    '.mp3': {'audio_codec': 'libmp3lame', 'audio_bitrate': AUDIO_BITRATE},
    '.ogg': {'audio_codec': 'libvorbis', 'audio_bitrate': AUDIO_BITRATE},
    '.wav': {'audio_codec': 'pcm_s16le'}
}

BASE_CONFIG = {
    'normalization_type': 'ebu',
    'dynamic': True,
    'target_level': TARGET_LUFS,
    'true_peak': TRUE_PEAK,
    'sample_rate': SAMPLE_RATE,
    'print_stats': PRINT_STATS,
    'progress': True
}

def create_normalizer(ext):
    """Create a normalizer with appropriate codec for the file type"""
    config = BASE_CONFIG.copy()
    config.update(CODEC_CONFIG.get(ext))        
    return FFmpegNormalize(**config)

def main():
    source_dir = Path(SOURCE_DIR)
    output_dir = Path(OUTPUT_DIR)
    
    # Check if source directory exists
    if not source_dir.exists():
        print(f"Source directory '{source_dir}' not found!")
        return 1
    
    # Find all audio files
    audio_files_by_ext = {}
    for ext in AUDIO_EXTENSIONS:
        audio_files_by_ext[ext] = list(source_dir.rglob(f"*{ext}"))

    files_count = sum(len(files) for files in audio_files_by_ext.values())
    if files_count == 0:
        print(f"No audio files found in '{source_dir}'")
        return 0

    print(f"Found {files_count} audio files")
    print(f"Target: {TARGET_LUFS} LUFS, {TRUE_PEAK} dBTP, LRA={LOUDNESS_RANGE_TARGET}, {SAMPLE_RATE}Hz")
    print()

    total_processed = total_skipped = 0
    
    for ext in audio_files_by_ext:
        ext_count = len(audio_files_by_ext[ext])
        
        if ext_count == 0:
            continue

        ext_processed = ext_skipped = 0

        normalizer = create_normalizer(ext)
        for i, audio_file in enumerate(audio_files_by_ext[ext], 1):
            # Calculate output path (preserve directory structure)
            relative_path = audio_file.relative_to(source_dir)
            output_file = output_dir / relative_path
            
            # Create output directory if needed
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Skip if output already exists
            if output_file.exists():
                print(f"[{i}/{ext_count}] SKIP: {relative_path} (already exists)")
                ext_skipped += 1
                continue

            print(f"[{i}/{ext_count}] ADD for Processing: {relative_path}")
            ext_processed += 1
            normalizer.add_media_file(str(audio_file), str(output_file))

        total_processed += ext_processed
        total_skipped += ext_skipped
        print(f"Processing {ext_processed} files with extension '{ext}'...")
        normalizer.run_normalization()
                
    # Summary
    print()
    print("=" * 50)
    print(f" SUMMARY:")
    print(f"    Processed: {total_processed}")
    print(f"    Skipped:   {total_skipped}")
    print(f"    Output:    {output_dir}")
    print("=" * 50)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())