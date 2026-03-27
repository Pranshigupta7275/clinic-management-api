# Clinic API

A Django REST Framework-based API for managing clinic patients and appointments with token-based authentication.


# Dashboard Screenshots

<img src="https://github.com/user-attachments/assets/909eb7b7-bcdf-46d3-ab96-5cd94f756df1" width="800" />
<img src="https://github.com/user-attachments/assets/323e2011-b279-4f2e-b00d-80357c048114" width="800">
<img src="https://github.com/user-attachments/assets/b6068e55-d581-4969-86fa-e85bded3af65" width="800">
<img src="https://github.com/user-attachments/assets/2eca385f-71aa-45d2-a58c-392635bd9a6b"  width="800">


- Patient management (CRUD operations)
- Appointment scheduling and management
- Real-time statistics and analytics
- Upcoming appointments list (7-day window)
- Token-based authentication
- Custom permission system (Staff-only write access)
- Consistent response formatting
- Search and filter capabilities

## Prerequisites

- Python 3.11+
- Django 6.0.3
- Django REST Framework 3.17.1

## Setup

### 1. Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

```bash
python manage.py migrate
```

### 4. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 5. Run Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication

#### Login

- **Endpoint**: `POST /api/auth/login/`
- **Auth**: Not required
- **Request Body**:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

- **Response**:

```json
{
  "success": true,
  "data": {
    "token": "abcd1234efgh5678ijkl9012mnop3456"
  },
  "message": "Login successful"
}
```

#### Token Auth (DRF Built-in)

- **Endpoint**: `POST /api/auth/token/`
- **Auth**: Not required
- **Request Body**:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

### Patients

#### List Patients

- **Endpoint**: `GET /api/patients/`
- **Auth**: Token or Session
- **Query Parameters**:
  - `search` (optional): Search by patient name
- **Response**:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "age": 30,
      "gender": "Male",
      "contact_number": "1234567890",
      "blood_group": "O+",
      "created_at": "2024-03-27T10:00:00Z"
    }
  ],
  "message": "Patients fetched successfully"
}
```

#### Create Patient

- **Endpoint**: `POST /api/patients/`
- **Auth**: Staff token required
- **Request Body**:

```json
{
  "name": "Jane Smith",
  "age": 28,
  "gender": "Female",
  "contact_number": "9876543210",
  "blood_group": "A+"
}
```

#### Retrieve Patient

- **Endpoint**: `GET /api/patients/{id}/`
- **Auth**: Token or Session

#### Update Patient

- **Endpoint**: `PUT /api/patients/{id}/`
- **Auth**: Staff token required

#### Delete Patient

- **Endpoint**: `DELETE /api/patients/{id}/`
- **Auth**: Staff token required

### Appointments

#### List Appointments

- **Endpoint**: `GET /api/appointments/`
- **Auth**: Token or Session
- **Query Parameters**:
  - `status` (optional): Filter by status (Pending, Confirmed, Cancelled)
  - `patient_id` (optional): Filter by patient ID
- **Response**:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "patient": 1,
      "patient_name": "John Doe",
      "doctor_name": "Dr. Smith",
      "appointment_date": "2024-04-01T14:00:00Z",
      "reason": "General Checkup",
      "status": "Confirmed"
    }
  ],
  "message": "Appointments fetched successfully"
}
```

#### Create Appointment

- **Endpoint**: `POST /api/appointments/`
- **Auth**: Staff token required
- **Request Body**:

```json
{
  "patient": 1,
  "doctor_name": "Dr. Brown",
  "appointment_date": "2024-04-05T10:30:00Z",
  "reason": "Follow-up consultation",
  "status": "Pending"
}
```

#### Update Appointment Status

- **Endpoint**: `PATCH /api/appointments/{id}/`
- **Auth**: Staff token required
- **Request Body**:

```json
{
  "status": "Confirmed"
}
```

#### Delete Appointment

- **Endpoint**: `DELETE /api/appointments/{id}/`
- **Auth**: Staff token required

### Statistics

#### Get Stats

- **Endpoint**: `GET /api/stats/`
- **Auth**: Token or Session
- **Response**:

```json
{
  "success": true,
  "data": {
    "total_patients": 5,
    "total_appointments": 12,
    "status_counts": [
      { "status": "Pending", "count": 3 },
      { "status": "Confirmed", "count": 7 },
      { "status": "Cancelled", "count": 2 }
    ]
  },
  "message": "Stats fetched successfully"
}
```

### Upcoming Appointments

#### Get Next 7 Days' Appointments

- **Endpoint**: `GET /api/upcoming-appointments/`
- **Auth**: Token or Session
- **Response**:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "patient": 1,
      "patient_name": "John Doe",
      "doctor_name": "Dr. Smith",
      "appointment_date": "2024-03-29T14:00:00Z",
      "reason": "General Checkup",
      "status": "Confirmed"
    }
  ],
  "message": "Upcoming appointments fetched successfully"
}
```

## Sample Requests (cURL)

### 1. Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. List Patients (with token)

```bash
curl -X GET http://localhost:8000/api/patients/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 3. Search Patients

```bash
curl -X GET "http://localhost:8000/api/patients/?search=John" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 4. Create Patient (Staff only)

```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{
    "name": "Alice Wonder",
    "age": 32,
    "gender": "Female",
    "contact_number": "5555555555",
    "blood_group": "B+"
  }'
```

### 5. Create Appointment (Staff only)

```bash
curl -X POST http://localhost:8000/api/appointments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{
    "patient": 1,
    "doctor_name": "Dr. Johnson",
    "appointment_date": "2024-04-10T10:00:00Z",
    "reason": "Dental checkup",
    "status": "Pending"
  }'
```

### 6. Get Statistics

```bash
curl -X GET http://localhost:8000/api/stats/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 7. Get Upcoming Appointments

```bash
curl -X GET http://localhost:8000/api/upcoming-appointments/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 8. Filter Appointments by Status

```bash
curl -X GET "http://localhost:8000/api/appointments/?status=Confirmed" \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Project Structure

```
clinic_api/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── README.md
├── clinic_api/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── patients/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── permissions.py
    ├── responses.py
    ├── urls.py
    ├── admin.py
    ├── apps.py
    └── migrations/
```

## Authentication

The API uses **Token-Based Authentication**. To authenticate:

1. Log in using `/api/auth/login/` with username and password
2. Receive a token in the response
3. Include the token in all subsequent requests:
   ```
   Authorization: Token YOUR_TOKEN_HERE
   ```

## Permissions

- **AllowAny**: No authentication required (Login, Home endpoints)
- **IsStaffOrReadOnly**: Staff members can write/update/delete, all users can read
  - Applied to: Patients, Appointments, Stats, Upcoming Appointments

## Response Format

All API responses follow a consistent format:

```json
{
  "success": true/false,
  "data": {...},
  "message": "Descriptive message"
}
```

## Testing

Run the test suite:

```bash
python manage.py test patients
```

## Admin Interface

Access the Django admin panel at `http://localhost:8000/admin/`

## Requirements

See `requirements.txt` for all dependencies:

- asgiref==3.11.1
- django==6.0.3
- djangorestframework==3.17.1
- sqlparse==0.5.5

## Troubleshooting

### ModuleNotFoundError: No module named 'rest_framework'

```bash
pip install djangorestframework
```

### Database errors

```bash
python manage.py migrate
```

### Port already in use

```bash
python manage.py runserver 8001
```

## License

This project is provided as-is for educational and clinic management purposes.

## Support

For issues or questions, please refer to the project documentation or contact the development team.
