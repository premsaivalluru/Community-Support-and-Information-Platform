from django.db import models
from django.contrib.auth.models import User as AuthUser
# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50, default='')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(unique=True,max_length=13)
    profession = models.CharField(max_length=50, default = 'Student')
    password = models.CharField(max_length=128,default='12345678')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length = 30, default='Vizianagaram')
    photo = models.ImageField(upload_to = 'images', default = 'images/profile.jpg')
    
    def __str__(self):
        return self.username
    
class Phone(models.Model):
    phone = models.CharField(max_length=13, unique=True)
    created_at= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.phone
    
class Volunteer(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name="volunteer_profile", null=True, blank=True)
    username = models.CharField(max_length=50, default='')
    first_name = models.CharField(max_length=50,default='')
    last_name = models.CharField(max_length=50, default='')
    phone_number = models.CharField(unique=True, max_length=13, default='')
    profession = models.CharField(max_length=50, default='Student')
    address = models.CharField(max_length=30, default='Vizianagaram')
    photo = models.ImageField(upload_to='images', default='images/profile.jpg')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username if self.user else self.username


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts",null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    author_name = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    event_date = models.DateTimeField(default=None)
    status = models.CharField(max_length=20, default="pending")
    author_phone_number = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_phones")
    verified_by = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name="verified_posts", null=True, blank=True)
    notified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
class Feedback(models.Model):
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    feedback = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    author_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.author_name
    
class Contact(models.Model):
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=13)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class VolunteerMessage(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name="messages")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="volunteer_messages")
    message_sid = models.CharField(max_length=100)
    status = models.CharField(max_length=30, default="sent")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.volunteer and self.volunteer.user:
            return self.volunteer.user.username
        return f"VolunteerMessages {self.id}"

class PostVerification(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="verification")
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name="post_verifications")
    status = models.CharField(max_length=10, choices=[('true', 'True'),('false', 'False')])
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'volunteer')