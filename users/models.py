
# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Extended User model with additional matrimony-specific fields"""
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    USER_TYPE_CHOICES = (
        ('regular', 'Regular'),
        ('premium', 'Premium'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='regular')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'gender']
    
    def __str__(self):
        return self.email

    def age(self):
        from datetime import date
        today = date.today()
        born = self.date_of_birth
        if born:
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return None

# profiles/models.py
from django.db import models
from django.conf import settings

class Profile(models.Model):
    """Detailed matrimony profile information"""
    MARITAL_STATUS_CHOICES = (
        ('never_married', 'Never Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('awaiting_divorce', 'Awaiting Divorce'),
    )
    
    RELIGION_CHOICES = (
        ('hindu', 'Hindu'),
        ('muslim', 'Muslim'),
        ('christian', 'Christian'),
        ('sikh', 'Sikh'),
        ('buddhist', 'Buddhist'),
        ('jain', 'Jain'),
        ('parsi', 'Parsi'),
        ('jewish', 'Jewish'),
        ('other', 'Other'),
    )
    
    EDUCATION_LEVEL_CHOICES = (
        ('high_school', 'High School'),
        ('bachelors', 'Bachelor\'s Degree'),
        ('masters', 'Master\'s Degree'),
        ('doctorate', 'Doctorate'),
        ('other', 'Other'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # in cm
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # in kg
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES)
    mother_tongue = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    # Location details
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    
    # Education and Career
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES)
    education_details = models.TextField(blank=True, null=True)
    occupation = models.CharField(max_length=100)
    income_range = models.CharField(max_length=100, blank=True, null=True)
    
    # Family details
    family_type = models.CharField(max_length=50, blank=True, null=True)  # Joint/Nuclear
    family_values = models.CharField(max_length=50, blank=True, null=True)  # Traditional/Liberal/Moderate
    about_family = models.TextField(blank=True, null=True)
    
    # Lifestyle
    diet = models.CharField(max_length=50, blank=True, null=True)  # Veg/Non-veg/Occasionally Non-veg
    smoking = models.CharField(max_length=50, blank=True, null=True)  # Yes/No/Occasionally
    drinking = models.CharField(max_length=50, blank=True, null=True)  # Yes/No/Occasionally
    
    # Hobbies and interests
    hobbies = models.TextField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email}'s Profile"

class Photo(models.Model):
    """Additional photos for a profile"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='profile_photos/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo for {self.profile.user.email}"

# matching/models.py
from django.db import models
from django.conf import settings

class PartnerPreference(models.Model):
    """Partner preferences for matching"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partner_preference')
    
    # Age preferences
    min_age = models.IntegerField(default=18)
    max_age = models.IntegerField(default=50)
    
    # Height preferences
    min_height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # in cm
    max_height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # in cm
    
    # Location preferences
    preferred_countries = models.TextField(blank=True, null=True)  # Comma-separated countries
    preferred_states = models.TextField(blank=True, null=True)  # Comma-separated states
    preferred_cities = models.TextField(blank=True, null=True)  # Comma-separated cities
    
    # Background preferences
    preferred_religions = models.TextField(blank=True, null=True)  # Comma-separated religions
    preferred_mother_tongues = models.TextField(blank=True, null=True)  # Comma-separated languages
    preferred_marital_status = models.TextField(blank=True, null=True)  # Comma-separated marital statuses
    
    # Education and Career preferences
    preferred_education_levels = models.TextField(blank=True, null=True)  # Comma-separated education levels
    preferred_occupations = models.TextField(blank=True, null=True)  # Comma-separated occupations
    preferred_income_range = models.CharField(max_length=100, blank=True, null=True)
    
    # Lifestyle preferences
    preferred_diet = models.TextField(blank=True, null=True)  # Comma-separated diets
    preferred_smoking = models.TextField(blank=True, null=True)  # Comma-separated smoking habits
    preferred_drinking = models.TextField(blank=True, null=True)  # Comma-separated drinking habits
    
    # Additional preferences
    about_partner = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email}'s Partner Preference"

class Match(models.Model):
    """Records matches between users"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )
    
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_matches')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_matches')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('sender', 'receiver')
    
    def __str__(self):
        return f"Match between {self.sender.email} and {self.receiver.email}"

# messaging/models.py
from django.db import models
from django.conf import settings

class Conversation(models.Model):
    """Conversation between two users"""
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    started_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    """Individual message in a conversation"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    attachment = models.FileField(upload_to='message_attachments/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message from {self.sender.email} at {self.created_at}"