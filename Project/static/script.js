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

    // Check if no results or a specific message is returned
    if (results.message) {
        resultsDiv.innerHTML = `<p class="text-warning">${results.message}</p>`;
    } else if (results.error) {
        resultsDiv.innerHTML = `<p class="text-danger">${results.error}</p>`;
    } else {
        // Display results if available
        results.forEach((result, index) => {
            const div = document.createElement("div");
            div.className = "result";
            div.innerHTML = `
                <h5 class="text-green">Result ${index + 1}</h5>
                <p><strong>File:</strong> ${result.file}</p>
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

        // Add event listeners to play buttons
        document.querySelectorAll(".play-button").forEach((button) => {
            button.addEventListener("click", (event) => {
                const file = button.getAttribute("data-file");
                const start = button.getAttribute("data-start");

                const audioPlayer = document.getElementById("audioPlayer");
                const audioSource = document.getElementById("audioSource");
                const mp3PlayerDiv = document.getElementById("mp3-player");

                // Set the source of the audio player
                audioSource.src = `/play?file=${encodeURIComponent(file)}`;
                mp3PlayerDiv.style.display = "block";

                // Load the audio and set the start time
                audioPlayer.load();
                audioPlayer.addEventListener("loadedmetadata", () => {
                    audioPlayer.currentTime = parseFloat(start);
                    audioPlayer.play();
                });
            });
        });
    }
});
