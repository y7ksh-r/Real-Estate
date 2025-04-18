# Real Estate App - Docker Optimization

## Overview
This repository contains a **Docker-optimized** version of the Real Estate App, ensuring **faster builds, reduced image size, and improved security.**

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
