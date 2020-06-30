from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from froala_editor.fields import FroalaField
from django.contrib.auth import get_user_model

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    def __str__(self):
        return self.name
    
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='P')
    

class Post(models.Model):
    objects = models.Manager()
    publish = PublishedManager()
    STATUS = [('D',"Draft"), ("P","published")]


    title = models.CharField(max_length=250)
    content = FroalaField()
    
    status = models.CharField(max_length = 50, choices=STATUS, default='D')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogs/', blank=True,)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    published = models.DateTimeField(auto_now_add=True)


    def all_comments(self):
        return self.comments.all().order_by('-created_date')


  

        
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)


    def __str__(self):
        return self.title
    
  
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post-detail", args=[self.slug])



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})
    def __str__(self):
        return self.content


    

class BookmarkBase(models.Model):
    class Meta:
        abstract = True
 
    user = models.ForeignKey(get_user_model(), verbose_name="User", on_delete=models.CASCADE)
 
    def __str__(self):
        return self.user.username



class BookmarkPost(BookmarkBase): 
    obj = models.ForeignKey(Post, verbose_name="Post", on_delete=models.CASCADE)
    def __str__(self):
        return self.obj.title
    
# class LikePost(BookmarkBase): 
#     obj = models.ForeignKey(Post, verbose_name="Post", on_delete=models.CASCADE)
#     def __str__(self):
#         return self.obj.title
 

