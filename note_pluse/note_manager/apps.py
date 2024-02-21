from django.apps import AppConfig


class NoteManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'note_manager'
    
    def ready(self):
        import note_manager.signals
