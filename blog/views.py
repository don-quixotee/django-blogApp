from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib import auth
from django.views import View
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView, FormView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Category, Comment, BookmarkPost
from .forms import contactUsForm, RegisterForm, PostForm, CommentForm, SearchForm
from account.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth.decorators import login_required


# Create your views here.




class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/stories.html'
    form_class = SearchForm

    def get(self,request, id=None):
        posts = Post.objects.filter(status='P')
        category = Category.objects.all()


        
        if id:
            cat = Category.objects.get(id=id)
            posts = Post.objects.filter(category=cat)
        context = {'posts':posts,'category':category}
        return render(request,"blog/stories.html",context)
    




 


class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    form_class = CommentForm
    template_name = 'blog/blog-post.html'
    login_url = 'login'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'slug':self.object.slug})  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        post = self.get_object()
        comment = Comment.objects.filter(post=post)
        context['comment_form'] = comment

        
        return context
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            
            post = self.get_object()
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.author = self.request.user
            new_comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self, form):
        return super().form_valid(form)

@login_required
def contact_us_form_view(request):
    if request.method == "GET":
        form = contactUsForm()
        return render(request, 'blog/contact-us.html', context={'form':form,})
    else:

        form = contactUsForm(request.POST)
        if form.is_valid():
            return render(request, 'blog/success.html', {})
        else:
            return render(request, 'blog/contact-us.html', context={'form':form,})


class PostCreateView( LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required='blog.add_post'
    model = Post
    form_class = PostForm
    template_name = "blog/post.html"
    success_url = "/"
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
   



class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = 'blog.change_post'
    model = Post
    fields = ['title','content','status','category','image']
    template_name = "blog/update.html"
    pk_url_kwarg = 'id'

    success_url = "/"
    login_url = 'login'

    def test_func(self, *args, **kwargs):
        post=Post.objects.get(slug=self.kwargs.get('slug'))
        if post.author == self.request.user:
            return True
        else:
            return False



class PostDeleteView( LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    permission_required = 'blog.change_post'
    model = Post
    template_name = 'blog/delete.html' 
 
    success_url = reverse_lazy('home')
    login_url = reverse_lazy("login")

    def test_func(self, *args, **kwargs):
        post=Post.objects.get(slug=self.kwargs.get('slug'))
        if post.author == self.request.user:
            return True
        else:
            return False



class profileDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name ='blog_user'
    template_name = 'blog/userprofile.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        blog_user = self.get_object()

        posts = Post.objects.filter(author=blog_user)
        context['posts']=posts
        return context
        



@login_required    
def SearchListView(request):
    form = SearchForm()
    query = None
    results = []
    category = Category.objects.all()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title',weight='A')+SearchVector('content', weight='B')
            search_query =SearchQuery(query)
            posts = Post.publish.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.5).order_by('-rank')
            return render(request, 'blog/stories.html', context={'form':form,'query':query, 'posts':posts , 'category':category})


    else:

        next = request.POST.get('next', '/')
        HttpResponseRedirect(next)





class BookmarkView(LoginRequiredMixin, ListView):
    login_url ='login'
    model = BookmarkPost
    template_name = 'blog/bookmark.html'
    context_object_name ='posts'


    def get_success_url(self):
        return reverse_lazy('bookmark')  

        
    def get(self, request, pk=None):
        if pk: 
            user = auth.get_user(request)
            bookmark, created = self.model.objects.get_or_create(user=user, obj_id=pk)
            bookmark.user = user
            if not created:
                bookmark.delete()
            bookmark.save()

            user = self.request.user
            user_id = user.id
            posts =  BookmarkPost.objects.filter(user=user_id) 
            return render(request, 'blog/bookmark.html',{'posts':posts})
        
   


        user = self.request.user
        user_id = user.id
        posts =  BookmarkPost.objects.filter(user=user_id)    


        return render(request, 'blog/bookmark.html',{'posts':posts})
        
@login_required    
def  CommentDeleteView(request, id):
    if id:
        comment = Comment.objects.get(id=id)
        comment.delete()
        return redirect('/')

@login_required
def bookmarkDeleteView(request, id):
    if id:
        bookmark = BookmarkPost.objects.get(id=id)
        bookmark.delete()
        return redirect('bookmark')
