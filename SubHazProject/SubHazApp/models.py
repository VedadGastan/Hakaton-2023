from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from phonenumber_field.modelfields import PhoneNumberField
from phone_field import PhoneField

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

AUTHENTICATION = (
    (0, "Not Authenticated"),
    (1, "Authenticated")
)

class Category(models.Model): 
    name = models.CharField(max_length=255, default="Uncategorised")
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='static/featured_image/')
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    updated_on = models.DateTimeField(auto_now= True)
    content = tinymce_models.HTMLField()
    excerpt = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class Profile(models.Model):
    image = models.ImageField(upload_to='media/profile_image/')
    image_id = models.ImageField(upload_to='media/profile_id_image/')
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone_number = PhoneField(null=False, blank=False, unique=True)
    address = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    rate_range = models.CharField(max_length=200)
    status = models.IntegerField(choices=AUTHENTICATION, default=0)
    def __str__(self):
        return self.user.username
        

class Unavailability(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    busy_from = models.DateField()
    busy_until = models.DateField()

    def __str__(self):
        return self.profile.first_name + " " + self.profile.first_name
