from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from django.urls import reverse
from django.views import generic
# Create your views here.
from groups.models import Group, GroupMember


class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields=('name','description')
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except:
            messages.warning(self.request,'Already a member')
        else:
            messages.success(self.request,'You are now a member')
        return super().get(*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,*args,**kwargs):

        try:
            membership = GroupMember.objects.filter(
            user=self.request.user,
            group__slug=self.kwargs.get('slug')
            ).get()

        except:
            messages.warning(self.request,'Sorry! You are not in this group.')
            print('What the fuckk')
        else:
            membership.delete()
            messages.success(self.request,'You left the group.')
        return super().get(*args,**kwargs)
