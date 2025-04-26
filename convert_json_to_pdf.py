import json
import tempfile
import subprocess
from pathlib import Path
from weasyprint import HTML
from nodejs import npx, npm


def convert_json_to_pdf(json_data: dict, theme='jsonresume-theme-onepage-plus') -> Path:
    # Create a temporary working directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Save the resume JSON
        resume_json = tmp_path / 'resume.json'
        with open(resume_json, 'w') as f:
            json.dump(json_data, f, indent=2)

        # Install the specified theme locally
        subprocess.run(['npm', 'install', theme], cwd=tmp_path, check=True)

        # Use resumed to generate HTML from JSON
        npx.call([
            'resumed',
            'render',
            '--resume', str(resume_json),
            '--theme', theme,
            '--out', 'resume.html'
        ], cwd=tmp_path)

        # Convert HTML to PDF using WeasyPrint
        html_file = tmp_path / 'resume.html'
        pdf_file = tmp_path / 'resume.pdf'
        HTML(filename=str(html_file)).write_pdf(str(pdf_file))

        # Move the PDF to a permanent location
        final_pdf = Path.cwd() / 'resume.pdf'
        final_pdf.write_bytes(pdf_file.read_bytes())

        return final_pdf
