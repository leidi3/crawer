# Subtitle Segmentation Tool

This repository includes a helper script `add_segmented_subtitles.py` for segmenting SRT subtitle files with the OpenAI GPT‑4o model and burning them into an MP4 video using `ffmpeg`.

## Requirements

- Python 3.11+
- `openai>=1.0.0` (already listed in `weibo-crawler-master/requirements.txt`)
- `ffmpeg` installed and available in your `$PATH`

Install Python dependencies with:

```bash
pip install -r weibo-crawler-master/requirements.txt
```

## Usage

Set your OpenAI API key in the environment variable `OPENAI_API_KEY` and run:

```bash
python add_segmented_subtitles.py INPUT.srt INPUT.mp4 OUTPUT.mp4
```

An intermediate segmented SRT file will be saved as `segmented.srt` (or the path provided with `--output_srt`). The script first sends the original subtitles to GPT‑4o to split long lines into natural sentences. It then calls `ffmpeg` to overlay the resulting subtitles onto the video.
