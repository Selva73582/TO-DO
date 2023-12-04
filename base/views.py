from django.shortcuts import render,redirect

from django.http import HttpResponse

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.views import LogoutView


from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from . import models


class TaskList(LoginRequiredMixin,ListView):
    model=models.Task
    context_object_name='tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(is_completed=False).count()

        search_input=self.request.GET.get('search-area') or ''

        if search_input:
            context['tasks']=context['tasks'].filter(title__istartswith=search_input)

        context['search_area']=search_input
        return context


class TaskDetail(LoginRequiredMixin,DetailView):
    model=models.Task

    context_object_name='task'

    template_name='base/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model=models.Task
    fields = ['title', 'description', 'is_completed']
    template_name='base/task_form.html'
    success_url = reverse_lazy('TaskList')


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=models.Task
    fields='__all__'
    success_url = reverse_lazy('TaskList')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=models.Task
    context_object_name='task'
    success_url = reverse_lazy('TaskList')



class CustomLogin(LoginView):
    model=models.Task
    fields='__all__'
    template_name='base/login.html'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('TaskList')
    

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('TaskList')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('TaskList')
        return super(RegisterPage, self).get(*args, **kwargs)
    

    def get_success_url(self):
        return reverse_lazy('TaskList')
    
