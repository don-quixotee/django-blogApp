from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from account.forms import SignUpForm, UserProfileForm
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin




# Create your models here.

class SignUpView(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")




@login_required
def  userAccountView(request):

    user = request.user
    context={"user":user}
  
    print(user.id)
    return render(request, 'account/account.html', context)

# class  userAccountView(TemplateView):

#     model= User
#     tempate_name = 'account/profile.html'
#     def get(self, request, id=None
#     ):
#         user = User.objects.get(id=id)
#         post=Post.objects.filter(post=user)
#         return render(request, 'account/profile.html', context={'user':user, 'post':post})        




class userUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'account/updateprofile.html'
    pk_url_kwarg = 'id'
    form_class = UserProfileForm
    # success_url =  reverse_lazy('profile')
    login_url = 'account/login'























