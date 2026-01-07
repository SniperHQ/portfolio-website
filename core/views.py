from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages

from .models import (
    HeroSection,
    About,
    Skill,
    TimelineEvent,
    Project,
    Service,
    ContactInfo,
    ContactMessage,
    SocialLink
)

import logging

logger = logging.getLogger(__name__)


# ================= HOME =================
def home(request):
    hero = HeroSection.objects.filter(is_active=True).first()
    projects = Project.objects.all().order_by('-created_at')[:3]
    services = Service.objects.all()

    return render(request, 'home.html', {
        'hero': hero,
        'projects': projects,
        'services': services,
    })


# ================= ABOUT =================
def about(request):
    about_info = About.objects.first()
    skills = Skill.objects.all()
    timeline = TimelineEvent.objects.all()

    return render(request, 'about.html', {
        'about_info': about_info,
        'skills': skills,
        'timeline': timeline,
    })


# ================= PROJECTS =================
def projects(request):
    projects_list = Project.objects.all().order_by('-created_at')
    return render(request, 'projects.html', {'projects': projects_list})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_detail.html', {'project': project})


# ================= SERVICES =================
def services(request):
    services_list = Service.objects.all()
    return render(request, 'services.html', {'services': services_list})


# ================= CONTACT =================
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage, ContactInfo
from twilio.rest import Client
import logging

logger = logging.getLogger(__name__)

def contact_view(request):
    contact_info = ContactInfo.objects.first()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message_content = request.POST.get('message')

        if not name or not email or not phone or not message_content:
            messages.error(request, "All fields are required.")
            return redirect('contact')

        # Save message in database
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message_content
        )

        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            # Send WhatsApp message to admin
            client.messages.create(
                body=f"New message from {name} ({phone}, {email}): {message_content}",
                from_=settings.TWILIO_WHATSAPP_NUMBER,
                to=settings.MY_WHATSAPP_NUMBER
            )

            # Send WhatsApp confirmation to user
            client.messages.create(
                body=f"Hi {name}, thanks for reaching out! I received your message and will reply soon.",
                from_=settings.TWILIO_WHATSAPP_NUMBER,
                to=f"whatsapp:{phone}"
            )

            messages.success(request, "Message sent! WhatsApp confirmation delivered.")

        except Exception as e:
            logger.error(f"WhatsApp sending failed: {e}")
            messages.error(request, "Message saved, but WhatsApp confirmation failed.")

        return redirect('contact')

    return render(request, 'contact.html', {'contact_info': contact_info})



# ================= CONTACT AJAX =================
@csrf_exempt
def contact_ajax(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

    name = request.POST.get('name')
    email = request.POST.get('email')
    message_content = request.POST.get('message')

    if not name or not email or not message_content:
        return JsonResponse({'status': 'error', 'message': 'All fields are required.'})

    # Save message
    ContactMessage.objects.create(
        name=name,
        email=email,
        message=message_content
    )

    try:
        send_mail(
            subject=f"New Contact Message from {name}",
            message=f"From: {name} ({email})\n\n{message_content}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=True,  # 🔥 CRITICAL
        )
        return JsonResponse({'status': 'success', 'message': 'Message sent successfully.'})
    except Exception as e:
        logger.error(f"Email sending failed: {e}")
        return JsonResponse({
            'status': 'success',
            'message': 'Message saved. We will contact you shortly.'
        })


# ================= CV DOWNLOAD =================
def download_cv(request):
    about = About.objects.first()

    if not about or not about.cv:
        raise Http404("CV not available")

    # 📈 Track downloads
    about.cv_downloads += 1
    about.save(update_fields=['cv_downloads'])

    return FileResponse(
        about.cv.open(),
        as_attachment=True,
        filename=about.cv.name.split('/')[-1]
    )


# ================= CONTEXT PROCESSOR =================
def base_context(request):
    return {
        'social_links': SocialLink.objects.all()
    }
