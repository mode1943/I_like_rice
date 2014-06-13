# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

from rice_rice.models import (Rice, RiceRoom)
from rice_member.models import (Group, Member)


def demo(request):
    """demo """
    return render_to_response('rice/demo.html', context_instance=RequestContext(request)) 



def index(request):
    """ the index of this web """
    #import pdb
    #pdb.set_trace()
    riceroom_lists = RiceRoom.objects.filter(is_open=1)
    rice_lists = Rice.objects.filter(is_sell=1)
    group_lists = Group.objects.filter(headman=request.user.member.pk)
    extra_context = {
                     'riceroom_lists': riceroom_lists,
                     'rice_lists': rice_lists,
                     'group_lists': group_lists,
                    }
    return render_to_response('rice/index.html', extra_context, 
                        context_instance=RequestContext(request))



