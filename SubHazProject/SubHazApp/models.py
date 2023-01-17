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

certificate_types=["CAC", "CSST"]
rate_range = [("$10-$20", "$10-$20"), ("$20-$30", "$20-$30"), ("$30-$40", "$30-$40"), ("$40-$50", "$40-$50"), ("$50+", "$50+")]
profile_types = [("Consultant", "Consultant"), ("Non-Consultant", "Non-Consultant")]

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
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_type = models.CharField(choices=profile_types, max_length=200)
    phone_number = PhoneField(null=False, blank=False, unique=True)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username
        

class Consultant(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    consultant_company = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True, null=True)
    region = models.CharField(max_length=200)
    district = models.CharField(max_length=200, blank=True, null=True)
    rate_range = models.CharField(choices=rate_range, max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200)
    phone_number = PhoneField(null=False, blank=True, unique=False)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=200)
    phone_number = PhoneField(null=True, blank=True, unique=False)
    address = models.CharField(max_length=200, blank=True, null=True)
    auth_consultant = models.ForeignKey('Consultant', on_delete=models.CASCADE, blank=True, null=True)
    FEIN = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class Unavailability(models.Model):
    consultant_Id = models.ForeignKey('Consultant', on_delete=models.CASCADE)
    busy_from = models.DateField()
    busy_until = models.DateField()

    def __str__(self):
        return self.consultant_Id.name

class Certificate(models.Model):
    certificate_type = models.CharField(max_length=200)
    consultant_Id = models.ForeignKey('Consultant', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/certificate_images/', blank=True, null=True)
    expiration_date = models.DateField()
    status = models.IntegerField(choices=AUTHENTICATION, default=0)

    def __str__(self):
        return self.consultant_Id.name + " - " + self.certificate_type + " -> " + str(self.status)
