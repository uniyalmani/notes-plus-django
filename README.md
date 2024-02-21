# Project Setup 

## requirement
Docker

```
docker-compose up
```


# API Documentation

This documentation provides information about the  API .

## Signup API

### Endpoint

`POST /api/auth/signup/`

### Request Body

```json
{
  "name": "example",
  "email": "example@examplel.com",
  "password": "secure_password123",
  "dob": "1990-01-01"
}
```
Success Response
```json
{
    "data": {
        "refresh": "",
        "access": ""
    },
    "success": true,
    "message": "account creation successful"
}
```
Error Response
```json
{
    "errors": {
        "field_name": ["error_message"],
        "another_field": ["error_message"]
    },
    "success": false,
    "message": "Error message"
}
```
Notes
The name and email fields should be unique.
Password must meet the security requirements.
The dob (Date of Birth) field is optional.


## Login API

### Endpoint

`POST /api/auth/login/`

### Request Body

```json
{
  "email": "example@examplel.com",
  "password": "secure_password123"
}
```
Success Response
```json
{
    "data": {
        "refresh": "",
        "access": ""
    },
    "success": true,
    "message": "Login successful"
}
```
Error Response
```json
{
    "errors": {
        "error": ["Invalid credentials"]
    },
    "success": false,
    "message": "Error"
}
```
Notes
The email and password fields are required for login.
Ensure that the provided credentials are correct for successful login.


## Refresh Token API

### Endpoint

`POST /api/auth/refresh-token/`

### Request Body

```json
{
    "refresh_token": "your_refresh_token_here"
}
```
Success Response
```json
{
    "data": {
        "access_token": "your_new_access_token_here",
        "refresh_token": "your_new_refresh_token_here"
    },
    "success": true,
    "message": "Token refreshed successfully"
}
```
Error Response
```json
{
    "errors": {
        "error": ["Invalid refresh token"]
    },
    "success": false,
    "message": "Error"
}
```
Notes
Provide a valid refresh_token for refreshing the access token.
The refresh_token is obtained during the login process.
Ensure that the provided refresh token is valid for a successful refresh.



## Create  Notes API

### Endpoint

`POST /api/notes/create/`

### Request Headers

- `Authorization`: Bearer Token (Include your valid access token)

### Request Body

```json
{
    "content": "thsi is good \n this is it",
    "title": "new Notes 2 "
}
```
Success Response
```json
{
    "data": {
        "id": "81c807f8-a824-4a15-ac73-28a54a279226",
        "title": "new Notes 2 ",
        "content": "thsi is good <br> this is it"
    },
    "success": true,
    "message": "Note created successfully."
}
```
Error Response
```json
{
    "errors": {
        "error": ["error "]
    },
    "success": false,
    "message": "Error"
}
```
Notes
Ensure that you include a valid Bearer Token in the Authorization header.
The API is protected, and only authorized users can add paragraphs.
Handle duplicate entries by checking the error message in the error response.


## Get Notes API

### Endpoint

`GET /api/notes/{note_id}/`

### Request Headers

- `Authorization`: Bearer Token (Include your valid access token)

### Request Path Parameter

- `note_id` (required): id to search for note.

### Success Response

```json
{
    "data": {
        "id": "62ebfd68-872b-4017-bab7-c46f1cd24e66",
        "title": "new Notes 2 ",
        "content": "thsi is good <br> this is it"
    },
    "success": true,
    "message": "Note retrieved successfully."
}
```
Error Response
```json
{
    "errors": "error ",
    "success": false,
    "message": "Error"
}
```
Notes
Ensure that you include a valid Bearer Token in the Authorization header.
The API is protected, and only authorized users can retrieve notes.
The id parameter is required. 



## Update Notes API

### Endpoint

`PUT /api/notes/{note_id}/`

### Request Headers

- `Authorization`: Bearer Token (Include your valid access token)

### Request Path Parameter

- `note_id` (required): id to search for note.

### Request Body
```json
{
    "content": "thsi is good \n hello \n this is good",
    "title": "notes.py "
}
```

### Success Response

```json
{
    "data": {
        "id": "81c807f8-a824-4a15-ac73-28a54a279226",
        "title": "notes.py ",
        "content": "thsi is good <br> hello <br> this is good"
    },
    "success": true,
    "message": "Note updated successfully."
}
```
Error Response
```json
{
    "errors": "error ",
    "success": false,
    "message": "Error"
}
```

Notes
Ensure that you include a valid Bearer Token in the Authorization header.
The API is protected, and only authorized users can retrieve notes.
\n is for new line exp - "this is \n good way" these are two lines
The id parameter is required. 



## Get Notes History API

### Endpoint

`GET /api/notes/version-history/{note_id}/`

### Request Headers

- `Authorization`: Bearer Token (Include your valid access token)

### Request Path Parameter

- `note_id` (required): id to search for note.

### Success Response

```json
{
        "data" : [
        {
            "version_number": 6,
            "timestamp": "2024-02-21T07:28:51.034318Z",
            "content": "thsi is good"
        },
        {
            "version_number": 5,
            "timestamp": "2024-02-21T07:28:26.998033Z",
            "content": "thsi is good <br> hello"
        },
        {
            "version_number": 4,
            "timestamp": "2024-02-21T07:19:50.869796Z",
            "content": "thsi is good"
        },
        {
            "version_number": 3,
            "timestamp": "2024-02-21T07:19:45.341201Z",
            "content": "thsi is good <br> t"
        },
        {
            "version_number": 2,
            "timestamp": "2024-02-21T07:18:35.224591Z",
            "content": "thsi is good <br> this is it <br> added"
        },
        {
            "version_number": 1,
            "timestamp": "2024-02-21T07:16:21.161463Z",
            "content": "thsi is good <br> this is it"
        }
    ],
    "success": true,
    "message": "notes history retrieved successfully"
}
```
Error Response
```json
{
    "errors": "error ",
    "success": false,
    "message": "Error"
}
```

Notes
Ensure that you include a valid Bearer Token in the Authorization header.
The API is protected, and only authorized users can retrieve notes.
api will return all changes made previously
The id parameter is required. 



## Share Notes API

### Endpoint

`POST /api/notes/share/`

### Request Headers

- `Authorization`: Bearer Token (Include your valid access token)

### Request Body
```json
{
    "note_id": "81c807f8-a824-4a15-ac73-28a54a279226",
    "user_ids": [2]
}
```

### Success Response

```json
{
    "data": {
        "user_id": [
            2
        ],
        "note_id": "81c807f8-a824-4a15-ac73-28a54a279226"
    },
    "success": true,
    "message": "successfully"
}
```
Error Response
```json
{
    "errors": "error ",
    "success": false,
    "message": "Error"
}
```
Notes
Ensure that you include a valid Bearer Token in the Authorization header.
The API is protected, and only authorized users can retrieve notes.
The id parameter is required. 



