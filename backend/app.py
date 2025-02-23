from flask import Flask, request, render_template, send_from_directory, abort
import os
from backend.converters.config_parser import parse_config_xml
from backend.converters.dsl_generator import generate_dsl

app = Flask(__name__, template_folder="../frontend/templates")

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
OUTPUT_FOLDER = os.path.join(UPLOAD_FOLDER, "dsl_outputs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename.endswith(".xml"):
            xml_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(xml_path)

            job_type, job_config = parse_config_xml(xml_path)
            if not job_type:
                return "Unsupported job type!", 400

            dsl_script = generate_dsl(job_type, job_config)
            output_filename = job_config["job_name"] + ".groovy"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)

            with open(output_path, "w") as f:
                f.write(dsl_script)

            return render_template("result.html", job_name=job_config["job_name"], dsl_script=dsl_script, filename=output_filename)

    return render_template("index.html")

@app.route("/download/<filename>")
def download_dsl(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    
    if os.path.exists(file_path):
        return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)
    else:
        abort(404, description="File not found")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)

