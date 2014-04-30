from django.shortcuts import render_to_response, redirect, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from haccp.forms import QuatFormTech, QuatFormMan
from haccp.models import QuatForm, User
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

import datetime

# Create your views here.
def index(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('haccp/index.html',context_dict, context)

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



def user_login(request):
    context= RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #is_manager =User.objects.filter(type='MAN')
        user = authenticate(username = username , password = password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # if is_manager:
                #     return HttpResponseRedirect('/haccp/ManagerDashBoard.html')
                #
                # else:
                #     return HttpResponseRedirect('/haccp/TechnicianDashBoard.html')
                return HttpResponseRedirect('/haccp/dashboard.html')
            else:
                return HttpResponse("Your account is disabled")
        else:
            print "Invalid login details {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('/haccp/login.html', {}, context)


def TechDashboardView(request):
    context = RequestContext(request)
    # if not request.user.is_authenticated():
    #     return redirect('/haccp/')
    # else:
    #     render_to_response('/haccp/TechnicianDashBoard.html',{}, context)
    return render(request,'/haccp/TechnicianDashBoard.html')
#def type_check(user):
#    is_manager =User.objects.filter(type='MAN')
#    return is_manager

#@user_passes_test(type_check)

@login_required
def ManDashboardView(request):
    if not request.user.is_authenticated():
        return redirect('/haccp/')
    else:
        HttpResponseRedirect('/haccp/ManagerDashBoard.html')

def logout_view(request):
    logout(request)
    return redirect('/haccp/')

def dashboardview(request):
    is_manager = User.objects.filter(id=request.user.id).filter(type='MAN')
    context = RequestContext(request)
    context_dict = {'is_manager':is_manager}
    return render_to_response('haccp/dashboard.html',context_dict, context)