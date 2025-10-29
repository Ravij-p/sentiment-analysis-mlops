import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import os

# Paths are now relative to the /app directory inside the container
DATA_PATH = "data/reviews.csv"
MLFLOW_TRACKING_URI = "model_store" # No leading 'app/'

# Set tracking URI to a simple subdirectory name
mlflow.set_tracking_uri(f"file:{MLFLOW_TRACKING_URI}")

def train_model():
    print(f"MLflow tracking URI set to: {mlflow.get_tracking_uri()}")
    mlflow.set_experiment("Sentiment Analysis")

    with mlflow.start_run() as run:
        print(f"MLflow Run ID: {run.info.run_id}")
        
        df = pd.read_csv(DATA_PATH)
        df = df.dropna()
        df['sentiment'] = df['sentiment'].apply(lambda x: 1 if x == 'positive' else 0)
        X, y = df['review'], df['sentiment']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('logreg', LogisticRegression())
        ])
        pipeline.fit(X_train, y_train)

        accuracy = accuracy_score(y_test, pipeline.predict(X_test))
        print(f"Accuracy: {accuracy}")

        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(pipeline, "model")

        print("Model trained and logged successfully inside the container.")

if __name__ == "__main__":
    train_model()