from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import View

from .forms import AddPermitForm
from .models import TransportPermit, HarvestingPermit, District, Village, Sector, Cell
from .utils import generate_pdf_weasy, render_to_pdf
from .forms import AddressForm


@method_decorator(login_required, name='dispatch')
class PermitView(View):
    def get(self, *args, **kwargs):
        context = {
            'permits': TransportPermit.objects.all(),
            'form': AddPermitForm

        }
        return render(self.request, 'pages/permits.html', context)


permit = PermitView.as_view()


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


def generate_permit_pdf(request, *args, **kwargs):
    template = 'print/permit.html'
    context = {}
    return generate_pdf_weasy(request, template, 'test', context)


class HarvestingPermitView(View):
    def get(self, *args, **kwargs):
        permits = HarvestingPermit.objects.all()[:5]
        context = {'permits': permits}
        return render(self.request, 'pages/hp-list.html', context)


hp_list_view = HarvestingPermitView.as_view()


class CreateHPermitView(View):
    def get(self, *args, **kwargs):
        address_form = AddressForm
        form = AddPermitForm()
        context = {'form': form, 'a_form': address_form}
        return render(self.request, 'forms/create-wizard.html', context)


create_hp_view = CreateHPermitView.as_view()


class CreateTPermitView(View):
    def get(self, *args, **kwargs):
        form = AddPermitForm()
        return render(self.request, 'forms/create-wizard.html', {'form': form})


create_tp_view = CreateHPermitView.as_view()


#
def load_district(request):
    country_id = request.GET.get('province')
    d_id = request.GET.get('district')
    if country_id is not None:
        cities = District.objects.filter(
            province_id=country_id).order_by('name')
        return render(request, 'forms/dropdown.html', {'options': cities})
    if d_id is not None:
        sectors = Sector.objects.filter(district_id=d_id).order_by('name')
        return render(request, 'forms/dropdown.html', {'options': sectors})
