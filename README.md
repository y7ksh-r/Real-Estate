# Real Estate App - Docker Optimization

## Overview
This repository contains a **Docker-optimized** version of the Real Estate App, ensuring **faster builds, reduced image size, and improved security.**

## Architecture Diagram
![Docker Optimization](https://raw.githubusercontent.com/y7ksh-r/Real-Estate/main/docs/docker_optimization.png)  
*Multi-stage build to keep image size minimal and remove unnecessary dependencies.*

## Optimizations Applied
- **Multi-Stage Builds**: Reduces image size by separating dependency installation.
- **Alpine-based Slim Image**: Uses `python:3.10-slim` for minimal footprint.
- **Layer Minimization**: Removes unnecessary files to reduce build context.
- **Dive Analysis Results**:
  - **Before Optimization**: `359 MB`
  - **After Optimization**: `280 MB` (22% reduction)

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

## Future Enhancements
- Implement **Docker Slim** for even smaller images.
- Enable **CI/CD with GitHub Actions** for automated builds.
