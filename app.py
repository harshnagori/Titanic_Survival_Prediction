from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model
model = joblib.load("titanic_model.pkl")

@app.route("/")
def home():
    return render_template("index.html")  # Serve the frontend

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON input from the frontend
        data = request.get_json()

        # Convert categorical inputs
        sex = 0 if data["sex"] == "Male" else 1
        embarked_dict = {"C": 0, "Q": 1, "S": 2}
        embarked = embarked_dict.get(data["embarked"], 2)

        # Create DataFrame with proper column order
        input_data = pd.DataFrame([[
            int(data["pclass"]),
            sex,
            float(data["age"]),
            int(data["sibsp"]),
            int(data["parch"]),
            float(data["fare"]),
            embarked
        ]], columns=["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"])

        # Make prediction
        prediction = model.predict(input_data)[0]
        result = "Survived" if prediction == 1 else "Not Survived"

        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=False)
