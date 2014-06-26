import datetime

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
# Create your models here.
SEX_CHOICES = (
                ('M', _('boy')),
                ('W', _('girl')),
              )

ACTION_CHOICES = (
                    ('A', 'apply'),
                    ('R', 'accept'),
                    ('D', 'decline'),
                )

class Group(models.Model):
    """ the group class """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='the_group_name')
    c_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    headman = models.IntegerField(max_length=10, blank=True, null=True)

   
    def __unicode__(self):
        return self.name
        get_lastest_by = c_time

    class Meta:
        ordering = ['c_time']

    @classmethod
    def create_group(cls, m_obj, name, description=''):
        """ create group by m_obj"""
        g = cls.objects.create(name=name, description=description)
        g.member_set.add(m_obj)
        g.headman = m_obj.pk
        g.save()
        return g

    @classmethod
    def remove_group(cls, m_id=0, g_id=0):
        """ delete group by m_obj"""
        if g_id and m_id:
            try:
                g = cls.objects.get(pk=int(g_id))
            except cls.DoesNotExist:
                raise ValueError('group has not exists')
            else:
                if m_id is g.headman:
                    g.delete()
        else:
            raise ValueError('group id or m_id cannot be null')
 

class Member(models.Model):
    """ the member model for database table member"""
    user = models.OneToOneField(User,verbose_name='user_id')
    name = models.CharField(max_length=30, blank=True, null=True, verbose_name='name')
    telephone = models.CharField(max_length=11, blank=True, null=True,  db_index=True, verbose_name='tele')
    sex = models.CharField(max_length=5, blank=True, null=True, default='M', choices=SEX_CHOICES, verbose_name='sex')
    address = models.CharField(max_length=50, blank=True, null=True, verbose_name='address')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    group = models.ManyToManyField(Group, db_table='mtog')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['create_time']
        get_latest_by = 'create_time'

    @classmethod
    def create_member(cls, username, password, email, **kwargs):
        """ create member """
        if not User.objects.filter(Q(username=username)|Q(email=email)).exists():
            user = User.objects.create_user(username=username, password=password, email=email)
            m = cls(user=user)
            m.name = kwargs.get('name', '')
            m.telephone = kwargs.get('telephone', '')
            m.sex = kwargs.get('sex', 'M')
            m.address = kwargs.get('address', '')
            m.save()
            return m
        else:
            raise ValueError('this username or email has exists !') 
    
    @classmethod         
    def remove_member(cls, username):
        if username:
            try:
                u = User.objects.get(username=username)
                cls.objects.get(user=u).delete()
                u.delete()
                return True
            except User.DoesNotExist:
                raise ValueError('username has not exists')
            except cls.DoesNotExist:
                u.delete()
                return True
        else:
            raise ValueError('username cannot be null')
    
    
    @classmethod
    def push_member(cls, g_id, ms_id, mc_id):
        """ add member to group """
        if g_id and ms_id and mc_id:
            try:
                g = Group.objects.get(pk=int(g_id))
                ids = tuple(g.member_set.all().values('id'))
                if int(ms_id) == g.headman and int(mc_id) not in ids:
                    mems_o = cls.objects.get(pk=int(mc_id))
                else:
                    raise ValueError('you has no permmions')
            except Group.DoesNotExist:
                raise ValueError('Group has not exists')
            except cls.DoesNotExist:
                raise ValueError('Member has not exists')
            else:
                g.member_set.add(mems_o)
                return True
        else:
            raise ValueError('g_id,ms_id or mc_id cannot be null')


    @classmethod
    def pull_member(cls, g_id, ms_id, mc_id):
        """ del member from group """
        if g_id and ms_id and mc_id:
            try:
                g = Group.objects.get(pk=int(g_id))
                ids = list(g.member_set.all().values('id'))
                if int(ms_id) == g.headman and int(mc_id) not in ids:
                    mems_o = cls.objects.get(pk=int(mc_id))
                else:
                    raise ValueError('you has no perssions')
            except Group.DoesNotExist:
                raise ValueError('group has not exists')
            except cls.DoesNotExist:
                raise ValueError('Member has not exists')
            else:
                g.member_set.remove(mems_o)
                return True
        else:
            raise ValueError('g_id or m_id cannot be null')

    @classmethod
    def quit_group(cls, g_id, mc_id):
        """quit the group for member """
        if g_id and mc_id:
            try:
                g = Group.objects.get(pk=int(g_id))
                m = Member.objects.get(pk=int(mc_id))
            except Group.DoesNotExist:
                raise ValueError('the group do not exist')
            except Member.DoesNotExist:
                raise ValueError('the member do not exist')
            else:
                g.member_set.remove(m)
                return True
        else:
            raise ValueError('g_id or m_id cannot be null')


class GroupRequestAct(models.Model):
    """ the member can apply to join in a group and group 
        can allow or not to the member to be
    """
    member_id = models.IntegerField('member_id', default=0, db_index=True)
    group_id = models.IntegerField('group_id', default=0, db_index=True)
    action = models.CharField(max_length=10, blank=True, null=True, choices=ACTION_CHOICES, verbose_name='request action')
    r_time = models.DateTimeField(auto_now_add=True)
    a_time = models.DateTimeField(default=datetime.datetime(2000,1,1,0,0,0))
    
    def __unicode__(self):
        return self.member_id

    @classmethod
    def create_act(cls, member_id, group_id):
        """ member apply to join the group """
        if member_id and group_id:
            result = cls.objects.filter(member_id=int(member_id), group_id=int(group_id))
            if result.exists():
                if result[0].action == 'R':
                    return True
                if result[0].action == 'A':
                    return True
                if result[0].action == 'D':
                    result.update(action='R')
            else:
                cls.objects.create(member_id=int(member_id), group_id=int(group_id), action='R')
                return True
        else:
            raise ValueError("member_id and group_id can not be null")

    @classmethod
    def accept_act(cls, member_id, group_id, ms_id):
        """ group act the apply for member to join the group """
        if member_id and group_id:
            result = cls.objects.filter(member_id=int(member_id), group_id=int(group_id))
            result.update(action='A')
            Member.push_member(int(group_id), int(ms_id), int(member_id))
            print '1111'
            return True
        else:
            raise ValueError("member_id and group_id can not be null") 





    
