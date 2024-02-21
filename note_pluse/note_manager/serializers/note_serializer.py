from rest_framework import serializers
from ..models import Note, SharedNote


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'  
        

class ShareNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedNote
        fields = ('note_id', 'user_ids', 'can_edit')

        extra_kwargs = {
            'note_id': {'required': True},
            'user_ids': {'required': True}
        }
