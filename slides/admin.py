from django.contrib import admin

from slides.models import Slide, Block


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['slide_id', 'name', 'created_on']
    readonly_fields = ['slide_id']


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['block_id', 'active']
    readonly_fields = ['block_id']
