import time
import random

from django.utils.translation import ugettext_lazy as _
from django.db import models

from rice_rice.models import RiceRoom
# Create your models here.
def create_orderid():
    """create 8 bit number for order """
    code1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    code2 = ['1', '2' , '3', '4', '5', '6', '7', '8', '9']
    lenth = 0
    orders = []
    while lenth < 8:
        s = random.choice(code1)
        orders.append(s)
        lenth += 1
    if orders[0] == '0':
        orders[0] = random.choice(code2)
    if orders[7] == '0':
        orders[7] == random.choice(code2)
    return ''.join(orders)


status_CHOICES = (
                    ('0', _( 'ready')),
                    ('1', _('ok')),
                 )

class Order(models.Model):
    """ the rice order """
    order_id = models.CharField(max_length=10, db_index=True, blank=True, null=True, verbose_name='order id')
    rice_id = models.CharField(max_length=10, blank=True, null=True, verbose_name='rice id')
    member_id = models.CharField(max_length=10, blank=True, null=True, verbose_name='member id')
    c_time = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_num = models.IntegerField('nums', default=1)
    status = models.CharField(max_length=5, blank=True, null=True, default='0', choices=status_CHOICES, verbose_name='order status')


    def __unicode_(self):
        return self.order_id


    class Meta:
        ordering = ['c_time']

    @classmethod
    def create_order(cls, rice_id, member_id, **kwargs):
        """ create one order """
        from decimal import Decimal
        if rice_id and member_id:
            while 1:
                order_id = create_orderid()
                try:
                    cls.objects.get(order_id=order_id)
                except:
                    break
                else:
                    continue

            od = cls.objects.create(order_id=order_id, rice_id=rice_id, member_id=member_id)
            order_num = kwargs.get('order_num', 1)
            od.order_num = order_num
            price = Decimal(kwargs.get('price', 0)) * order_num
            od.price = price
            od.status = '1'
            od.save()
            return od
        else:
            raise ValueError('you should give one rice_id and member_id')
    
    @classmethod
    def remove_order(cls, order_id):
        """ delete the order """
        if order_id:
            cls.objects.get(order_id=order_id).delete()
            return True
        else:
            raise ValueError('you should give one order_id')


    @classmethod
    def get_member_order(cls, member_id):
        """ you can get orders from the same member """
        if member_id:
            orders = cls.objects.filter(member_id=int(member_id))
            return orders
        else:
            raise ValueError('you should give one member_id')

    @classmethod
    def get_rice_order(cls, rice_id):
        """ you can get orders from the same rice """
        if rice_id:
            orders = cls.objects.filter(rice_id=int(rice_id))
            return orders
        else:
            raise ValueError('you should give one rice_id')

    @classmethod
    def get_room_order(cls, room_id):
        """ you can get orders from the same room """
        if room_id:
            try:
                room = RiceRoom.objects.get(pk=int(room_id))
            except RiceRoom.DoesNotExist:
                raise ValueError('the riceroom does not exist')
            else:
                rice_list = [ r.pk for r in room.rice_set.all()]
                orders = cls.objects.filter(rice_id__in=rice_list)
                return orders
        else:
            raise ValueError('you should give one room_id')
    

        
