# 🏗️ Jenkins XML to Job DSL Converter  

This project converts **Jenkins `config.xml` files into Job DSL scripts**. It provides an easy-to-use **web interface** for uploading, converting, and downloading **DSL scripts**.

---

## 🚀 Features  
✅ **Supports all Jenkins Job Types:**  
   - Freestyle Jobs  
   - Pipeline Jobs  
   - Maven Jobs  
   - Matrix Jobs  
   - Multibranch Pipeline Jobs  

✅ **Extracts Job Name from Repository Name**  
✅ **Download Generated Job DSL as `.groovy` File**  
✅ **Runs Locally or with Docker (`docker-compose` supported)**  
✅ **Modern Web UI** for easy file upload and conversion  

---

## **📌 Installation & Usage**  

### **🔹 Option 1: Run Locally**
#### **1️⃣ Install Dependencies**
```bash
pip install -r requirements.txt


2️⃣ Start the Flask Server
python backend/app.py

3️⃣ Open the Application
Go to http://127.0.0.1:9000/ in your browser.


📌 Run with Docker

🔹 Option 2: Run with docker run (Without docker-compose)

1️⃣ Build the Docker Image
docker build -t xml-to-dsl .

2️⃣ Run the Docker Container
docker run -d --name xml-to-dsl-app -p 9000:9000 -v $(pwd)/uploads:/app/uploads xml-to-dsl

The -d flag runs the container in detached mode.
The -p 9000:9000 maps port 9000 inside the container to 9000 on your machine.
The -v $(pwd)/uploads:/app/uploads mounts the uploads/ directory for persistent file storage.

3️⃣ Open the Application
Go to http://127.0.0.1:9000/ in your browser.

4️⃣ Stop the Container

docker stop xml-to-dsl-app
docker rm xml-to-dsl-app


🔹 Option 3: Run with docker-compose
Using docker-compose allows for easier management and automatic volume mounting.

1️⃣ Start the Application
docker-compose up --build -d

2️⃣ Check Running Containers
docker ps

3️⃣ Stop the Application
docker-compose down

4️⃣ View Logs (If Needed)
docker-compose logs -f


📌 How It Works

1️⃣ Upload config.xml
Upload a Jenkins config.xml file via the UI

2️⃣ Convert to Job DSL
The tool extracts job details and generates a Job DSL script

3️⃣ Download DSL Script
Click "Download DSL" to save the .groovy file
