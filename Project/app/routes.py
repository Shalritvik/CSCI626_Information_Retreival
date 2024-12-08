from flask import Blueprint, render_template, request, jsonify, send_from_directory
import os
from .search_engine import PodcastSearchEngine
from .data_processing import load_transcripts, create_corpus

# Blueprint setup
bp = Blueprint("routes", __name__)

# Paths for data
folder_path = "Transcripts"  # Path to the folder containing JSON transcripts
mp3_folder =  r"D:\Shal_PG\NYIT\CSCI626_info_retreival\Project\Podcast_MP3"  #mention absolute paths
# Path to the MP3 files

# Initialize the search engine
transcripts = load_transcripts(folder_path)
corpus, metadata = create_corpus(transcripts)
search_engine = PodcastSearchEngine(corpus, metadata)

@bp.route("/")
def index():
    """Render the main search page."""
    return render_template("index.html")

@bp.route("/search", methods=["POST"])
@bp.route("/search", methods=["POST"])
def search():
    """Handle search queries and return results."""
    query = request.form.get("query")
    top_n = int(request.form.get("top_n", 30))

    if query:
        results = search_engine.search(query, top_n)
        
        # Filter out results with similarity score of 0
        relevant_results = [result for result in results if result["score"] > 0]

        if not relevant_results:  # No results found
            return jsonify({"message": "No relevant results found."})

        return jsonify(relevant_results)
    return jsonify({"error": "Empty query"})


from urllib.parse import unquote

@bp.route("/play", methods=["GET"])
def play():
    file_name = request.args.get("file")
    file_name = unquote(file_name)  # Decode URL-encoded characters
    if not file_name:
        return jsonify({"error": "File parameter is missing"}), 400

    file_path = os.path.abspath(os.path.join(mp3_folder, file_name))
    print(f"Looking for file at: {file_path}")

    if not os.path.exists(file_path):
        return jsonify({"error": f"File '{file_name}' not found in {mp3_folder}"}), 404

    return send_from_directory(mp3_folder, file_name)
import json
@bp.route("/transcription", methods=["GET"])
def get_transcription():
    file_name = request.args.get("file")
    transcription_path = os.path.join(r"D:\Shal_PG\NYIT\CSCI626_info_retreival\Project\Transcripts", f"{os.path.splitext(file_name)[0]}.json") #Mention absolute paths

    if not os.path.exists(transcription_path):
        return jsonify({"error": "Transcription not found"}), 404

    with open(transcription_path, "r") as f:
        transcription = json.load(f)

    return jsonify(transcription)

