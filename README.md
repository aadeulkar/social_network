 # Social Networking API

This is a social networking API built using Django and Django REST Framework (DRF). 
It supports user authentication, search, friend requests, and listing friends and pending requests. 
The project is containerized using Docker and uses JWT authentication.

## Features

- User registration and login with JWT tokens
- Search users by email or name
- Send and respond to friend requests
- List friends and pending friend requests

## Installation

1. **Clone the repository:**
   ```bash
   git clone  https://github.com/aadeulkar/social_network.git
   cd social_network

2.Set up the virtual environment:
python -m venv venv
venv\Scripts\activate # for windows

3.Install dependencies:
pip install -r requirements.txt

4.Run migrations:
python manage.py makemigrations
python manage.py migrate

5.Create a superuser:
python manage.py createsuperuser

6.Run the development server:
python manage.py runserver


# API Endpoints

POST /signup/: Register a new user.
POST /login/: Obtain JWT tokens for authentication.
POST /token/refresh/: Refresh JWT tokens.
GET /search/?q=<keyword>: Search users by email or name (paginated, 10 records per page).
POST /friend-request/send/: Send a friend request.
POST /friend-request/respond/: Respond to a friend request.
GET /friends/: List friends.
GET /friend-requests/pending/: List pending friend requests.


# Admin Panel
You can view and manage users and friend requests from the Django admin panel. Access it at http://localhost:8000/admin/

# Authentication
Sign Up: Users can register with their email address.
Login: Users can log in using their email and password to receive a JWT token.
Token Refresh: Use the token refresh endpoint to obtain a new JWT token.


# Postman Collection link
Postman_collection : "https://api.postman.com/collections/38198672-72954d53-e899-463a-b4f0-ac7476135e10?access_key=PMAT-01J7EM96YCDSE693RFSVKRXR5J"

# API Curl call

# 1. POST /signup/: 

curl --location 'http://127.0.0.1:8000/api/users/signup/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"ashish7",
    "password":"ashish7",
    "email": "ashish7@gmail.com"
}'

# 2. POST /login/: 
 
 curl --location 'http://127.0.0.1:8000/api/users/login/' \
--header 'Content-Type: application/json' \
--data '{
    "username":"ashish2",
    "password":"ashish2"
}'


# 3. POST /token/refresh/: 

 curl --location 'http://127.0.0.1:8000/api/users/token/refresh/' \
--header 'Content-Type: application/json' \
--data '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNjA3Njg4MCwiaWF0IjoxNzI1OTkwNDgwLCJqdGkiOiI1NDk5ZDEzZTBlN2U0ZjkwOWI1OGI1NDk4MzZlNGVkNyIsInVzZXJfaWQiOjE1fQ.gHhgVLSL7tUEQ4AzJlGQMo7TEkpUvm4XZJl9qHG6C9g"
}'


# 4.GET /search/?q=<keyword>:

curl --location 'http://127.0.0.1:8000/api/users/search/?q=%20ashi' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2MDc2ODgwLCJpYXQiOjE3MjU5OTA0ODAsImp0aSI6ImYwOWEyNWUxODFkYTQwYjE5NzA0MGJlZjAzMTZmYzY4IiwidXNlcl9pZCI6MTV9.408MqscfsV84JJrhLGX2p49_2s1fSZJt5WG5AIhyuHg'

 
# 5. POST /friend-request/send/:

curl --location 'http://127.0.0.1:8000/api/users/friend-request/send/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2MDc2ODgwLCJpYXQiOjE3MjU5OTA0ODAsImp0aSI6ImYwOWEyNWUxODFkYTQwYjE5NzA0MGJlZjAzMTZmYzY4IiwidXNlcl9pZCI6MTV9.408MqscfsV84JJrhLGX2p49_2s1fSZJt5WG5AIhyuHg' \
--header 'Content-Type: application/json' \
--data '{
    "receiver_id": 16
}'


# 6. POST /friend-request/respond/:

curl --location 'http://127.0.0.1:8000/api/users/friend-request/respond/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2MDc2ODgwLCJpYXQiOjE3MjU5OTA0ODAsImp0aSI6ImYwOWEyNWUxODFkYTQwYjE5NzA0MGJlZjAzMTZmYzY4IiwidXNlcl9pZCI6MTV9.408MqscfsV84JJrhLGX2p49_2s1fSZJt5WG5AIhyuHg' \
--header 'Content-Type: application/json' \
--data '{
    "request_id":22,
    "action":"accept"
}'


# 7. GET /friends/: 

curl --location 'http://127.0.0.1:8000/api/users/friends' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2MDc2ODgwLCJpYXQiOjE3MjU5OTA0ODAsImp0aSI6ImYwOWEyNWUxODFkYTQwYjE5NzA0MGJlZjAzMTZmYzY4IiwidXNlcl9pZCI6MTV9.408MqscfsV84JJrhLGX2p49_2s1fSZJt5WG5AIhyuHg'

 
 # 8.GET /friend-requests/pending/: 
 
 curl --location 'http://127.0.0.1:8000/api/users/friend-requests/pending/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2MDc2ODgwLCJpYXQiOjE3MjU5OTA0ODAsImp0aSI6ImYwOWEyNWUxODFkYTQwYjE5NzA0MGJlZjAzMTZmYzY4IiwidXNlcl9pZCI6MTV9.408MqscfsV84JJrhLGX2p49_2s1fSZJt5WG5AIhyuHg'



















