# Meeting Summarizer

## Install requirements

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ brew install ollama
```

## Download Vosk Library

### For English
This is the language library this speech to text uses. Download this [Here](https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip)

### For Chinese
Download this [Here](https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip)

Once downloaded unzip in your project directory.

## Summarize a meeting
Before using please make sure ollama is running.

Video must be `.mp4` or `.mov`

```
$ python main.py --video videoname.mp4
```

Audio must be `.wav`

```
$ python main.py --audio audioname.wav
```

## If you already have a transcript
Save it to transcript.txt and run
```
$ python llama.py
```

## Language
Use `--lang cn` for Chinese otherwise default is English
```
$ python main.py --video videoname.mp4 --lang cn
```
