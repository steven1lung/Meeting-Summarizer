import argparse
import logging
import os
import uuid
import zipfile

import requests
from vosk import Model, SetLogLevel

import llama
from sharetape import Sharetape

CN_MODEL = "vosk-model-cn-0.22"
EN_MODEL = "vosk-model-en-us-0.42-gigaspeech"


def download_model(model_url, model_path):
    response = requests.get(model_url, stream=True)
    response.raise_for_status()
    with open(model_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    with zipfile.ZipFile(model_path, "r") as zip_ref:
        zip_ref.extractall(os.path.dirname(model_path))


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

    model_name = CN_MODEL if args.lang == "cn" else EN_MODEL
    if not os.path.exists(model_name):
        confirm = input(
            f"Model not found at {model_name}. Do you want to download it? (y/n): "
        )
        if confirm.lower() == "y":
            print("Downloading...")
            model_url = f"https://alphacephei.com/vosk/models/{model_name}.zip"
            download_model(model_url, model_name)
        else:
            print("Download cancelled.")
            return

    model = Model(model_name)
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
    try:
        print(llama.summarize(transcript))
    except Exception as e:
        print("Error summarizing transcript, please make sure you have ollama running")


if __name__ == "__main__":
    main()
