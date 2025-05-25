# HopeConnect

**HopeConnect** is a Django 5.2-based RESTful API and real-time backend system built to coordinate donations, orphan sponsorships, and volunteer services for children in Gaza. The system is designed for **transparency**, **efficiency**, and **real-time collaboration** between donors, volunteers, orphanages, and logistics teams.

---

## 🌟 Key Features

- **User Roles**: Admin, Donor, Volunteer, Orphanage, Logistics  
- **Donations**: Money, clothes, food, education & medical aid  
- **Sponsorships**: Donors can sponsor orphans with update tracking  
- **Volunteer Offers**: Skill-based volunteer help (e.g., medical, teaching)  
- **Deliveries**: Real-time delivery tracking with status updates  
- **Orphanage Reviews**: Donors leave reviews and star ratings  
- **Secure Payments**: Stripe integration for monetary donations  
- **JWT Authentication**: Secure access with refresh + access tokens  
- **WebSockets**: Real-time updates with Django Channels  
- **Background Jobs**: Celery + Redis for async task handling  
- **Semantic Matching**: Embeddings-powered skill matching system  

---

## 📦 Tech Stack

| Layer            | Technology                        |
|------------------|-----------------------------------|
| Backend          | Django 5.2, Django REST Framework |
| Real-Time        | Django Channels + Redis           |
| Background Tasks | Celery + Redis                    |
| Database         | MySQL                             |
| Payments         | Stripe API                        |
| Auth             | JWT (SimpleJWT)                   |
| Containerization | Docker + Docker Compose           |

---

## 🚀 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/<your-org>/hopeconnect.git
cd hopeconnect

# 2. Setup environment
cp .env.example .env

# 3. Run backend (Docker or manual)
docker-compose up -d

# If using local setup
python manage.py migrate
python manage.py createsuperuser
```

---

## 🧩 API Overview

### 🔐 Auth
- `POST /api/auth/login/` — Obtain JWT tokens  
- `POST /api/auth/logout/` — Blacklist refresh token  

### 👥 Users
- Register, update, soft-delete account  
- Role-based access control  

### 🎁 Donations
- Create money or material donations  
- Attach to orphan or campaign  
- Admin updates status and adds reports  

### 🧒 Orphans
- Create and update orphan profiles  
- Sponsors view progress reports & notes  

### 🏠 Orphanages
- Register and update info  
- Receive reviews and donations  

### 🙋 Volunteers
- Create profiles with skills & availability  
- Offer services (e.g., tutoring, medical aid)  

### 🚚 Deliveries
- Admin schedules pickups/drop-offs  
- Donors can view delivery progress in real time  

### 🧠 Matcher
- Match volunteers with orphanage requests  
- AI-powered semantic matching engine  

---

## 🧪 Testing

- ✅ **Postman Collection included**
- Roles covered: Admin, Donor, Volunteer, Orphanage  
- Manual & optional automated testing with `pytest` or `unittest`

---

## 📡 Real-Time & Background Processing

- **WebSockets (Django Channels)**: Real-time updates (e.g., delivery status)
- **Celery + Redis**: Async task queue for email, refunds, report processing

---

## 🔒 Security

- Role-based access control  
- JWT-secured endpoints with token rotation  
- Blacklisting of refresh tokens on logout  
- Django-level protections (CSRF, SQL injection, etc.)

---

## 🛠 Deployment

- Fully Dockerized with MySQL & Redis containers  
- `.env.example` provided for easy environment setup  
- Production ready with:
  - Gunicorn
  - (Optional) Nginx reverse proxy
  - (Optional) SSL certificate support

---

## 📑 License

MIT License

---

## 🙌 Contributors

- **Osama Mansour**  
- Team Members @ An-Najah National University  
- Instructor: Dr. Amjad AbuHassan

---

## 📚 Resources

- [📘 Project Wiki](https://github.com/Eng-OsamaMansour/HopeConnect/wiki)  
- [📬 Postman Collection](https://www.postman.com/eng-osama/workspace/hopeconnect/collection/39599522-138adac2-00fb-47bf-85b8-6da4442717e7?action=share&creator=39599522)  
- [🧾 Django REST Framework](https://www.django-rest-framework.org/)  
- [💳 Stripe API](https://stripe.com/docs/api)

