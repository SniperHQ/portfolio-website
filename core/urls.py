from django.urls import path
from .views import home, about, projects, project_detail, services, contact_view, contact_ajax, download_cv

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("projects/", projects, name="projects"),
    path("projects/<int:pk>/", project_detail, name="project_detail"),
    path("services/", services, name="services"),
    path("contact/", contact_view, name="contact"),
    path("contact-ajax/", contact_ajax, name="contact_ajax"),
    path("download-cv/", download_cv, name="download_cv"),
]
