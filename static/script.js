document.addEventListener("DOMContentLoaded", () => {
    const scanBtn = document.getElementById("scanBtn");
    const resetBtn = document.querySelector("button[type='reset']");
    const urlInput = document.getElementById("urlInput");
    const loader = document.getElementById("loader"); 

    scanBtn.addEventListener("click", function (e) {
        e.preventDefault();

        const url = urlInput.value;
        loader.style.display = "block"; 

        fetch("https://phishing-detector-8xam.onrender.com/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .then(data => {
            loader.style.display = "none"; 

            const resultPage = window.open('', '_blank');

            const html = `
                <html>
                <head>
                    <title>Scan Result</title>
                    <style>
                        body {
                            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            padding: 1px;
                            background-color: #f4f4f4;
                            color: #333;
                        }
                        .result-container {
                            background-color: #fff;
                            padding: 30px;
                            padding-left: 80px;
                            border-radius: 12px;
                            width: 50%;
                            box-shadow: 0 0 20px rgba(0,0,0,0.1);
                        }
                        h2 {
                            color: #2c7a2c;
                            text-align: center;
                            margin-bottom: 20px;
                        }
                        h3 {
                            margin-top: 30px;
                            color: #555;
                        }
                        ul.feature {
                            padding-left: 20px;
                            line-height: 1.6;
                        }
                        p {
                            margin: 8px 0;
                        }
                        .back-button {
                            background-color: #2c7a2c;
                            color: white;
                            text-decoration: none;
                            border-radius: 8px;
                            font-weight: bold;
                            margin-bottom: 30px;
                            margin-top: 100px;
                            padding: 10px;
                        }
                        .back-button:hover {
                            background-color: #256023;
                        }
                        .center {
                            display: flex;
                            justify-content: center;
                            margin-top: 5%;
                            width: 100%
                        }
                    </style>
                </head>
                <body>
                    <br><br>
                    <a href="index.html" class="back-button">← Back to Scan</a>
                    <div class="center">
                        <div class="result-container">
                            <h2>Phishing Detection Result</h2>
                            <p><strong>URL:</strong> ${data.url}</p>
                            <p><strong>Prediction:</strong> <span style="color: ${data.prediction === 'Legitimate' ? 'green' : 'red'}; font-weight: bold;">
                                ${data.prediction}
                            </span></p>
                            <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%</p>
                            <p><strong>Raw Prediction:</strong> ${data.raw_prediction}</p>
                            <p><strong>Timestamp:</strong> ${data.timestamp}</p>
                            <h3>Extracted Features:</h3>
                            <ul class="feature">
                                <li><strong>URL Length:</strong> ${data.features.url_length}</li>
                                <li><strong>Special Char Count:</strong> ${data.features.special_char_count}</li>
                                <li><strong>Uses HTTPS:</strong> ${data.features.uses_https}</li>
                                <li><strong>Domain Age (days):</strong> ${data.features.domain_age_days}</li>
                                <li><strong>DNS Resolves:</strong> ${data.features.dns_resolves}</li>
                                <li><strong>Has Suspicious Keywords:</strong> ${data.features.has_suspicious_keywords}</li>
                            </ul>
                        </div>
                    </div>
                </body>
                </html>
            `;

            resultPage.document.write(html);
            resultPage.document.close();
        })
        .catch(error => {
            loader.style.display = "none"; 
            console.error("Error:", error);
            alert("Something went wrong. Please try again.");
        });
    });

    resetBtn.addEventListener("click", function (e) {
        e.preventDefault();
        urlInput.value = "";
    });
});
