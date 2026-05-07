# Crccf QR Code Generator

A Django-only employee QR verification system. It generates a unique QR code for each employee, but the QR code stores only a permanent verification URL:

```text
http://127.0.0.1:8000/employee/verify/<employee_id>/
```

When an admin updates employee data, the downloaded QR image stays the same and scans show the latest database record.

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

## Create Admin User

```bash
python manage.py createsuperuser
```

## Run Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```
