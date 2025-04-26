import json
from pathlib import Path
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
import tempfile

def convert_json_to_pdf(json_data: dict) -> Path:
    # Setup Jinja environment
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("resume_template.html")

    # Render HTML with resume data
    html_content = template.render(**json_data)

    # Save to a temporary HTML file
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        html_file = tmp_path / "resume.html"
        pdf_file = tmp_path / "resume.pdf"

        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Generate PDF using WeasyPrint
        HTML(str(html_file)).write_pdf(str(pdf_file))

        # Move to a permanent location
        final_pdf = Path.cwd() / "resume.pdf"
        final_pdf.write_bytes(pdf_file.read_bytes())
        return final_pdf
