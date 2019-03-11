"""Circles admin."""

# Django
from django.contrib import admin

# Model
from cride.circles.models import Circle, Membership


@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Circle admin."""

    list_display = (
        'slug_name',
        'name',
        'is_public',
        'verified',
        'is_limited',
        'members_limit'
    )
    search_fields = ('slug_name', 'name')
    list_filter = (
        'is_public',
        'verified',
        'is_limited'
    )


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    """Membership admin."""

    list_display = (
        'user',
        'profile',
        'circle',
        'is_admin',
        'is_active'
    )
    search_fields = ('circle',)
    list_filter = (
        'is_admin',
        'is_active'
    )
