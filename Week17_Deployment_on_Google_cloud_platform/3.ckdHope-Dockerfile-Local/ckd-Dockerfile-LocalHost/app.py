from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib

app = Flask(__name__, template_folder="templates")

# Load trained model
model = joblib.load("finalized_model_ckd.sav")

@app.route("/")
def index():
    return render_template("input.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        age = float(request.form["age"])
        blood_pressure = float(request.form["blood_pressure"])
        specific_gravity = float(request.form["specific_gravity"])
        albumin = float(request.form["albumin"])
        sugar = float(request.form["sugar"])

        input_data = np.array([[age, blood_pressure, specific_gravity, albumin, sugar]])
        prediction = model.predict(input_data)

        result = (
            "Chronic Kidney Disease Detected"
            if prediction[0] == 1
            else "No Chronic Kidney Disease"
        )

        return render_template("output.html", result=result)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
