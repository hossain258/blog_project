from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured


class Tag(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)   # when created, 
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    


class Content(models.Model): 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # user --> content (one to many)
    title = models.CharField(max_length=150)
    text = models.TextField()
    tags = models.ManyToManyField("Tag")
    
    """
    Content Tag
    1        2
    1        3
    2        4
    5        4
    3        2
    """    
    date_created = models.DateTimeField(auto_now_add=True)   # when created, 
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def validate_date_created(self):
        date_created = self.date_created
        last_updated = self.last_updated
        print("Inside Validate date_created")
        if (not date_created) and (not last_updated):
            return None

        if date_created > last_updated:
            raise ImproperlyConfigured("Date created cannot be more than last_updated")
        print("Done")
        return True

    def validate_text(self):
        text = self.text
        if "django" not in text:
            raise ImproperlyConfigured("You should write about django")

        return True

    def validate_unique_user_and_title(self):
        """
        Safwan -> hello

        """

    def save(self, *args, **kwargs):
        self.validate_date_created()
        return super().save(*args, **kwargs)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # models.OneToOneRel
    phone = models.CharField(max_length=15)    
    address_1 = models.TextField()
    address_2 = models.TextField()

    def __str__(self):
        return self.user.username
