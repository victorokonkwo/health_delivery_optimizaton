# health_delivery_optimizaton

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/yourproject.svg)](https://github.com/yourusername/yourproject/stargazers)


## Introduction

Optimizing Health care delivery


## Installation

Provide step-by-step instructions on how to install the Conda environment from the `environment.yml` file.

### Overview

1. First, clone the repository to your local machine using Git
2. Create conda environment from environment.yml

   ```bash
    conda env create -f environment.yml
   ```
3. Activate the Conda environment:
   ```bash
   conda activate pyomo_env
   ```
4. The app.py shows a flask web app of the demand prediction model
5. The explainer.py shows the model explainability endpoint.
   ```bash
      python explainer.py
   ```
6. The optimizer.py in the resource allocation folder was implemented from this [paper](https://www.mdpi.com/2571-5577/6/5/78), though still in development because the mathematical model was too complex for pyomo using gurobi free license and also adding the demand prediction as a constaint to optimize the resource allocation.
7. The optimizer gives the optimal parameters for minimizing resource allocation.
9. There is a lot that needs to be done in improving the model accuracy and streamling the model pipline end to end.
10. Unit testing and Integration testing needs to be completed.
11. Model Tracking and Experimentation using MLFlow or KubeFlow.
12. Model Deployment on AWS
