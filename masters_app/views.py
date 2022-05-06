from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import Cast

from .models import Post, Player
from users.models import Scores, ESPN

def home(request):
    context ={
        'posts': Post.objects.all()
    }
    return render(request, 'masters_app/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'masters_app/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10
    
    def get_context_data(self,**kwargs):
        context = super(PostListView,self).get_context_data(**kwargs)
        context['player']=Player.objects.all().order_by("odds_points")
        return context

class UserPostListView(ListView):
    model = Post
    template_name = 'masters_app/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView, DetailView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    player = Player.objects.all().order_by("odds_points")
    print(f"player is {player}")
    return render(request, 'masters_app/about.html', {"player": player})

def stats(request):
    scores = Scores.objects.all().order_by("score").values()
    espn = ESPN.objects.all().order_by("row_num").values()
    context = {"scores": scores, "espn": espn}
    return render(request, 'masters_app/stats.html', context)

