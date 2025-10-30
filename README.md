-----

# MLOps End-to-End Sentiment Analysis Project

This project demonstrates a complete, production-grade MLOps pipeline for a customer review sentiment analysis web application. The application is containerized, deployed on Kubernetes, and monitored using Prometheus and Grafana.

## Overview 📜

The goal of this project is to build a web service that can classify the sentiment of a product review as either **Positive** or **Negative**. It covers the entire machine learning lifecycle, from experiment tracking and model training to automated deployment and real-time performance monitoring.

This serves as a comprehensive guide and practical implementation of core MLOps principles.

## Features ✨

  * **Experiment Tracking**: Uses **MLflow** to log model parameters, metrics (accuracy), and artifacts.
  * **Containerization**: Packages the application and its dependencies into a lightweight **Docker** image.
  * **CI/CD Pipeline**: Automates the building and pushing of the Docker image to Docker Hub using **GitHub Actions**.
  * **Orchestration & Deployment**: Deploys the application on a local **Kubernetes** cluster using Minikube.
  * **Monitoring & Alerting**: Scrapes application metrics using **Prometheus** and visualizes them on a **Grafana** dashboard.
  * **Production-Ready Serving**: Uses **Waitress** as a production-grade WSGI server for the Flask application.

## Tech Stack 🛠️

  * **Model**: Python, Scikit-learn, Pandas
  * **Application**: Flask, Waitress
  * **MLOps Tools**: MLflow, Prometheus, Grafana
  * **Infrastructure**: Docker, Kubernetes (Minikube), Nginx (as a reverse proxy concept)
  * **CI/CD**: Git, GitHub Actions

## Project Architecture

The workflow is as follows:

1.  **Development**: A text classification model is trained using a Python script (`train.py`). The experiment, including the model file and its accuracy, is logged by MLflow into a local `model_store` directory.
2.  **Containerization**: The Flask web application (`main.py`) and the trained model data are packaged into a Docker image. The training itself happens *during the build process* to ensure a reproducible artifact.
3.  **CI/CD**: When code is pushed to the `main` branch on GitHub, a GitHub Actions workflow automatically builds this Docker image and pushes it to Docker Hub.
4.  **Deployment**: Kubernetes manifest files (`deployment.yaml`, `service.yaml`) define the desired state of the application. These files are used to deploy the Docker image from Docker Hub onto a Minikube cluster.
5.  **Monitoring**: The running application exposes its metrics (like total requests) on a `/metrics` endpoint. A Prometheus instance, also deployed on the cluster, is configured to automatically discover and scrape this data. Grafana connects to Prometheus as a data source to visualize these metrics on a real-time dashboard.

-----

## Getting Started 🚀

Follow these steps to get the entire pipeline running on your local machine.

### Prerequisites

Make sure you have the following installed:

  * **Git**
  * **Python 3.8+** and `pip`
  * **Docker Desktop** (must be running)
  * **Minikube**
  * **kubectl**

### Setup Instructions

#### 1\. Clone the Repository

Clone this project to your local machine.

```bash
git clone https://github.com/Ravij-p/sentiment-analysis-mlops.git
cd sentiment-analysis-mlops
```

#### 2\. Set Up Python Environment

Create and activate a virtual environment.

```bash
# Create environment
python -m venv venv

# Activate environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3\. Build and Run the Self-Contained Docker Image

This project is designed to be fully reproducible. The model training happens *inside the Docker build process*.

```bash
# Build the image. The --no-cache flag is important to ensure training always runs.
docker build --no-cache -t your-docker-username/sentiment-analysis .

# Run the container
docker run -p 8080:8080 your-docker-username/sentiment-analysis
```

Your application should now be running\! Open your web browser and go to **`http://localhost:8080`** to see it.

-----

### CI/CD with GitHub Actions

To enable the automated CI/CD pipeline:

1.  **Create a GitHub Repository**: Create a new repository on your GitHub account and push this project's code to it.
2.  **Add Docker Hub Secrets**: In your GitHub repository, go to **Settings** -\> **Secrets and variables** -\> **Actions**.
      * Create a new secret named `DOCKERHUB_USERNAME` with your Docker Hub username as the value.
      * Create a new secret named `DOCKERHUB_TOKEN`. For the value, [create a new Access Token](https://hub.docker.com/settings/security) on the Docker Hub website with "Read & Write" permissions and paste it here.
3.  **Push a Change**: Commit and push any change to the `main` branch. This will trigger the workflow defined in `.github/workflows/main.yml`, which will build and push the image to your Docker Hub account.

### Deployment to Kubernetes

#### 1\. Start Your Cluster

```bash
minikube start
```

#### 2\. Apply All Kubernetes Manifests

This single command will deploy your sentiment app, Prometheus, and Grafana.

```bash
kubectl apply -f kubernetes/
```

Wait a few minutes for all the pods to download their images and start up. You can check their status with `kubectl get pods`.

#### 3\. Access the Services

  * **Sentiment Analysis App**:
    ```bash
    minikube service sentiment-app-service
    ```
  * **Prometheus Dashboard**:
    ```bash
    minikube service prometheus-service
    ```
  * **Grafana Dashboard**:
    ```bash
    minikube service grafana-service
    ```
    (Log in to Grafana with username: `admin`, password: `admin`)

-----
