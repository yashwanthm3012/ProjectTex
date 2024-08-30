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

    # LaTeX template files
    main_tex = f"""
    \\documentclass{{article}}

    \\usepackage[english]{{babel}}
    \\usepackage[letterpaper,top=2cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm]{{geometry}}
    \\usepackage{{amsmath}}
    \\usepackage{{graphicx}}
    \\usepackage[colorlinks=true, allcolors=blue]{{hyperref}}

    \\title{{Your Paper}}
    \\author{{{name}}}  % Assuming you want to use the 'name' variable for the author
    \\date{{\\today}}
    \\begin{{document}}
    \\maketitle

    \\textbf{{{usn}}}
    \\include{{Introduction}}  

    \\end{{document}}
    """


    section1_tex = """
    \\section{Introduction}
    This is the introduction section.
    """

    # Write LaTeX files to the temporary directory
    with open('temp_latex/main.tex', 'w') as f:
        f.write(main_tex)
    
    with open('temp_latex/Introduction.tex', 'w') as f:
        f.write(section1_tex)

    try:
        # Run pdflatex and capture output
        result = subprocess.run(
            ['pdflatex', '-output-directory=temp_latex', 'temp_latex/main.tex'],
            capture_output=True, text=True
        )

        # Print the stdout and stderr for debugging
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode != 0:
            return "An error occurred while generating the PDF. See logs for details.", 500

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
