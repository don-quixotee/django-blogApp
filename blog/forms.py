from django import forms
from blog.models import Post, Comment
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
from froala_editor.widgets import FroalaEditor





class contactUsForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.RegexField(regex="^[6-9]\d{9}$")
    message = forms.Textarea()

    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data.get('email') or (cleaned_data.get('phone_number'))):
            raise forms.ValidationError("please enter either email or phone number !", code="invalid")

    def clean_email(self):
        data = self.cleaned_data['email']
        if "edyoda" not in data:
            raise forms.ValidationError("Invalied domain !", code="Invalid")
        return data
    


class RegisterForm(forms.Form):
    GENDER_CHOICES = [("M", "Male"), ("F", "Female")]
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=32, min_length=8, widget = forms.PasswordInput)
    confirm_password = forms.CharField(max_length=32, min_length=8, widget = forms.PasswordInput)
    gender = forms.ChoiceField(choices = GENDER_CHOICES, widget = forms.RadioSelect)
    
    def clean(self):
        cleaned_data = super().clean()
        if  cleaned_data.get('password ') !=  cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Password  not matching !", code="invalid")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','status','category','image']
        widgets = {
            'title': forms.Textarea(attrs={'class': 'post-title-input', 'placeholder': 'Title'}),
            'content': FroalaEditor(),
            
        }
        





    def clean_title(self):
        title = self.cleaned_data.get('title')
        slug = slugify(title)
        try:
          post_obj = Post.objects.get(slug=slug)
          raise forms.ValidationError("title already exist")
        except ObjectDoesNotExist:
            return title


            


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('content',)
        widgets = {
                'content': forms.Textarea(attrs={'class': 'comment-input', 'placeholder': 'response'}),
                
            }
class SearchForm(forms.Form):
    query = forms.CharField()