from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, FileResponse
from django.conf import settings
from .models import (
    HeroSection, About, Project, Service, TimelineEvent,
    Skill, ContactInfo, ContactMessage, SocialLink
)
import os

# ---------------- Home Page ----------------
def home(request):
    hero = HeroSection.objects.filter(is_active=True).first()
    skills = Skill.objects.all()
    timeline = TimelineEvent.objects.all()
    projects = Project.objects.all()[:6]  # show first 6
    services = Service.objects.all()
    context = {
        "hero": hero,
        "skills": skills,
        "timeline": timeline,
        "projects": projects,
        "services": services,
    }
    return render(request, "core/home.html", context)


# ---------------- About Page ----------------
def about(request):
    about_info = About.objects.first()
    skills = Skill.objects.all()
    timeline = TimelineEvent.objects.all()
    context = {
        "about_info": about_info,
        "skills": skills,
        "timeline": timeline,
    }
    return render(request, "core/about.html", context)


# ---------------- Projects List ----------------
def projects(request):
    projects_list = Project.objects.all()
    context = {"projects": projects_list}
    return render(request, "core/projects.html", context)


# ---------------- Project Detail ----------------
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    context = {"project": project}
    return render(request, "core/project_detail.html", context)


# ---------------- Services ----------------
def services(request):
    services_list = Service.objects.all()
    context = {"services": services_list}
    return render(request, "core/services.html", context)


# ---------------- Contact ----------------
def contact_view(request):
    contact_info = ContactInfo.objects.first()
    context = {"contact_info": contact_info}
    return render(request, "core/contact.html", context)


# ---------------- Contact AJAX ----------------
def contact_ajax(request):
    if request.method == "POST" and request.is_ajax():
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        ContactMessage.objects.create(name=name, email=email, message=message)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


# ---------------- Download CV ----------------
def download_cv(request):
    about_info = About.objects.first()
    if not about_info or not about_info.cv:
        return HttpResponse("CV not available", status=404)

    # ---------------- Cloudinary ----------------
    if hasattr(about_info.cv, 'url'):
        return redirect(about_info.cv.url)

    # ---------------- Local ----------------
    file_path = os.path.join(settings.MEDIA_ROOT, about_info.cv.name)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response

    return HttpResponse("CV not found", status=404)


# ---------------- Base Context for Templates ----------------
def base_context(request):
    """
    Add global context variables accessible in all templates.
    """
    social_links = SocialLink.objects.all()
    contact_info = ContactInfo.objects.first()
    return {
        "social_links": social_links,
        "contact_info": contact_info,
    }
