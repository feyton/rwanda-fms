import csv
import os
import random
from datetime import datetime
from io import BytesIO

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from reportlab.pdfgen import canvas
import os
os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
from xhtml2pdf import pisa

dirs = settings.BASE_DIR


def permit_code():
    string = 'QWERTYUIOPASDFGHJKLZXCVBNM'
    randomstr = ''.join((random.choice(string)) for x in range(4))
    return '%s-%s' % (datetime.now().strftime('%Y%m%d'), randomstr)


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


def report_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Start writing the PDF here
    p.drawString(100, 100, 'Hello world.')
    # End writing

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    # PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def generate_pdf_weasy(request, template, file_name, context):
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename=%s.pdf" % (file_name)
    html = render_to_string(template, context)

    font_config = FontConfiguration()
    pdf = HTML(string=html, base_url=request.build_absolute_uri()
               ).write_pdf(response, font_config=font_config)
    return response


