document.getElementById("predict-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const data = {
        pclass: document.getElementById("pclass").value,
        sex: document.getElementById("sex").value,
        age: document.getElementById("age").value,
        sibsp: document.getElementById("sibsp").value,
        parch: document.getElementById("parch").value,
        fare: document.getElementById("fare").value,
        embarked: document.getElementById("embarked").value,
    };

    const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    const result = await response.json();
    const resultBox = document.getElementById("result-box");

    if (result.error) {
        resultBox.className = "alert alert-danger mt-3";
        resultBox.innerText = "Error: " + result.error;
    } else {
        resultBox.className = result.prediction === "Survived"
            ? "alert alert-success mt-3"
            : "alert alert-danger mt-3";
        resultBox.innerText = `Prediction: ${result.prediction}`;
    }

    resultBox.classList.remove("d-none");
});
