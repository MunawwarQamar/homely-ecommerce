# 🏠 Homely | Full-Stack E-Commerce Web Application

> A modern full-stack e-commerce platform for home products, built as a **solo project** during the Full Stack Bootcamp at **AXSOS Academy**.

🌐 **Live Demo:** https://homely-ecommerce.onrender.com/

---

# 📖 Project Overview

Homely is a complete web-based e-commerce application that simulates a real-world online shopping experience for home products.

The platform allows users to browse products by category, search items, manage their shopping cart, and communicate with the store through a contact system.

On the admin side, the system provides a custom dashboard for managing products, uploading images, monitoring customer messages, and controlling store content efficiently.

The project focuses on:

- Clean and responsive UI/UX
- Real-world functionality
- Full-stack architecture
- Admin vs User system roles
- Secure and scalable backend logic

---

# 🧠 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python / Django | Backend framework |
| MySQL | Database management |
| Bootstrap 5 | Responsive frontend UI |
| HTML / CSS | Interface structure & styling |
| JavaScript | Frontend interactions |
| AJAX | Dynamic cart updates |
| Pillow | Image handling |
| SMTP (Gmail) | Email functionality |
| Git & GitHub | Version control |
| Render | Deployment |

---

# 📡 API Endpoint

```bash
/api/products/
```

Returns product data in JSON format.

---

# 🖼️ Screenshots

| Home | Products | Cart |
|------|----------|------|
| ![Home](Screenshots/home.png) | ![Products](Screenshots/products.png) | ![Cart](Screenshots/cart.png) |

| Admin Dashboard | Admin Products | Messages |
|-----------------|----------------|----------|
| ![Admin](Screenshots/admin-dashboard.png) | ![Admin Products](Screenshots/admin-products.png) | ![Messages](Screenshots/messages.png) |

---

# ⚙️ Installation & Setup

## 1. Clone Repository

```bash
git clone https://github.com/MunawwarQamar/homely-ecommerce.git
cd homely_project
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv env
env\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv env
source env/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run Database Migrations

```bash
python manage.py migrate
```

---

## 5. Run Development Server

```bash
python manage.py runserver
```

---

# 👥 System Roles

## User

- Browse and search products
- Add products to cart
- Contact the store

## Admin

- Manage products
- Manage customer messages
- Control store content

---

# 🚧 Future Improvements

Planned future enhancements include:

- Online payment integration
- Wishlist system
- Order tracking
- Product reviews and ratings
- Advanced filtering and sorting
- User profile management

---

# 👩‍💻 Author

## Munawwar Qamar
Full Stack Developer  

---

# 📄 Educational Note

This project was built for educational and portfolio purposes as part of the AXSOS Academy Full Stack Bootcamp.
