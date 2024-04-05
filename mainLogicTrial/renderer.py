def render_latex_template(data, template_path='template.tex'):
    with open(template_path, 'r') as file:
        template = file.read()
    
    for key, value in data.items():
        placeholder = "{{" + key + "}}"
        template = template.replace(placeholder, value)
    
    return template
