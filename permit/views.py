import csv
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View

from .forms import (AddPermitForm, DestinationForm, OriginForm, RequestorForm,
                    TransportVehicleForm)
from .models import (Category, Cell, District, Province, Sector,
                     TransportPermit, Village)
from .utils import generate_pdf_weasy, render_to_pdf

dirs = settings.BASE_DIR


@method_decorator(login_required, name='dispatch')
class TransportPermitView(View):
    def get(self, *args, **kwargs):
        user = self.request.user

        if user.is_dfnro():
            d = {'licenses': TransportPermit.objects.filter(
                officer=user.dfnro)}
            return render(self.request, 'dfnro-list.html', d)
        context = {
            'permits': TransportPermit.objects.filter(prepared_by=user).order_by('-created'),
            'form': AddPermitForm

        }
        return render(self.request, 'pages/tp-list.html', context)


tp_permit = TransportPermitView.as_view()


@login_required
def print_permit(request, pk):
    permit = get_object_or_404(TransportPermit, pk=pk)
    if permit:
        template = 'pages/print-permit.html'
        context = {'permit': permit}
        render_to_pdf(template, context)
    raise PermissionDenied


def permit_detail(request, pk):
    permit = get_object_or_404(TransportPermit, pk=pk)
    data = permit
    return JsonResponse(data)


def test_template(request):
    template = 'print/permit.html'
    return render(request, template)


def generate_tpermit_pdf(request, pk, *args, **kwargs):
    permit = get_object_or_404(TransportPermit, pk=pk)
    template = 'print/transport.html'
    context = {'permit': permit,
               'categories': Category.objects.all()}
    return generate_pdf_weasy(request, template, permit.code, context)


class CreateTPermitView(View):
    def get(self, *args, **kwargs):
        context = {
            'r_form': RequestorForm,
            'd_form': DestinationForm,
            'v_form': TransportVehicleForm,
            'o_form': OriginForm,
            'p_form': AddPermitForm
        }
        return render(self.request, 'forms/tp-create.html', context)

    def post(self, *args, **kwargs):
        r_form = RequestorForm(self.request.POST or None)
        d_form = DestinationForm(self.request.POST or None)
        v_form = TransportVehicleForm(self.request.POST or None)
        o_form = OriginForm(self.request.POST or None)
        p_form = AddPermitForm(self.request.POST or None)

        if r_form.is_valid() and d_form.is_valid() and v_form.is_valid() and o_form.is_valid() and p_form.is_valid():
            requestor = r_form.save()
            destination = d_form.save()
            origin = o_form.save()
            vehicle = v_form.save()
            permit = p_form.save(commit=False)
            permit.requestor = requestor
            permit.vehicle = vehicle
            permit.origin = origin
            permit.destination = destination
            permit.prepared_by = self.request.user
            permit.save()
            messages.success(self.request, 'New permit created successfully')
            return redirect(permit)

        context = {
            'r_form': r_form,
            'd_form': d_form,
            'v_form': v_form,
            'o_form': o_form,
            'p_form': p_form
        }
        return render(self.request, 'forms/tp-create.html', context)


create_tp_view = CreateTPermitView.as_view()


#
def load_district(request):
    country_id = request.GET.get('province')
    d_id = request.GET.get('district')
    s_id = request.GET.get('sector')
    c_id = request.GET.get('cell')
    if country_id is not None:
        cities = District.objects.filter(
            province_id=country_id).order_by('name')
        return render(request, 'forms/dropdown.html', {'options': cities})
    if d_id is not None:
        sectors = Sector.objects.filter(district_id=d_id).order_by('name')
        return render(request, 'forms/dropdown.html', {'options': sectors})
    if s_id is not None:
        cells = Cell.objects.filter(sector_id=s_id)
        return render(request, 'forms/dropdown.html', {'options': cells})
    if c_id is not None:
        cells = Village.objects.filter(cell_id=c_id)
        return render(request, 'forms/dropdown.html', {'options': cells})


def transport_permit_single_view(request, pk):
    permit = get_object_or_404(TransportPermit, pk=pk)
    context = {'permit': permit}
    return render(request, 'permit/tp/single.html', context)


def edit_tp_permit(request, pk):
    permit = get_object_or_404(TransportPermit, pk=pk)
    context = {
        'r_form': RequestorForm(instance=permit.requestor),
        'd_form': DestinationForm(instance=permit.destination),
        'v_form': TransportVehicleForm(instance=permit.vehicle),
        'o_form': OriginForm(instance=permit.origin),
        'p_form': AddPermitForm(instance=permit)
    }
    if request.method == 'POST':
        r_form = RequestorForm(request.POST, instance=permit.requestor)
        d_form = DestinationForm(request.POST, instance=permit.destination)
        v_form = TransportVehicleForm(request.POST, instance=permit.vehicle)
        o_form = OriginForm(request.POST, instance=permit.origin)
        p_form = AddPermitForm(request.POST, instance=permit)
        if r_form.is_valid() and d_form.is_valid() and v_form.is_valid() and o_form.is_valid() and p_form.is_valid():
            requestor = r_form.save()
            destination = d_form.save()
            origin = o_form.save()
            vehicle = v_form.save()
            permit = p_form.save()
            messages.success(
                request, 'Permit with %s code has been edited.' % permit.code)
            return redirect(permit)
        else:
            messages.error(request, 'Error in form')
            return render(request, 'forms/tp-create.html', context)

    return render(request, 'forms/tp-create.html', context)


def export_csv():
    import csv
    reader = csv.DictReader(open(os.path.join(dirs, "static/adm.csv")))
    for raw in reader:
        province = raw['PROVINCE']
        p_code = raw['PCODE'].strip('RW')
        district = raw['DISTRICT']
        d_code = raw['DCODE'].strip('RW')
        sector = raw['SECTOR']
        s_code = raw['SCODE'].strip('RW')
        cell = raw['CELL']
        c_code = raw['CCODE'].strip('RW')

        prov, created = Province.objects.get_or_create(
            code=p_code, name=province)
        dist, created = District.objects.get_or_create(
            code=d_code, name=district, province=prov)
        sec, created = Sector.objects.get_or_create(
            code=s_code, name=sector, district=dist)
        cel, created = Cell.objects.get_or_create(
            name=cell, code=c_code, sector=sec)


class DashboardSummary(View):
    def get(self, *args, **kwargs):
        data = {}
        return JsonResponse(data)

dashboard_summary = DashboardSummary.as_view()
