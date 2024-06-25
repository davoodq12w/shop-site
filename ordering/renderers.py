from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from django.template.loader import get_template


def render_to_pdf(template_src, context_dict: dict = {}, css_file_path=None):
    template = get_template(template_src)
    html = template.render(context_dict)

    font_config = FontConfiguration()

    if css_file_path:
        with open(css_file_path, 'r') as css_file:
            css_string = css_file.read()
        css = CSS(string=css_string, font_config=font_config)
    else:
        css = None

    pdf = HTML(string=html).write_pdf(stylesheets=[css] if css else [])
    return pdf
