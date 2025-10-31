import flask
from flask import request, render_template_string
import mlflow
from prometheus_flask_exporter import PrometheusMetrics


MLFLOW_TRACKING_URI = "/app/model_store"
mlflow.set_tracking_uri(f"file:{MLFLOW_TRACKING_URI}")

def find_latest_model_uri():
    """Finds the latest run from any ACTIVE experiment and returns its model URI."""
    print(f"Searching for models in: {MLFLOW_TRACKING_URI}", flush=True)
    
    active_experiments = [exp.experiment_id for exp in mlflow.search_experiments() if exp.lifecycle_stage == 'active']
    if not active_experiments:
        raise RuntimeError("FATAL: Could not find any active MLflow experiments in the image.")

    latest_run = mlflow.search_runs(
        experiment_ids=active_experiments,
        order_by=["start_time DESC"],
        max_results=1
    )
    if latest_run.empty:
        raise RuntimeError("FATAL: Found active experiments, but they contain no runs.")
    
    run_id = latest_run.iloc[0]['run_id']
    print(f"Found latest run with ID: {run_id}", flush=True)
    model_uri = f"runs:/{run_id}/model"
    return model_uri


print("Starting application...", flush=True)
model_uri = find_latest_model_uri()
model = mlflow.pyfunc.load_model(model_uri)
print("✅ Model loaded successfully.", flush=True)

app = flask.Flask(__name__)
metrics = PrometheusMetrics(app)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sentiment Analysis</title>
    <style>
        body { font-family: sans-serif; background-color: 
        .container { max-width: 500px; margin: 50px auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        textarea { width: 95%; padding: 10px; margin-bottom: 10px; border-radius: 4px; border: 1px solid 
        input[type="submit"] { background-color: 
        h2 { color: 
        .result { margin-top: 20px; font-size: 1.2em; }
        .positive { color: green; }
        .negative { color: red; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Customer Review Sentiment Analysis</h2>
        <form action="/" method="post">
            <textarea name="text" rows="4" placeholder="Enter review text here..."></textarea><br>
            <input type="submit" value="Predict">
        </form>
        {% if prediction %}
            <div class="result">
                Prediction:
                {% if prediction == "Positive" %}
                    <span class="positive"><b>{{ prediction }}</b></span>
                {% else %}
                    <span class="negative"><b>{{ prediction }}</b></span>
                {% endif %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def predict_sentiment():
    prediction_text = None
    if request.method == 'POST':
        text = request.form['text']
        if text:
            prediction = model.predict([text])
            sentiment = "Positive" if prediction[0] == 1 else "Negative"
            prediction_text = sentiment
    return render_template_string(HTML_TEMPLATE, prediction=prediction_text)