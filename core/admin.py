from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, FileResponse
from django.conf import settings
from .models import HeroSection, About, Project, Service, TimelineEvent, Skill, ContactInfo, ContactMessage
import os

# ---------------- Home ----------------
def home(request):
    hero = HeroSection.objects.filter(is_active=True).first()
    skills = Skill.objects.all()
    timeline = TimelineEvent.objects.all()
    projects = Project.objects.all()[:6]
    services = Service.objects.all()
    return render(request, "core/home.html", {
        "hero": hero,
        "skills": skills,
        "timeline": timeline,
        "projects": projects,
        "services": services,
    })

# ---------------- About ----------------
def about(request):
    about_info = About.objects.first()
    skills = Skill.objects.all()
    timeline = TimelineEvent.objects.all()
    return render(request, "core/about.html", {
        "about_info": about_info,
        "skills": skills,
        "timeline": timeline,
    })

# ---------------- Projects ----------------
def projects(request):
    projects = Project.objects.all()
    return render(request, "core/projects.html", {"projects": projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "core/project_detail.html", {"project": project})

# ---------------- Services ----------------
def services(request):
    services = Service.objects.all()
    return render(request, "core/services.html", {"services": services})

# ---------------- Contact ----------------
def contact_view(request):
    contact_info = ContactInfo.objects.first()
    return render(request, "core/contact.html", {"contact_info": contact_info})

def contact_ajax(request):
    if request.method == "POST" and request.is_ajax():
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message")
        )
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

# ---------------- Download CV ----------------
def download_cv(request):
    about = About.objects.first()
    if not about or not about.cv:
        return HttpResponse("CV not available", status=404)

    if hasattr(about.cv, "url"):
        return redirect(about.cv.url)

    file_path = os.path.join(settings.MEDIA_ROOT, about.cv.name)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, "rb"), content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    return HttpResponse("CV not found", status=404)
