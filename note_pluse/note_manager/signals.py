from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Note, NoteVersion

@receiver(post_save, sender=Note)
def create_note_version(sender, instance, created, **kwargs):
    """
    Create a new version of the note whenever it's saved, 
    whether created or updated.
    """
    # Check if the note already has versions 
    if not created and NoteVersion.objects.filter(note=instance).exists():
        # Get the latest version and check if content has changed
        latest_version = NoteVersion.objects.filter(note=instance).order_by('-version_number').first()
        if latest_version.content != instance.content:
            # Content has changed, create a new version
            NoteVersion.objects.create(note=instance, content=instance.content, version_number=latest_version.version_number + 1)
    else:
        # New note or content changed, create a new version
        NoteVersion.objects.create(note=instance, content=instance.content, version_number=1)


@receiver(post_delete, sender=Note)
def delete_note_versions(sender, instance, **kwargs):
    # Delete associated versions when the note is deleted
    instance.versions.all().delete()