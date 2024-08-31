from flask import Flask, request, send_file, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML file

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form.get('name', '').encode('utf-8').decode('utf-8')
    usn = request.form.get('usn', '').encode('utf-8').decode('utf-8')
    
    # Create a temporary directory to hold LaTeX files
    temp_dir = 'temp_latex'
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Read the LaTeX template from the file with proper encoding
        with open('main.tex', 'r', encoding='utf-8') as file:
            template_content = file.read()

        # Read the title page template from the file with proper encoding
        with open('titlepage.tex', 'r', encoding='utf-8') as file:
            title_content = file.read()

        # Replace placeholders with actual values
        title_page_tex = title_content.replace('__NAME__', name).replace('__USN__', usn)

        # Write the modified LaTeX content to the temporary files
        with open(os.path.join(temp_dir, 'main.tex'), 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        with open(os.path.join(temp_dir, 'titlepage.tex'), 'w', encoding='utf-8') as f:
            f.write(title_page_tex)

        # Run pdflatex to compile the LaTeX file into a PDF
        result = subprocess.run(
            ['pdflatex', '-output-directory=' + temp_dir, os.path.join(temp_dir, 'main.tex')],
            capture_output=True, text=True, check=True
        )

        # Print both stdout and stderr for troubleshooting
        #print(result.stdout)
        #print(result.stderr)

    except subprocess.CalledProcessError as e:
        print("Error during pdflatex compilation:", e.stderr)
        return "An error occurred while generating the PDF.", 500

    # Send the generated PDF
    pdf_path = os.path.join(temp_dir, 'main.pdf')
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return "PDF generation failed.", 500

if __name__ == '__main__':
    app.run(debug=True)
