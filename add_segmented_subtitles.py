import argparse
import os
import subprocess
from openai import OpenAI


def read_srt(path: str) -> str:
    with open(path, 'r', encoding='utf-8-sig') as f:
        return f.read()


def segment_srt(text: str, api_key: str) -> str:
    client = OpenAI(api_key=api_key)
    system_prompt = (
        "You are a subtitle assistant."
        " Split subtitle lines into natural sentences while keeping the index and"
        " timestamps unchanged. The input is an SRT file with Chinese and English" 
        " lines. Return the complete new SRT text."
    )
    user_prompt = f"Here is the SRT content:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content


def burn_subtitles(video: str, srt: str, output: str) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        video,
        "-vf",
        f"subtitles={srt}",
        "-c:a",
        "copy",
        output,
    ]
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(description="Segment SRT with GPT-4o and burn to video")
    parser.add_argument("input_srt", help="Original SRT file")
    parser.add_argument("input_video", help="Input MP4 video")
    parser.add_argument("output_video", help="Output video with subtitles")
    parser.add_argument("--output_srt", default="segmented.srt", help="Intermediate segmented SRT")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY environment variable not set")

    srt_text = read_srt(args.input_srt)
    new_srt = segment_srt(srt_text, api_key)

    with open(args.output_srt, "w", encoding="utf-8") as f:
        f.write(new_srt)

    burn_subtitles(args.input_video, args.output_srt, args.output_video)


if __name__ == "__main__":
    main()
