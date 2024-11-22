import whisper
import json
import os

def transcribe_audio(file_path, output_file):
    print(f"Loading Whisper model...")
    model = whisper.load_model("medium")
    print(f"Model loaded. Starting transcription for {file_path}...")

    # Transcribe the audio file
    result = model.transcribe(file_path)
    print(f"Transcription completed for {file_path}.")

    # Extract and format the segments with timestamps
    segments = result.get("segments", [])
    formatted_transcription = [
        {
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"]
        }
        for segment in segments
    ]

    # Save the transcription with timestamps to a JSON file
    with open(output_file, "w") as f:
        json.dump(formatted_transcription, f, indent=4)

    print(f"Transcription saved to {output_file}")

def transcribe_all_mp3_in_folder(input_folder, output_folder):
    print(f"Checking input folder: {input_folder}...")
    if not os.path.exists(input_folder):
        print(f"Error: The input folder '{input_folder}' does not exist.")
        return

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    mp3_files = [f for f in os.listdir(input_folder) if f.endswith(".mp3")]
    if not mp3_files:
        print("No MP3 files found in the specified folder.")
        return

    for file_name in mp3_files:
        mp3_file_path = os.path.join(input_folder, file_name)
        output_file_name = f"{os.path.splitext(file_name)[0]}.json"
        output_file_path = os.path.join(output_folder, output_file_name)

        print(f"Transcribing {file_name}...")
        try:
            transcribe_audio(mp3_file_path, output_file_path)
        except Exception as e:
            print(f"An error occurred while transcribing {file_name}: {e}")

if __name__ == "__main__":
    # Specify the input folder containing the MP3 files
    input_folder_path = "MP3"  # Replace with your input folder path containing MP3 files

    # Specify the output folder where JSON files will be saved
    output_folder_path = "Transcripts"  # Replace with your desired output folder path

    # Transcribe all MP3 files in the specified folder
    transcribe_all_mp3_in_folder(input_folder_path, output_folder_path)
