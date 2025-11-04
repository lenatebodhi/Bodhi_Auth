# Bodhi_Django_Backend

Authorization and Authentication backend for the Bodhi platform.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/lenatebodhi/Bodhi_Auth.git

```

### 2. Add Environment Files

#### Create the following two files in the root directory of the project:
##### 1. .env file

```bash
DEBUG=True
DATABASE_NAME=bodhi

# LOCAL
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_PASSWORD=rvvj jkhu qjux ndmi
EMAIL_HOST_USER=lenatebodhi@gmail.com
DEFAULT_FROM_EMAIL=lenatebodhi@gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

# AWS S3 Storage
AWS_ACCESS_KEY=DO00KDJNX6NQY8F6JRHU
AWS_SECRET_KEY=JA3jPJgB/FwcG41mlnpeUHTGxDuQhRXZjJrTsxzPdG4
AWS_STORAGE_BUCKET_NAME=wearlay-documents

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
WEBHOOK_SUCCESS_SECRET=
WEBHOOK_FAILURE_SECRET=
WEBHOOK_CANCELLED_SECRET=

# Base URLs
DEFAULT_BASE_URL=https://www.ringofhires.com/
ADMIN_BASE_URL=https://app.ringofhires.com/admin/

# Social Media URLs
GOOGLE_CLIENT_ID=
FACEBOOK_URL=www.facebook.com
TWITTER_URL=www.twitter.com
LINKEDIN_URL=www.linkedin.com
INSTAGRAM_URL=www.instagram.com

# Celery + Redis
CELERY_BROKER_URL=redis://redis:6379/0
RESULT_BACKEND=redis://redis:6379/0

# Twilio SMS Service
TWILO_ACCOUNT_SID=ACf4817a95e11109e27a77ad17682fcc96
TWILO_ACCESS_TOKEN=6f9586fd1e4d761398c9416e3be7ce30
TWILO_SERVICE_ID=VA8cb9f32f11d414fd4a57b59709d91e02

# JWT Secret Key
JWT_SECRET_KEY=django-insecure-+y0d%cn__#!97t-*%pq5f-!s#ruj40p&-ejssdj94zvbh3&6ke
```

##### 2. .env.db file
``` bash
POSTGRES_DB=bodhi
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

```

### 3. Running the Project with Docker
#### 1. Build and Start Containers
```bash
docker compose up --build

```

#### 2. Apply Migrations
```bash
docker compose exec backend python manage.py migrate

```

