# ACEest Fitness Management Application

## 1. Project Overview

ACEest Fitness is a fitness management application developed as part of a DevOps assignment. The project demonstrates version control, automated testing, containerization, and Continuous Integration (CI) using GitHub Actions and Jenkins.

The repository contains the application, multiple supplied source versions, automated tests, a Dockerfile, and CI pipeline configurations.

### Objectives

- Maintain source code using Git and GitHub.
- Validate Python syntax across the supplied application versions.
- Automate testing using pytest.
- Containerize the project using Docker.
- Run automated checks using GitHub Actions.
- Implement a Jenkins pipeline for validation, testing, Docker image building, and image promotion.
- Demonstrate how defects can be identified through automated checks.

## 2. Repository Structure

```text
aceest-devops/
├── .github/
│   └── workflows/
│       └── main.yml
├── source_versions/
│   ├── Aceestver-1.0.py
│   ├── Aceestver-1.1.py
│   ├── Aceestver1.1.2.py
│   ├── Aceestver2.0.1.py
│   ├── Aceestver-2.1.2.py
│   ├── Aceestver-2.2.1.py
│   ├── Aceestver-2.2.4.py
│   ├── Aceestver-3.0.1.py
│   ├── Aceestver-3.1.2.py
│   └── Aceestver-3.2.4.py
├── tests/
│   └── test_app.py
├── app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
└── README.md

3. Prerequisites

To run the project locally, install:

* Python 3
* pip
* Git
* Docker (for container-related steps)

Jenkins is required to execute the Jenkins pipeline.