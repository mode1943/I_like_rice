# Create your views here.
import json

from django.http import HttpResponse
from rice_order.models import Order


def buy_rice(request):
    rice_id = group_id = 0
    if request.REQUEST.get('rice_id', 0):
        rice_id = int(request.REQUEST.get('rice_id'))
    if request.REQUEST.get('group_id', 0):
        group_id = int(request.REQUEST.get('group_id'))
    user = request.user
    result = Order.create_order(rice_id, user.member.id, sub_to=group_id)
    if result:
        data = {'result': 1}
    else:
        data = {'result': 0}
    return HttpResponse(json.dumps(data))

