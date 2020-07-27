from django.shortcuts import get_object_or_404, render
from .models import TransportPermit
from django.views.generic import View
from .forms import AddPermitForm
from .utils import render_to_pdf
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse


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