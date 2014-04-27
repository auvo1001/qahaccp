from django.shortcuts import render_to_response, redirect, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponse
from haccp.forms import QuatFormTech, QuatFormMan
from haccp.models import QuatForm
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse

import datetime

# Create your views here.
def index(request):
    context =RequestContext(request)
    context_dict = {}
    return render_to_response('haccp/index.html',context_dict,context)

class QuatFormTodayView(ListView):
    queryset = QuatForm.objects.filter(date=datetime.datetime.now().date())

    def get_context_data(self, **kwargs):
        context = super(QuatFormTodayView, self).get_context_data(**kwargs)
        context['now'] = datetime.datetime.now().date()
        return context

def QuatFormTechView(request):

    context =RequestContext(request)
    if request.method =='POST':
        form = QuatFormTech(request.POST)
        if form.is_valid():
            form.save(commit=True)
        else:
            print form.errors
    else:
        form = QuatFormTech
        result = render_to_response('haccp/quaternary_form.html',{'form':form}, context)
    return result


class QuatFormManView(UpdateView):

   model = QuatForm
   template_name='haccp/quaternary_form_manager_form.html'

   def get_success_url(self):
        return reverse('QuatFormTodayView')

   def get_context_data(self, **kwargs):

        context = super(QuatFormManView, self).get_context_data(**kwargs)
        context['action'] = reverse('QuatFormManView',
                                    kwargs={'pk': self.get_object().id})
        return context