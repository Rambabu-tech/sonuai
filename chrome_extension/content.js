(function(){

    function addButton(){

        if(document.getElementById("sonuai-btn")) return;

        let btn = document.createElement("button");

        btn.id = "sonuai-btn";
        btn.innerText = "⚡ Auto Apply (SonuAI)";

        btn.style.position = "fixed";
        btn.style.bottom = "20px";
        btn.style.right = "20px";
        btn.style.zIndex = "9999";
        btn.style.padding = "10px";
        btn.style.background = "#22c55e";
        btn.style.color = "white";
        btn.style.border = "none";
        btn.style.cursor = "pointer";

        btn.onclick = function(){

            fetch("http://127.0.0.1:5000/apply-now-url", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({url: window.location.href})
            })
            .then(res => res.json())
            .then(data => {
                alert("Applied: " + data.status);
            })
            .catch(() => alert("Error connecting to SonuAI"));
        };

        document.body.appendChild(btn);
    }

    setTimeout(addButton, 3000);

})();