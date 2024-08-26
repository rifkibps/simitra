from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):

    theme_dark = (
       ('0', 'true'),
       ('1', 'false')
    )
        
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    theme = models.CharField(max_length=1, choices=theme_dark, default='1', null=False, blank=False, verbose_name='User Theme Dark Mode' )
    theme_condense = models.CharField(max_length=1, choices=theme_dark, default='1', null=False, blank=False, verbose_name='User Theme Left Side Condense' )
    
    def __str__(self):
        return f'{self.user.username} Profile' #show how we want it to be displayed

    def save(self):
        super().save()

        img = Image.open(self.image.path) # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path) # Save it again and override the larger image

# Create your models here.
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)