from django.contrib import admin
from django.utils.html import format_html
from .models import (
    HeroSection,
    About,
    Skill,
    TimelineEvent,
    Project,
    Service,
    ContactInfo,
    SocialLink
)

# ---------------- Hero Section ----------------
@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'is_active', 'preview_image')
    list_filter = ('is_active',)
    search_fields = ('name', 'title')
    ordering = ('-is_active', 'name')
    readonly_fields = ('preview_image',)

    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="70" style="border-radius:6px; object-fit:cover;" />',
                obj.image.url
            )
        return "-"

    preview_image.short_description = "Image Preview"


# ---------------- About Section (MERGED & FIXED) ----------------
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview_image', 'cv_link', 'cv_downloads')
    search_fields = ('title',)
    readonly_fields = ('preview_image', 'cv_downloads')

    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" style="border-radius:50%; object-fit:cover;" />',
                obj.image.url
            )
        return "-"

    preview_image.short_description = "Profile Image"

    def cv_link(self, obj):
        if obj.cv:
            return format_html(
                '<a href="{}" target="_blank">View CV</a>',
                obj.cv.url
            )
        return "No CV"

    cv_link.short_description = "Resume (PDF)"


# ---------------- Skills ----------------
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency', 'preview_icon')
    list_filter = ('proficiency',)
    search_fields = ('name',)
    readonly_fields = ('preview_icon',)

    def preview_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="40" />', obj.icon.url)
        return "-"

    preview_icon.short_description = "Icon Preview"


# ---------------- Timeline Events ----------------
@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'order', 'preview_icon')
    list_editable = ('order',)
    ordering = ('order',)
    readonly_fields = ('preview_icon',)

    def preview_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="40" />', obj.icon.url)
        return "-"

    preview_icon.short_description = "Icon Preview"


# ---------------- Projects ----------------
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview_image', 'features', 'created_at')
    list_display_links = ('title',)
    search_fields = ('title', 'features')
    list_filter = ('created_at',)
    readonly_fields = ('preview_image',)

    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="70" style="border-radius:6px; object-fit:cover;" />',
                obj.image.url
            )
        return "-"

    preview_image.short_description = "Preview"


# ---------------- Services ----------------
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview_icon', 'order')
    list_editable = ('order',)
    ordering = ('order',)
    readonly_fields = ('preview_icon',)

    def preview_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="40" />', obj.icon.url)
        return "-"

    preview_icon.short_description = "Icon Preview"


# ---------------- Contact Info ----------------
@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'address')


# ---------------- Social Links ----------------
@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'order', 'preview_icon')
    list_editable = ('order',)
    ordering = ('order',)
    readonly_fields = ('preview_icon',)

    def preview_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="40" />', obj.icon.url)
        return "-"

    preview_icon.short_description = "Icon Preview"
