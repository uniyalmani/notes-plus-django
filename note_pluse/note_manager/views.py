from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_200_OK, HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Note, NoteVersion, SharedNote
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404
from auth_app.models import CustomUser as User
from .serializers.note_serializer import NoteSerializer
from .utils import convert_newlines_to_html
from .utils import error_response, success_response







@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def create_note(request):
    """
    Creates a new note, handling data processing, user permissions, and edge cases.

    Args:
        request: The Django request object.

    Returns:
        A Django Response object indicating success or an appropriate error message.
    """

    content = request.data.get('content')
    title = request.data.get('title', '')

    if not content:
        return error_response(errors='Missing content field.',
                              message="This API required content field",
                              status_code=status.HTTP_400_BAD_REQUEST)

    # Process content before creating the note:
    content = convert_newlines_to_html(content).strip()
    lines = content.splitlines()
    while lines and not lines[-1]:  # Remove trailing empty lines
        lines.pop()
    content = "\n".join(lines)

    # Create the note with processed content:
    note = Note.objects.create(content=content, title=title, owner=request.user)

    formatted_note = {
        'id': note.id,
        'title': note.title,
        'content': note.content,
    }

    return success_response(message='Note created successfully.', data=formatted_note, status_code=status.HTTP_201_CREATED)






def get_note(request, pk):
    """
    Retrieves a specific note with authorization checks.

    Args:
        request: The Django request object.
        pk: The primary key of the note to retrieve.

    Returns:
        A Django Response object containing the note data or an appropriate error message.
    """

    try:
        
        note = Note.objects.get(pk=pk, is_deleted=False)
        if note.owner != request.user:
            if not SharedNote.objects.filter(note=note, user=request.user).exists():
                response = error_response(errors='You are not authorized to view this note.'
                                          , message="please login this api is protected"
                                          ,status_code=status.HTTP_403_FORBIDDEN)
                return response

        
        note_data = {
            'id':note.id,
            'title': note.title,
            'content': note.content,
          
        }

        response = success_response(message="Note retrieved successfully."
                                    , data=note_data, status_code=status.HTTP_200_OK)
        return response

    except Note.DoesNotExist:
        response = error_response(errors='Note not found.',
                                  message="Note with given id does not exist",
                                  status_code=status.HTTP_404_NOT_FOUND)
        return response

    except Exception as e:
        response = error_response(errors='An unexpected error occurred.',
                                  message="unknow error occured",
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response






def update_notes(request, pk):
    """
    Updates a specific note, handling authorization, permissions, and edge cases.

    Args:
        request: The Django request object.
        pk: The primary key of the note to update.

    Returns:
        A Django Response object indicating success or an appropriate error message.
    """

    content = request.data.get('content')
    new_title = request.data.get('title')

    try:
        # Validate input and fetch note:
        if not content:
            response = error_response(errors='Missing content field.',
                                      message='this api required content field',
                                      status_code=status.HTTP_400_BAD_REQUEST)
            return response
        note = Note.objects.get(pk=pk, is_deleted=False)

        # Authorization and permission checks:
        if note.owner != request.user:
            if not SharedNote.objects.filter(note=note, user=request.user, can_edit=True).exists():
                response = error_response(errors='You are not authorized to update this note.',
                                          message="you need permission to edit this note",
                                        status_code=status.HTTP_403_FORBIDDEN)
                return response

        # Update title (optional):
        note.title = new_title or note.title  # Preserve existing title if not provided
        
        # Validate edits for shared users:
        if request.user != note.owner:
            original_lines = [line.strip() for line in note.content.split('<br>')]
            new_lines = [line.strip() for line in content.splitlines()]
            print(original_lines, new_lines)
            # Ensure only new lines are added, no deletion or modification allowed:
            if len(new_lines) <= len(original_lines) or any(
                old_line not in new_lines for old_line in original_lines
            ):
                response = error_response(errors='Shared users cannot modify existing content.',
                                          message='Only the owner can modify existing content',
                                          status_code=status.HTTP_403_FORBIDDEN)
                return response

        # Handle newlines correctly with <br> conversion:
        note.content = convert_newlines_to_html(content).strip()  # Convert newlines to <br> and remove leading/trailing whitespace

        # Save the updated note (triggers the signal handler)
        note.save()

        
        updated_note = {
            'id': note.id,
            'title': note.title,
            'content': note.content,
           
        }

        response = success_response(message='Note updated successfully.', data=updated_note,
                                    status_code=status.HTTP_200_OK)
        
        return response

    except Note.DoesNotExist:
        response = error_response(errors='Note not found.', 
                                  message="Notes with given id does not exist",
                                  status_code=status.HTTP_404_NOT_FOUND)
        return response

    except Exception as e:
        
        response = error_response(errors='error occured', 
                                  message="unkown error occured",
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return response





@api_view(['GET', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_or_update_notes(request, pk):
    if request.method == 'GET': 
        return get_note(request, pk) 
    elif request.method == 'PUT':
        return update_notes(request,pk)
    





@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_notes_version_history(request, pk):
    try:
        note = Note.objects.get(pk=pk, is_deleted=False, owner=request.user)
        
        notes_version = NoteVersion.objects.filter(note=note ).order_by('-version_number')
    except Note.DoesNotExist:
        response = error_response(errors='Note not found.',
                                  message=f"notes with id = {pk} not found"
                                  ,status_code=HTTP_404_NOT_FOUND)
        return response

    
    # Return list of version data with additional details
    version_data = [
    {
        'version_number': version.version_number,
        'timestamp': version.created_at,
        'content': version.content,
    }
    for version in notes_version
    ]
    
    response = success_response(message="notes history retrieved successfully",
                                data=version_data, 
                                status_code=status.HTTP_200_OK)

    return response








@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def share_note(request):
    try:
        data = request.data
        note_id = data['note_id']
        user_ids = list(data['user_ids'])

        # Validate note existence and ownership:
        note = get_object_or_404(Note, pk=note_id, owner=request.user)
        
        # Validate user IDs:
        invalid_user_ids = []
        for user_id in user_ids:
            try:
                
                user = get_object_or_404(User, pk=user_id)
                
                if user == note.owner:
                    continue
                if SharedNote.objects.filter(note=note, user=user).exists():
                    continue
                SharedNote.objects.create(note=note, user=user, can_edit=True)
            except User.DoesNotExist:
                invalid_user_ids.append(user_id)

        if invalid_user_ids:
            response = error_response(errors= "invalid user ids",
                                      message=f'Invalid user IDs: {invalid_user_ids}',
                                      status_code=status.HTTP_400_BAD_REQUEST)
            return Response({'error': f'Invalid user IDs: {invalid_user_ids}'}, status=HTTP_400_BAD_REQUEST)
       
        serializer = NoteSerializer(note)
        
        response = success_response(data={"user_id": user_ids, "note_id": note_id}, 
                                    message="successfully", 
                                    status_code=status.HTTP_200_OK)
        return response

    except KeyError as e:
        response = error_response(errors="missing keys",
                                  message= f'Missing required field',
                                  status_code=status.HTTP_400_BAD_REQUEST)
        return response

    except Exception as e:
        response = error_response(errors='error occured', 
                                  message="unkown error occured",
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return response
