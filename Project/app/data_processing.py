import json
import os

def load_transcripts(folder_path):
    transcripts = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            with open(os.path.join(folder_path, file_name), "r") as f:
                segments = json.load(f)
                transcripts.append({"file": file_name, "segments": segments})
    return transcripts

def create_corpus(transcripts):
    corpus = []
    metadata = []
    for transcript in transcripts:
        for segment in transcript["segments"]:
            corpus.append(segment["text"])
            metadata.append({
                "file": transcript["file"],
                "start": segment["start"],
                "end": segment["end"]
            })
    return corpus, metadata
