from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from phonenumber_field.modelfields import PhoneNumberField
from phone_field import PhoneField

AUTHENTICATION = (
    (0, "Not Authenticated"),
    (1, "Authenticated")
)

CHOICE = (
    (0, "No"),
    (1, "Yes")
)

class Profile(models.Model):
    image = models.ImageField(upload_to='media/profile_image/')
    image_id = models.ImageField(upload_to='media/profile_id_image/')
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone_number = PhoneField(null=False, blank=False, unique=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    charge_rate = models.CharField(max_length=200)
    status = models.IntegerField(choices=AUTHENTICATION, default=0)
    description = models.TextField(max_length=1000)
    setac = models.IntegerField(choices=CHOICE,default=0)
    cuvar = models.IntegerField(choices=CHOICE,default=0)
    trener = models.IntegerField(choices=CHOICE,default=0)
    def __str__(self):
        return self.user.username
