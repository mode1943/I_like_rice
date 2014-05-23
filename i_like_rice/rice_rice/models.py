from datetime import datetime
from time import time
from PIL import Image

from django.utils.translation import ugettext_lazy as _
from django.db import models

# Create your models here.

rice_CHOICES = (
                ('1', _('rice with meat and vegetables')),
                ('2', _('pasta')),
                ('3', _('a fried dish')),
                ('4', _('drink')),
                ('5', _('rice flour')),
                )

priority_CHOICES = (
                    ('A', _('five rice')),
                    ('B', _('four rice')),
                    ('C', _('three rice')),
                    ('D', _('two rice')),
                    ('E', _('zero rice')),
                    )

class RiceRoom(models.Model):
    """ define the restaurant"""
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='restanrant')
    telephone = models.CharField(max_length=15, blank=True, null=True, verbose_name='tel')
    priority = models.CharField(max_length=5, default='E', choices=priority_CHOICES, verbose_name='the ranking')
    is_open = models.IntegerField(max_length=1, default=1, verbose_name='wether on the bussiness')
    c_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name


    class Meta:
        ordering = ['c_time']

    
    @classmethod
    def create_riceroom(cls, name, telephone):
        """create rice room """
        rm = cls.objects.create(name=name, telephone=telephone)
        return rm


    @classmethod
    def remove_riceroom(cls, rm_id):
        """delete rice room """
        cls.objects.get(pk=int(rm_id)).delete()
        return True


class Rice(models.Model) :
    """define the cookbook """
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name='dish' )
    price = models.DecimalField(max_digits=8, decimal_places=3, default=0.00, verbose_name='price')
    rice_type = models.CharField(max_length=5, default='1', choices=rice_CHOICES, verbose_name='rice_type')
    riceroom = models.ForeignKey(RiceRoom, null=True)
    description = models.CharField(max_length=100, blank=True, null=True, verbose_name='desc')
    total_rices = models.IntegerField(max_length=10, blank=True, null=True, default=100, verbose_name='total_nums')
    current_rices = models.IntegerField(max_length=10, blank=True, null=True, default=0, verbose_name='current_nums')
    is_sell = models.CharField(max_length=1, default='1')
    c_time = models.DateField(auto_now_add=True)
    

    def __unicode__(self):
        return self.name

    
    class Meta:
        ordering = ['c_time']


    @classmethod
    def create_rice(cls, name, price, riceroom_id, **kwargs):
        """ add rice dish """
        from decimal import Decimal
        if name and riceroom_id:
            rd = cls.objects.create(name=name, price=Decimal(price), riceroom_id=int(riceroom_id))
            rd.description = kwargs.get('description', '')
            rd.total_rices = kwargs.get('total_rices', 100)
            rd.current_rices = kwargs.get('current_rices', 0)
            rd.save()
            return rd
        else:
            raise ValueError('arguments cannot be null')

    @classmethod
    def remove_rice(cls, r_id):
        """ delete rice dish"""
        if r_id:
            cls.objects.get(pk=int(r_id)).delete()
            return True
        else:
            raise ValueError('you should give me a rice')


class RicePic(models.Model):
    """ define the rice dish picture"""
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name='name')
    rice = models.ForeignKey(Rice)
    path = models.CharField(max_length=100, blank=True, null=True, verbose_name='path')
    c_time = models.DateTimeField(auto_now_add=True)
   

    def __unicode__(self):
        return self.name
    
    @classmethod
    def save_pic(cls, f, rice_id):
        """save the rice picture """
        from django.conf import settings
        import os
        if f is not None and Rice.objects.filter(pk=int(rice_id)).exists():
            s_path = "%s/%s/%s/" %(datetime.now().year, datetime.now().month, datetime.now().day)
            save_path = os.path.join(settings.PHOTO_ROOT, s_path)
            save_name = "%s.jpg" % int(time())
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            url_path = os.path.join(settings.PHOTO_URL, s_path, save_name)
            cls.objects.create(name=os.path.splitext(f.name)[0], path=url_path, rice_id=rice_id)
            img = Image.open(f)
            img.thumbnail((150,210), Image.ANTIALIAS)
            img.save(os.path.join(save_path, save_name), quality=100)
            return True
        else:
            raise ValueError('file not null and the rice has not exist')

    @classmethod
    def delete_pic(cls, pic_id):
        """ delete the picture """
        if pic_id:
            try:
                p = cls.objects.get(pk=int(pic_id))
                p.delete()
                return True
            except RicePic.DoesNotExist:
                raise ValueError('the pic does not exists')
        else:
            raise ValueError('the picture you want to delete cannot be null')
