from django.db import models
from uuid import uuid4
from auth_app.models import CustomUser as User



class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    content = models.TextField()
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    

class NoteVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    content = models.TextField()
    version_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='shared_with')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)

    class Meta:
        unique_together = ('note', 'user') 
