# Create your views here.
import json

from django.http import HttpResponse
from rice_order.models import Order


def buy_rice(request):
    if request.REQUEST.get('rice_id', ''):
        rice_id = int(request.REQUEST.get('rice_id'))
        user = request.user
        result = Order.create_order(rice_id, user.member.id)
        if result:
            data = {'result': 1}
        else:
            data = {'result': 0}
        return HttpResponse(json.dumps(data))
