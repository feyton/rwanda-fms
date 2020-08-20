from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View

from permit.models import TransportPermit

from .forms import (ConstructionSpeciesForm, ForestForm, HPermitForm,
                    HPRequestorForm, TimberSpeciesForm)
from .models import HarvestingPermit



class HarvestingPermitView(ListView):
    model = HarvestingPermit
    template_name = 'list.html'
    context_object_name = 'permits'
    queryset = HarvestingPermit.objects.all().order_by('-start_date')
    paginate_by = 5


hp_list_view = HarvestingPermitView.as_view()


class CreateHPermitView(View):
    def get(self, *args, **kwargs):
        context = {
            'p_form': HPermitForm,
            'r_form': HPRequestorForm,
            'f_form': ForestForm,
            'c_form': ConstructionSpeciesForm,
            't_form': TimberSpeciesForm,
        }
        return render(self.request, 'hp-create.html', context)

    def post(self, *args, **kwargs):
        p_form = HPermitForm(self.request.POST or None)
        r_form = HPRequestorForm(self.request.POST or None)
        f_form = ForestForm(self.request.POST or None)
        c_form = ConstructionSpeciesForm(self.request.POST or None)
        t_form = TimberSpeciesForm(self.request.POST or None)
        if r_form.is_valid():
            r = r_form.save()
            f = f_form.save()
            p = p_form.save(commit=False)
            p.requestor = r
            p.forest = f
            p.save()
            return redirect(p)

        context = {
            'p_form': HPermitForm(self.request.POST or None),
            'r_form': HPRequestorForm(self.request.POST or None),
            'f_form': ForestForm(self.request.POST or None),
            'c_form': ConstructionSpeciesForm(self.request.POST or None),
            't_form': TimberSpeciesForm(self.request.POST or None),
        }
        return render(self.request, 'hp-create.html', context)


create_hp_view = CreateHPermitView.as_view()


class HPermitDetailView(DetailView):
    model = HarvestingPermit
    template_name = "detail.html"
    context_object_name = 'permit'
