# Real Estate App - Docker Optimization

## Details of the Project
The **Real Estate App** is a full-stack web application collaboratively built by me and my friends. My primary role was to handle the **complete DevOps automation and deployment pipeline** using modern tools like **Docker**, **Kubernetes**, and **Terraform**, all while staying within the **AWS Free Tier** limits.

The infrastructure is fully managed with Terraform, provisioning resources like EC2, IAM, S3, and DynamoDB. I've also implemented **Terraform remote state locking** using S3 and DynamoDB to ensure safe and consistent deployments across environments.

This project is structured across three repositories:
- [App Deployment Repo](https://github.com/y7ksh-r/Real-Estate) – includes Docker-related files and CI/CD workflows (The current Repo)
- [Terraform Infrastructure Repo](https://github.com/y7ksh-r/Real-estate-app-infra) – for provisioning AWS infrastructure and managing remote backend state.
- [Kubernetes Manifests Repo](https://github.com/y7ksh-r/Real-estate-app) – includes all necessary manifests for deploying the app on a Kubernetes cluster.

This repository contains a **Docker-optimized** version of the Real Estate App, ensuring **faster builds, reduced image size, and improved security.**

You can find the **architecture diagram** of the entire setup below, which outlines how the components integrate in a production-like DevOps pipeline.

## Architecture Diagram
![XPD1RZ~1](https://github.com/user-attachments/assets/d306a927-31a4-46ca-8599-cfbbea27f43a)


## Optimizations Applied
- **Multi-Stage Builds**: Reduces image size by separating dependency installation.
- **Alpine-based Slim Image**: Uses `python:3.10-slim` for minimal footprint.
- **Layer Minimization**: Removes unnecessary files to reduce build context.
- **Dive Analysis Results**:
  - **Before Optimization**: `1.6 GB`
  - **After Optimization**: `280 MB` (83% reduction)

## Real-World Use Case
Optimizing Docker images ensures **faster deployments, lower storage costs, and quicker scaling.** This is crucial for microservices and cloud-based deployments where **every MB matters.**

**This is Step 1 out of 3, please visit the provided link at the end to complete the entire project installation.**

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

**Now head over to [Terraform Infrastructure Repo](https://github.com/y7ksh-r/Real-estate-app-infra) & continue the further steps to deploy the entire Application!**
