from flask import Flask, request, render_template, send_from_directory, abort, flash
import os
from werkzeug.utils import secure_filename
from converters.config_parser import parse_config_xml
from converters.dsl_generator import generate_dsl

# Initialize Flask app
app = Flask(__name__, template_folder="/app/frontend/templates", static_folder="/app/frontend/static")
app.secret_key = "supersecretkey"  # Required for flash messages

# Define correct folder paths
BASE_UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
UPLOAD_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "uploads_XML")  # XML uploads folder
OUTPUT_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, "convert_DSL")  # Converted DSL output folder

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"xml"}

def allowed_file(filename):
    """Check if the file is an allowed XML type."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            flash("No file selected!", "error")
            return render_template("index.html")

        if not allowed_file(file.filename):
            flash("Invalid file type! Only XML files are allowed.", "error")
            return render_template("index.html")

        try:
            # Secure and save the uploaded file in "uploads_XML/"
            filename = secure_filename(file.filename)
            xml_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(xml_path)

            # Parse the XML configuration
            job_type, job_config = parse_config_xml(xml_path)

            if not job_type or "job_name" not in job_config:
                flash("Invalid or unsupported XML format!", "error")
                return render_template("index.html")

            # Generate the DSL script
            dsl_script = generate_dsl(job_type, job_config)
            output_filename = secure_filename(job_config["job_name"] + ".groovy")
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)  # Save in "convert_DSL/"

            # Save the DSL script
            with open(output_path, "w") as f:
                f.write(dsl_script)

            return render_template("result.html", job_name=job_config["job_name"], dsl_script=dsl_script, filename=output_filename)

        except Exception as e:
            flash(f"Error processing file: {str(e)}", "error")
            return render_template("index.html")

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

