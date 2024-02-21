from django.urls import path
from .views import create_note,  get_or_update_notes, get_notes_version_history, share_note

urlpatterns = [
    path('create/', create_note, name='createNotes'),
    path('<uuid:pk>/', get_or_update_notes, name='get_notes'),
    path('version-history/<uuid:pk>/', get_notes_version_history, name="get history"),
    path('share/', share_note, name="share note" )
]