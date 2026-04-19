# Gym Management System (gym_site)

A professional Django-based application designed to manage gym memberships, user profiles, and subscription plans.

## 🚀 Project Overview
This project provides a robust backend for a fitness center, allowing for the management of:
- **User Authentication:** Secure registration and login.
- **Membership Management:** Different tiers (Basic, Premium, VIP).
- **Profile Customization:** Personalized user details and activity tracking.

## 🛠️ Tech Stack
- **Backend:** Python 3.x, Django
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **Frontend:** Django Templates, HTML5, CSS3, Bootstrap

## 📂 Project Structure
```text
gym_site/
├── accounts/              # App for users, profiles, and memberships
│   ├── services/          # Business logic layer
│   ├── models.py          # Database schema
│   └── ...
├── gym_site/              # Project configuration folder
│   ├── settings.py        # Main Django settings
│   └── urls.py            # Project-level URL routing
├── templates/             # Global HTML templates
├── manage.py              # Django management script
└── README.md              # Project documentation
```

## ⚙️ Setup and Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd gym_site
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv .venv
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install django
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Start the Development Server
```bash
python manage.py runserver
```
Access the app at `http://127.0.0.1:8000/`

## 📝 Roadmap
- [ ] Implement JWT Authentication
- [ ] Integrate Stripe for Membership Payments
- [ ] Create Trainer Dashboard
- [ ] Implement Workout Logging API