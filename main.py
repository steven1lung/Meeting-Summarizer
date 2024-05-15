import argparse
import logging
import os
import uuid

from vosk import Model, SetLogLevel

import llama
from sharetape import Sharetape


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video", type=str, required=False, default="")
    parser.add_argument("-a", "--audio", type=str, required=False, default="")
    parser.add_argument("-t", "--transcript", type=str, required=False, default="")
    parser.add_argument("-l", "--lang", type=str, required=False, default="en")
    args = parser.parse_args()

    if not (args.video or args.audio or args.transcript):
        parser.error("No action requested, add --video, --audio or --transcript")
    if args.transcript:
        with open(args.transcript, "r") as f:
            print(llama.summarize(f.read()))
            return
    elif args.video and args.audio:
        parser.error("Only select one action --video or --audio")

    SetLogLevel(-1)
    model = Model(
        model_path="vosk-model-small-cn-0.22"
        if args.lang == "cn"
        else "vosk-model-en-us-0.42-gigaspeech"
    )
    print("Extracting transcript from video")

    video_id = str(uuid.uuid4())
    os.makedirs(f"tmp/{video_id}")

    if args.audio != "":
        audio = args.audio
    else:
        audio = f"tmp/{video_id}/audio.wav"

    shartape = Sharetape(
        args.video,
        audio,
        f"tmp/{video_id}/mono_audio.wav",
        f"tmp/{video_id}/transcript.txt",
        f"tmp/{video_id}/words.json",
        f"tmp/{video_id}/captions.srt",
        model,
    )
    transcript = shartape.extract_transcript()
    print(llama.summarize(transcript))


if __name__ == "__main__":
    main()
