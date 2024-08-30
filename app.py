from flask import Flask, request, send_file, render_template
from io import BytesIO
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

    # LaTeX template files
    main_tex = f"""
    \\documentclass{{article}}
    \\begin{{document}}
    \\title{{Student Information}}
    \\author{{{name}}}
    \\date{{USN: {usn}}}
    \\include{{section1}}
    \\end{{document}}
    """

    
    #section1_tex = """
    #\\section{{Introduction}}
    #This is the introduction section.
    #"""

    #section2_tex = """
    #\\section{{Details}}
    #This section contains details.
    #"""
    

    # Write LaTeX files to the temporary directory
    with open('temp_latex/main.tex', 'w') as f:
        f.write(main_tex)
    
    with open('temp_latex/section1.tex', 'w') as f:
        f.write(section1_tex)
    
    #with open('temp_latex/section2.tex', 'w') as f:
        #f.write(section2_tex)
    

    try:
        # Check if temp_latex directory exists and create it if not
        os.makedirs('temp_latex', exist_ok=True)

        # Run pdflatex
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

    print(os.path.abspath('main.tex'))



if __name__ == '__main__':
    app.run(debug=True)
