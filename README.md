# 🛒 Homely - E-commerce Web Application

Homely is a full-stack e-commerce web application built using Django as part of a **solo project** during the Full Stack Bootcamp at **AXSOS Academy**.

The goal of this project is to simulate a real-world online store with both **user-side functionality** and a fully functional **admin dashboard**, focusing on clean UI/UX, security, and dynamic interactions.

---

## 🚀 Features

### 👤 User Features
- User registration and login system
- Browse products by category
- Search for products
- View product details
- Add to cart and update cart dynamically (AJAX)
- Contact form with email confirmation

---

### 🛠️ Admin Features
- Admin dashboard with statistics
- Add new products
- Edit existing products
- Archive products (soft delete)
- View and manage contact messages
- Mark messages as read

---

## 🧠 Technologies Used

- Backend: Django (Python)
- Database: MySQL
- Frontend: HTML, CSS, Bootstrap
- Dynamic Updates: AJAX (Fetch API)
- Authentication: Session-based auth + password hashing
- Email Integration: SMTP (Gmail)

---

## 🔐 Security Features

- CSRF Protection
- Password Hashing
- Form Validation
- Image Upload Validation (only images allowed)

---

## 📡 API Endpoint

/api/products/

Returns all products in JSON format.

---

## 📸 Screenshots

(Add your screenshots here inside a folder named screenshots)

Example:
![Home](screenshots/home.png)
![Products](screenshots/products.png)
![Cart](screenshots/cart.png)
![Admin](screenshots/admin.png)
![Messages](screenshots/messages.png)

---

## ⚙️ Installation

1. Clone the repository:
git clone https://github.com/your-username/homely.git
cd homely

2. Create virtual environment:
python -m venv venv
venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Run migrations:
python manage.py migrate

5. Run server:
python manage.py runserver

---

## 🎯 Project Purpose

This project was developed as a **solo educational project** during the AXSOS Full Stack Bootcamp.

It demonstrates:
- Full-stack development skills
- Real-world system design
- UI/UX implementation
- Admin vs User role management

---

## 👩‍💻 Author

Munawwar Qamar  
Frontend & Full Stack Developer

---

## ⭐ Notes

- This project is for educational purposes.
- Future improvements may include payment integration and order tracking.
