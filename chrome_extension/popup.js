function apply(){

    document.getElementById("status").innerText = "⏳ Applying...";

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {

        let url = tabs[0].url;

        fetch("http://127.0.0.1:5000/apply-now-url", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({url: url})
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("status").innerText =
                "✅ Status: " + data.status;
        })
        .catch(err => {
            document.getElementById("status").innerText =
                "❌ Error connecting to SonuAI";
        });

    });
}