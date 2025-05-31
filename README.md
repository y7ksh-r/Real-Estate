# Real Estate App

## Details of the Project
The **Real Estate App** is a full-stack web application collaboratively built by me and my friends. My primary role was to handle the **complete DevOps automation and deployment** using modern tools like **Docker**, **Kubernetes**, and **Terraform**, all while staying within the **AWS Free Tier** limits.

The infrastructure is fully managed with Terraform, provisioning resources like EC2, IAM, S3, and DynamoDB. I've also implemented **Terraform remote state locking** using S3 and DynamoDB to ensure safe and consistent deployments across environments.

This project is structured across three repositories:
- [App](https://github.com/y7ksh-r/Real-Estate/tree/main/App) – includes all the necessary files of the Real Estate App.
- [Docker](https://github.com/y7ksh-r/Real-Estate/tree/main/Docker) – includes Docker-related files.
- [Terraform Infrastructure](https://github.com/y7ksh-r/Real-Estate/tree/main/Terraform-infra) – for provisioning AWS infrastructure and managing remote backend state.
- [Kubernetes Manifests](https://github.com/y7ksh-r/Real-Estate/tree/main/K8s-manifests) – includes all necessary manifests for deploying the app on a Kubernetes cluster.

You can find the **architecture diagram** of the entire setup below, which outlines how the components integrate in a production-like DevOps pipeline.

## Architecture Diagram
![XPD1RZ~1](https://github.com/user-attachments/assets/d306a927-31a4-46ca-8599-cfbbea27f43a)


# 1. Docker
This [folder](https://github.com/y7ksh-r/Real-Estate/tree/main/Docker) contains a **Docker-optimized** version of the Real Estate App, ensuring **faster builds, reduced image size, and improved security.**

## Optimizations Applied
- **Multi-Stage Builds**: Reduces image size by separating dependency installation.
- **Alpine-based Slim Image**: Uses `python:3.10-slim` for minimal footprint.
- **Layer Minimization**: Removes unnecessary files to reduce build context.
- **Dive Analysis Results**:
  - **Before Optimization**: `1.6 GB`
  - **After Optimization**: `280 MB` (83% reduction)

## Real-World Use Case
Optimizing Docker images ensures **faster deployments, lower storage costs, and quicker scaling.** This is crucial for microservices and cloud-based deployments where **every MB matters.**


## Usage
1. Clone the repository:
   ```sh
   git clone https://github.com/y7ksh-r/Real-Estate.git
   cd Real-Estate
   ```
2. Build the Docker image:
   ```sh
   docker build -t real-estate-app .
   ```
3. Run the container:
   ```sh
   docker run -p 8000:8000 real-estate-app
   ```
4. Check image size & layers using `dive`:
   ```sh
   dive real-estate-app
   ```

# 2. Terraform Infrastructure

## Overview
This infrastructure demonstrates the complete DevOps pipeline and automation for a cloud-native Real Estate web application, optimized for AWS Free Tier usage. It uses Terraform to provision and manage scalable, secure cloud resources on AWS, including the following features:

## Features
- **State Locking with S3 & DynamoDB**: Prevents race conditions in Terraform deployments.
- **Infrastructure as Code (IaC)**: Enables reproducible and version-controlled deployments.
- **Secure Access Control**: IAM roles and security groups restrict access.
- **Scalability & Modularity**: Easily extendable to accommodate future changes.

## Real-World Use Case
This Terraform setup allows teams to **quickly provision and manage cloud infrastructure** without manual intervention. It's especially useful for **DevOps workflows** where infrastructure needs to be **version-controlled, auditable, and automated.**

## Deployment Steps
1. Navigate to your respective terraform folder:
   ```sh
   cd Terraform-infra
   ```
2. Initialize Terraform:
   ```sh
   terraform init
   ```
3. Plan the deployment:
   ```sh
   terraform plan
   ```
4. Apply changes:
   ```sh
   terraform apply -auto-approve
   ```
5. Destroy infrastructure (if needed):
   ```sh
   terraform destroy -auto-approve
   ```

## Future Enhancements
- Implement **Terraform modules** for better reusability.
- Integrate **AWS Lambda for automated scaling.**
- Add **monitoring with Prometheus & Grafana.**

# 3. Kubernetes Manifests

  ## Overview
This directory contains the Kubernetes manifests required to deploy the Real Estate web application on a lightweight K3s cluster hosted on AWS EC2, optimized for Free Tier usage. These manifests define the application's:

## Features
- **Declarative Configuration**: All K8s resources are managed via YAML files.
- **Load Balancing**: Uses a Kubernetes **Ingress Controller**.
- **Auto-Healing & Scaling**: Ensures high availability.
- **Monitoring with Prometheus & Grafana**.

## Real-World Use Case
Deploying via Kubernetes allows the app to **scale efficiently**, handle high traffic loads, and maintain **zero-downtime deployments.**

## Deployment Steps
1. Clone the repository:
   ```sh
   cd K8s-manifests
   ```
2. Deploy the application:
   ```sh
   kubectl apply -f deployment.yaml
   ```
3. Verify pod status:
   ```sh
   kubectl get pods
   ```
4. Access the application via the **LoadBalancer or Ingress Controller**.

## Future Enhancements
- Integrate **ArgoCD for GitOps-based deployments**.
- Implement **service mesh (Istio or Linkerd) for better traffic control.**
