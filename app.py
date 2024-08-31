from flask import Flask, request, send_file, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML file

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    usn = request.form['usn']
    
    # Create a temporary directory to hold LaTeX files
    os.makedirs('temp_latex', exist_ok=True)

    # Read the LaTeX template from the file
    with open('template.tex', 'r') as file:
        template_content = file.read()

    # Replace placeholders with actual values
    main_tex = template_content.replace('__NAME__', name).replace('__USN__', usn)

    # Write the modified LaTeX content to the temporary main.tex file
    with open('temp_latex/main.tex', 'w') as f:
        f.write(main_tex)
    
    try:
        # Run pdflatex to compile the LaTeX file into a PDF
        result = subprocess.run(
            ['pdflatex', '-output-directory=temp_latex', 'temp_latex/main.tex'],
            capture_output=True, text=True, check=True
        )

        # Print both stdout and stderr for troubleshooting
        print(result.stdout, result.stderr)

    except subprocess.CalledProcessError as e:
        print("Error during pdflatex compilation:", e.stderr)
        return "An error occurred while generating the PDF.", 500

    # Send the generated PDF
    pdf_path = 'temp_latex/main.pdf'
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return "PDF generation failed.", 500

if __name__ == '__main__':
    app.run(debug=True)
