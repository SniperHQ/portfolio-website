from django.db import models
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField  # <-- for Cloudinary images

# ================= PDF Validator =================
def validate_pdf(file):
    if not file.name.lower().endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")


# ---------------- Hero Section ----------------
class HeroSection(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)  # <-- Cloudinary
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class About(models.Model):
    title = models.CharField(max_length=200, default="About Me")
    description = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)  # <-- Cloudinary

    cv = models.FileField(
        upload_to='cv/',
        blank=True,
        null=True,
        help_text="Upload PDF resume only"
    )

    cv_downloads = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


# ---------------- Skills ----------------
class Skill(models.Model):
    name = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField(help_text="Enter a number 0-100 for skill level")
    icon = CloudinaryField('icon', blank=True, null=True)  # <-- Cloudinary

    def __str__(self):
        return self.name


# ---------------- Timeline / Journey ----------------
class TimelineEvent(models.Model):
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = CloudinaryField('icon', blank=True, null=True)  # <-- Cloudinary
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.year} - {self.title}"


# ---------------- Projects ----------------
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = CloudinaryField('image')  # <-- Cloudinary
    live_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    tech_stack = models.CharField(max_length=255)
    features = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def feature_list(self):
        return self.features.splitlines()

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',')]

    def __str__(self):
        return self.title


# ---------------- Services ----------------
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = CloudinaryField('icon', blank=True, null=True)  # <-- Cloudinary
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


# ---------------- Contact Info ----------------
class ContactInfo(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return "Contact Information"


# ---------------- Contact Messages ----------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


# ---------------- Social Links ----------------
class SocialLink(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    icon = CloudinaryField('icon', blank=True, null=True)  # <-- Cloudinary
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
