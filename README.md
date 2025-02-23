# Jenkins XML to Job DSL Converter

## Overview
This application converts **Jenkins `config.xml`** files into **Job DSL scripts**.

## Features
✅ Supports **Freestyle, Pipeline, Maven, Matrix, and Multibranch jobs**  
✅ Parses **config.xml** and extracts all job configurations  
✅ Generates **Job DSL scripts dynamically**  
✅ Provides **a simple Web UI for file uploads**  
✅ Runs as **a containerized app using Docker**

## Installation

### 1️⃣ Run Without Docker
```bash
pip install -r requirements.txt
python backend/app.py

