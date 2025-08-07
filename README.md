♻️ RVM Project – Recycle Rewards API
This project implements a Reverse Vending Machine (RVM) API that allows users to:

Register/login with authentication tokens

Log recyclable material deposits (plastic, glass, metal)

Earn reward points based on material and weight

View a summary of their recycling activity

📁 Project Structure
rvm_project/
├── rvm_app/              # Your main app (models, views, urls)
│   ├── models.py         # User, RVM machine, Deposit models
│   ├── views.py          # Register, login, deposit, summary views
│   ├── serializers.py    # DRF serializers
│   └── urls.py           # App-level URLs
├── rvm_project/
│   └── urls.py           # Project-level URL routing
├── db.sqlite3            # Default SQLite database
└── manage.py
