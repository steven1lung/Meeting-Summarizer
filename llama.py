import ollama


def summarize(context: str):
    reponse = ollama.chat(
        "llama3",
        messages=[
            {
                "role": "system",
                "content": """
Below is a transcription of a meeting. Read the transcription carefully and provide a summary that includes:
1.Main topics discussed
2.Key decisions made
3.Action items assigned, including to whom and any deadlinesPlease make sure the summary is concise, coherent, and directly addresses the contents of the meeting. Exclude any extraneous information or casual conversation that does not contribute to the understanding of the meeting's outcomes.
4. Give me 3 quotes from the meeting
""",
            },
            {"role": "user", "content": f"<meeting_trans>{context}</meeting_trans>"},
        ],
        options={"temperature": 0.4},
    )

    return reponse["message"]["content"]


if __name__ == "__main__":
    with open("transcript.txt", "r") as f:
        transcipt = f.read()
    print(summarize(transcipt))
