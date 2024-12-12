document.getElementById("searchForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const query = document.getElementById("query").value;
    const topN = document.getElementById("topN").value;

    const response = await fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `query=${encodeURIComponent(query)}&top_n=${encodeURIComponent(topN)}`,
    });

    const results = await response.json();

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (results.message) {
        resultsDiv.innerHTML = `<p class="text-warning">${results.message}</p>`;
    } else if (results.error) {
        resultsDiv.innerHTML = `<p class="text-danger">${results.error}</p>`;
    } else {
        results.forEach((result, index) => {
            const div = document.createElement("div");
            div.className = "result";
            div.innerHTML = `
                <h5 class="text-green">Title ${result.file}</h5>
              
                <p><strong>Start:</strong> ${result.start}s | <strong>End:</strong> ${result.end}s</p>
                <p><strong>Snippet:</strong> ${result.text}</p>
                <p><strong>Relevance Score:</strong> ${result.score.toFixed(4)}</p>
                <button class="btn btn-green play-button" 
                        data-file="${result.file}" 
                        data-start="${result.start}">
                    Play
                </button>
            `;
            resultsDiv.appendChild(div);
        });

        // Add event listeners to Play buttons for each result
        document.querySelectorAll(".play-button").forEach((button) => {
            button.addEventListener("click", async (event) => {
                const file = button.getAttribute("data-file");
                const start = button.getAttribute("data-start");

                const audioPlayer = document.getElementById("audioPlayer");
                const audioSource = document.getElementById("audioSource");
                const transcriptionContainer = document.getElementById("transcription");
                const mp3PlayerDiv = document.getElementById("mp3-player");

                // Fetch transcription for the selected file
                const transcriptionResponse = await fetch(`/transcription?file=${encodeURIComponent(file)}`);
                const transcription = await transcriptionResponse.json();

                // Populate the transcription container
                transcriptionContainer.innerHTML = "";
                transcription.forEach((segment, index) => {
                    const li = document.createElement("li");
                    li.className = "transcription-segment";
                    li.dataset.start = segment.start;
                    li.dataset.end = segment.end;
                    li.innerText = segment.text;
                    transcriptionContainer.appendChild(li);
                });

                // Set the source of the audio player
                audioSource.src = `/play?file=${encodeURIComponent(file)}`;
                mp3PlayerDiv.style.display = "block";

                // Load the audio and set the start time
                audioPlayer.load();
                audioPlayer.currentTime = parseFloat(start);
                audioPlayer.play();

                // Highlight transcription during playback and scroll to the active line
                audioPlayer.addEventListener("timeupdate", () => {
                    const currentTime = audioPlayer.currentTime;
                    document.querySelectorAll(".transcription-segment").forEach((segment) => {
                        const start = parseFloat(segment.dataset.start);
                        const end = parseFloat(segment.dataset.end);

                        if (currentTime >= start && currentTime <= end) {
                            segment.style.backgroundColor = "#00d67d";
                            segment.style.color = "#000";

                            // Scroll the active segment into view
                            segment.scrollIntoView({ behavior: "smooth", block: "center" });
                        } else {
                            segment.style.backgroundColor = "transparent";
                            segment.style.color = "#ddd";
                        }
                    });
                });
            });
        });

        // MP3 Player Controls
        const audioPlayer = document.getElementById("audioPlayer");

        document.getElementById("playButton").addEventListener("click", () => {
            audioPlayer.play();
        });

        document.getElementById("pauseButton").addEventListener("click", () => {
            audioPlayer.pause();
        });

        document.getElementById("stopButton").addEventListener("click", () => {
            audioPlayer.pause();
            audioPlayer.currentTime = 0; // Reset to the beginning
        });
    }
});
