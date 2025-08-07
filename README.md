### ♻️ RVM Project – Recycle Rewards API
- This project implements a Reverse Vending Machine (RVM) API that allows users to:

- Register/login with authentication tokens

- Log recyclable material deposits (plastic, glass, metal)

- Earn reward points based on material and weight

- View a summary of their recycling activity

### 🚀 Features
- ✅ Custom user model using AbstractUser with added fields

- 🔐 Token-based authentication

- ♻️ Track recyclable material deposits

- 🏅 Auto-calculate points and update totals

- 📊 User summary: total points, weight, favorite material


### 🛠 Tech Stack
- Python 3.11+

- Django 5.2.5

- Django REST Framework

- Token Authentication

- SQLite3 (default, can change to PostgreSQL)


### API Endpoints , testing in postman 

| Endpoint                | Method | Auth | Description                  |
|-------------------------|--------|------|------------------------------|
| `/api/auth/register/`  | POST   | ❌   | Register a new user          |
| `/api/auth/login/`     | POST   | ❌   | Login and get token          |
| `/api/deposits/`       | POST   | ✅   | Log a new material deposit   |
| `/api/user/summary/`   | GET    | ✅   | View your recycling stats    |


### 📦 Installation
- 1.Clone the repo
<pre lang="markdown">bash git clone https://github.com/FatimaaAlzahraa/rvm_project.git 
cd rvm_project </pre>

- 2.Create and activate a virtual environment
<pre lang="markdown">python -m venv venv
venv\Scripts\activate  # On Mac use source venv/bin/activate </pre>

- 3.Install dependencies
<pre lang="markdown">pip install -r requirements.txt </pre>

- 4.Run migrations
<pre lang="markdown">python manage.py makemigrations
python manage.py migrate </pre>

- 5.Create superuser (optional)
<pre lang="markdown"> python manage.py createsuperuser </pre>

- 6.Run the server
<pre lang="markdown"> python manage.py runserver </pre>

### 🔐 Authentication
**This project uses DRF Token Authentication.** 
- After registering or logging in, you will receive a token.
- Use it in your headers for all authenticated API calls:
<pre lang="markdown"> Authorization: Token <your_token_here> </pre>

#### 📥 Register User
<pre lang="markdown"> POST  http://127.0.0.1:8000/api/auth/register/ </pre>

<pre lang="markdown">
{
  "username": "example",
  "email": "test@example.com",
  "password": "testpass123",
  "password_confirm": "testpass123",
  "phone_number": "0123456789"
}
 </pre>