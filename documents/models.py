from django.db import models
from django.conf import settings
from django.utils import timezone

class DocumentType(models.Model):
    """User-defined document types - UNLIMITED"""
    type_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_document_types')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['type_name']
    
    def __str__(self):
        return self.type_name

class CheckpointTemplate(models.Model):
    """Predefined checkpoints for each document type"""
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE, related_name='checkpoints')
    checkpoint_name = models.CharField(max_length=100)
    sequence_order = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['document_type', 'sequence_order']
        unique_together = ['document_type', 'sequence_order']
    
    def __str__(self):
        return f"{self.document_type.type_name} - {self.checkpoint_name}"

class Route(models.Model):
    """Routes for document distribution"""
    route_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['route_name']
    
    def __str__(self):
        return self.route_name

class Document(models.Model):
    """Main document tracking table"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('finalized', 'Finalized'),
    ]
    
    # Auto-generated tracking ID
    tracking_id = models.CharField(max_length=20, unique=True, editable=False)
    
    # Document details
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT, related_name='documents')
    route = models.ForeignKey(Route, on_delete=models.PROTECT, related_name='documents')
    document_date = models.DateField()
    exam_date = models.DateField(null=True, blank=True)
    
    # Status tracking
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    current_location = models.CharField(max_length=100, blank=True)
    is_finalized = models.BooleanField(default=False)
    
    # Metadata
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tracking_id']),
            models.Index(fields=['document_type', 'route']),
            models.Index(fields=['current_status']),
        ]
    
    def __str__(self):
        return f"{self.tracking_id} - {self.document_type.type_name}"
    
    def save(self, *args, **kwargs):
        if not self.tracking_id:
            # Generate tracking ID: DTS-YYYYMMDD-XXXX
            from django.utils.timezone import now
            date_str = now().strftime('%Y%m%d')
            last_doc = Document.objects.filter(tracking_id__startswith=f'DTS-{date_str}').order_by('-tracking_id').first()
            if last_doc:
                last_num = int(last_doc.tracking_id.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.tracking_id = f'DTS-{date_str}-{new_num:04d}'
        super().save(*args, **kwargs)
    
    def get_completion_percentage(self):
        """Calculate completion percentage based on checkpoints"""
        total_checkpoints = self.checkpoints.count()
        if total_checkpoints == 0:
            return 0
        completed_checkpoints = self.checkpoints.filter(is_completed=True).count()
        return int((completed_checkpoints / total_checkpoints) * 100)

class DocumentCheckpoint(models.Model):
    """Individual checkpoints for each document"""
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='checkpoints')
    checkpoint_name = models.CharField(max_length=100)
    sequence_order = models.IntegerField()
    
    # Completion tracking
    is_completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='completed_checkpoints')
    completed_at = models.DateTimeField(null=True, blank=True)
    receiver_name = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    
    class Meta:
        ordering = ['document', 'sequence_order']
        unique_together = ['document', 'sequence_order']
    
    def __str__(self):
        return f"{self.document.tracking_id} - {self.checkpoint_name}"
    
    def mark_completed(self, user, receiver_name='', remarks=''):
        """Mark checkpoint as completed"""
        self.is_completed = True
        self.completed_by = user
        self.completed_at = timezone.now()
        self.receiver_name = receiver_name
        self.remarks = remarks
        self.save()
        
        # Update document status
        if self.document.checkpoints.filter(is_completed=False).count() == 0:
            self.document.current_status = 'finalized'
            self.document.is_finalized = True
        elif self.document.checkpoints.filter(is_completed=True).count() > 0:
            self.document.current_status = 'in_progress'
        self.document.save()
