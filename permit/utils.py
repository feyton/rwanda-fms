from datetime import datetime
from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from xhtml2pdf import pisa


def permit_code(category):
    num = 0
    text = category.upper()
    year = datetime.now().year
    num += 1
    return "%s/%s/%s" % (num, text, year)


def start_date_default():
    return timezone.now() + timezone.timedelta(days=1)


def end_date_default():
    return timezone.now() + timezone.timedelta(days=2)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
