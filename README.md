# Meeting Summarizer

## Install requirements

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ brew install ollama
```

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
$ python main.py --transcript transcript.txt
```

## Language
Use `--lang cn` for Chinese otherwise default is English
```
$ python main.py --video videoname.mp4 --lang cn
```
