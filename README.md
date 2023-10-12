# health_delivery_optimizaton

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/yourproject.svg)](https://github.com/yourusername/yourproject/stargazers)


## Introduction

Optimizing Health care delivery


## Installation

Provide step-by-step instructions on how to install the Conda environment from the `environment.yml` file.

### Clone the Repository

1. First, clone the repository to your local machine using Git:

   ```bash
    conda env create -f environment.yml
   ```
2. Activate the Conda environment:
   ```bash
   conda activate pyomo_env
   ```
3. The app.py shows a flask web app of the demand prediction model
4. The explainer.py shows the model explainability endpoint.
   ```bash
      python explainer.py
   ```
5. The optimizer.py in the resource allocation folder was implemented from this [paper](https://www.mdpi.com/2571-5577/6/5/78), though still in development because the mathematical model was too complex for pyomo usin gurobi free license.
   
