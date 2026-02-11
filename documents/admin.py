from django.contrib import admin
from .models import DocumentType, CheckpointTemplate, Route, Document, DocumentCheckpoint

class CheckpointTemplateInline(admin.TabularInline):
    model = CheckpointTemplate
    extra = 1
    fields = ['checkpoint_name', 'sequence_order', 'description']

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['type_name', 'description']
    inlines = [CheckpointTemplateInline]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['route_name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['route_name', 'description']

class DocumentCheckpointInline(admin.TabularInline):
    model = DocumentCheckpoint
    extra = 0
    fields = ['checkpoint_name', 'sequence_order', 'is_completed', 'completed_by', 'completed_at', 'receiver_name']
    readonly_fields = ['completed_by', 'completed_at']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['tracking_id', 'document_type', 'route', 'current_status', 'document_date', 'created_by', 'created_at']
    list_filter = ['current_status', 'document_type', 'route', 'is_finalized', 'document_date']
    search_fields = ['tracking_id', 'notes']
    readonly_fields = ['tracking_id', 'created_at', 'updated_at']
    inlines = [DocumentCheckpointInline]
    
    fieldsets = (
        ('Document Information', {
            'fields': ('tracking_id', 'document_type', 'route', 'document_date', 'exam_date')
        }),
        ('Status', {
            'fields': ('current_status', 'current_location', 'is_finalized')
        }),
        ('Additional Details', {
            'fields': ('notes', 'created_by', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(DocumentCheckpoint)
class DocumentCheckpointAdmin(admin.ModelAdmin):
    list_display = ['document', 'checkpoint_name', 'sequence_order', 'is_completed', 'completed_at']
    list_filter = ['is_completed', 'completed_at']
    search_fields = ['document__tracking_id', 'checkpoint_name']
    readonly_fields = ['completed_at']
