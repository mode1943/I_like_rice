# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext



def index(request):
    """demo """
    return render_to_response('demo/demo.html', context_instance=RequestContext(request)) 

