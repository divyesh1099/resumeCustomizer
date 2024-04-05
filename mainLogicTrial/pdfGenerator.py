import subprocess

def generate_pdf(latex_content, output_filename='output'):
    with open('temp.tex', 'w') as file:
        file.write(latex_content)
    
    subprocess.run(['pdflatex', 'temp.tex'], stdout=subprocess.DEVNULL)
    # Clean up auxiliary files if needed (e.g., temp.aux, temp.log)
