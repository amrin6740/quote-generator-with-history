window.onload = function () {
    loadHistory();
};

async function generateQuote() {

    try {

        const response = await fetch("/get_quote");
        const data = await response.json();

        document.getElementById("quote").innerHTML = `"${data.quote}"`;
        document.getElementById("author").innerHTML = `— ${data.author}`;

        loadHistory();

    } catch (error) {

        console.error("Error fetching quote:", error);

        document.getElementById("quote").innerHTML =
            "Unable to fetch a quote. Please try again.";

        document.getElementById("author").innerHTML = "";

    }

}

async function loadHistory() {

    try {

        const response = await fetch("/history");
        const history = await response.json();

        const historyList = document.getElementById("historyList");

        historyList.innerHTML = "";

        history.forEach(item => {

            historyList.innerHTML += `
                <div class="history-item">
                    <p>"${item.quote}"</p>
                    <span>— ${item.author}</span>
                </div>
            `;

        });

    } catch (error) {

        console.error("Error loading history:", error);

    }

}