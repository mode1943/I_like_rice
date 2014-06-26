""" Create your views here."""
import json

from django.http import (HttpResponseRedirect, HttpResponse)
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm as AtForm
from django.contrib.auth import (login, logout)
from rice_member.forms import (RegForm, LoginForm)
from rice_member.models import (Member, Group, GroupRequestAct)


def mem_login(request):
    """ the function for the member login"""
    flag = 10
    again = False
    if request.method == 'POST':
        if request.session.get('login_error', 0) and request.session['login_error'] >= flag:
            form1 = LoginForm(data=request.POST)
            form = form1
        else:
            form2 = AtForm(data=request.POST)
            form = form2
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('index'))
        else:
            if not request.session.get('login_error', 0):
                request.session['login_error'] = 1
            else:
                request.session['login_error'] += 1
            if request.session['login_error'] >= flag:
                again = True
                form = form1
            else:
                form = form2
    else:

        if request.session.get('login_error', 0) and request.session['login_error'] >= flag:
            again = True
            form = LoginForm()
        else:
            form = AtForm()
    template_var = {'form': form}
    return render_to_response('member/login.html', template_var, 
                              context_instance=RequestContext(request))




def register(request):
    """the function for the member register"""
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            mem = Member.create_member(username, password=password, email=email)
            if mem is not None:
                return HttpResponseRedirect(reverse('reg_success'))
    else:
        form = RegForm()
    template_var = {'form':form}
    return render_to_response('member/register.html', template_var, \
                             context_instance=RequestContext(request))



def mem_logout(request):
    """ the function for the member logout """
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def applyfor_group(request):
    """the member apply to join the group """
    if request.REQUEST.get('member_id', 0) and request.REQUEST.get('group_id', 0):
        member_id = int(request.REQUEST.get('member_id'))
        group_id = int(request.REQUEST.get('group_id'))
        rep = GroupRequestAct.create_act(member_id, group_id)
        if rep:
            data = {"result": 1}
        else:
            data = {"result": 0}
    else:
        data = {"result": 0}
    return HttpResponse(json.dumps(data))
    
    
def accept_group(request):
    """ the group accept the member to join """
    ms_id = request.user.member.pk
    if request.REQUEST.get('member_id', 0) and request.REQUEST.get('group_id', 0):
        member_id = int(request.REQUEST.get('member_id'))
        group_id = int(request.REQUEST.get('group_id'))
        rep = GroupRequestAct.accept_act(member_id, group_id, ms_id)
        if rep:
            data = {'result': 1}
        else:
            data = {'result': 0}
    else:
        data = {"result": 0}
    return HttpResponse(json.dumps(data))


def create_group(request):
    """ create one group """
    print '111'
    if request.method == 'POST':
        mem = request.user.member
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        print '22222'
        group = Group.create_group(mem, name, description)
        if group:
            data = {'result': 1}
        else:
            data = {'result': 0}
        return HttpResponse(json.dumps(data))

