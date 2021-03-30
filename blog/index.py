from django.shortcuts import render, redirect
from . import models
from django.views.generic.list import ListView
from .form import CommentForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.contrib.auth.models import User


def about(request):
    return render(request, 'blog/about.html')


class postListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    template_name = 'blog/home.html'
    paginate_by = 2
    ordering = '-date'


class userPostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    template_name = 'blog/user_post.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(userPostListView, self).get_context_data()
        if 'username' in self.kwargs:
            context['username'] = self.kwargs['username']
        return context

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs['username'])
        return models.Post.objects.filter(author=user).order_by('-date')


def postDetailView(request, **kwargs):
    @login_required
    def postComment(req, **kw):
        cmt = CommentForm(request.POST)
        if cmt.is_valid():
            cmt.instance = Comment(post=Post.objects.get(pk=kw['pk']), user=req.user)
            cmt.save()
        return redirect('Post', pk=kwargs['pk'])

    if request.method == 'POST':
        return postComment(request, **kwargs)
    else:
        form = CommentForm()
        post = Post.objects.get(pk=kwargs['pk'])
        comments = Comment.objects.filter(post=post)
        return render(request, 'blog/post.html', context={'form': form, 'object': post, 'comments': comments})


class postCreateView(LoginRequiredMixin, CreateView):
    model = models.Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.save()
        self.success_url = '/post/{}'.format(form.instance.pk)
        return super().form_valid(form)


class postUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']

    def get_object(self, **kwargs):
        return models.Post.objects.get(pk=self.kwargs['pk'])

    def test_func(self):
        return self.get_object().author.pk == self.request.user.pk

    def form_valid(self, form):
        form.instance.save()
        self.success_url = '/post/{}'.format(form.instance.pk)
        return super().form_valid(form)


class postDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Post

    def get_success_url(self):
        return reverse('Home')

    def get_object(self, **kwargs):
        return models.Post.objects.get(pk=self.kwargs['pk'])

    def test_func(self):
        return self.get_object().author.pk == self.request.user.pk
