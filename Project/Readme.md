# Podcast Explorer

## Overview
Podcast Explorer is a web-based tool that allows users to search for specific content within podcast episodes. The system utilizes transcript-based search capabilities and ranks query results using cosine similarity with TF-IDF embeddings. Users can search for content, view snippet results, and playback the relevant sections of the podcast.

## Features
- **Search Podcasts:** Enter a query to find matching podcast segments.
- **Snippet Retrieval:** Display relevant snippets from podcast transcripts with timestamps.
- **Audio Playback:** Play the specific segment of the podcast directly from the search results.
- **Query Highlighting:** Shows how many times the query appears in the podcast file.

## Requirements
- Python 3.8+
- Flask
- CUDA
- Scikit-learn
- Numpy
- HTML/CSS for the frontend

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/podcast-explorer.git
    cd podcast-explorer
    ```

2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Place your podcast transcript files (in JSON format) inside the `Transcripts` folder.

4. Start the Flask server:
    ```bash
    python run.py
    ```

5. Open a browser and navigate to `http://127.0.0.1:5000`.

## How to Use
1. Enter a query in the search bar on the homepage.
2. Click "Search" to fetch results.
3. View the ranked results with relevance scores, query count, and snippet previews.
4. Use the "Play" button to listen to the specific podcast segment.

## Project Structure
```
.
|-- Transcripts/        # Folder containing JSON transcript files
|-- static/
|   |-- styles.css      # Styling for the web interface
|   |-- script.js       # Frontend JavaScript logic
|-- templates/
|   |-- index.html      # HTML structure for the app
|-- app/
|   |-- search_engine.py  # Main search engine logic
|   |-- data_processing.py # Data loading and preprocessing logic
|-- run.py              # Entry point to start the Flask server
|-- requirements.txt    # List of dependencies
```

## Examples
Below are screenshots of the working application:

### 1. Search Page
![Search Page](https://github.com/Shalritvik/CSCI626_Information_Retreival/blob/main/Project/Home.png)

### 2. Search Results
![Search Results](https://github.com/user-attachments/assets/edc8c0f3-a0c8-4f12-b068-31adef420da4)


### 3. Audio Playback
![Result_playback](https://github.com/user-attachments/assets/bf3ad498-e488-4431-95e1-acab6eda8fd2)



## License
This project is licensed under the MIT License. You are free to use, modify, and distribute this project, provided that proper attribution is given.

## Contributing
1. Fork the repository.
2. Create a new branch for your feature:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes and push to the branch:
    ```bash
    git add .
    git commit -m "Add your message here"
    git push origin feature-name
    ```
4. Open a pull request.

## Contact
For any inquiries, feel free to contact shalritvik.work@gmail.com.

