import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import os


DATA_PATH = "data/reviews.csv"
MODEL_STORE_PATH = "app/model_store"
EXPERIMENT_NAME = "Sentiment Analysis"


mlflow.set_tracking_uri(f"file:{MODEL_STORE_PATH}")

def train_model():
    
    
    mlflow.set_experiment(EXPERIMENT_NAME)
    

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

        print(f"Model trained and logged successfully to the '{EXPERIMENT_NAME}' experiment.")

if __name__ == "__main__":
    train_model()