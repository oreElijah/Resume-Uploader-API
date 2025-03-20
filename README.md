# 👤 Resume Uploader API

A FastAPI-based project that allows users to upload resumes. It includes authentication, email confirmation, role-based access control, and file management.

## 🚀 Features

- **User Authentication** (Registration, Login, Logout)
- **Role-Based Access Control** (Worker & Hirer roles)
- **Profile Picture Upload**
- **Resume Upload & Management**
- **Database Integration** (PostgreSQL with SQLAlchemy)

## 🛠️ Technologies Used

- **FastAPI** - Web framework
- **PostgreSQL** - Database storage
- **SQLAlchemy** - ORM for database interaction
- **Pydantic** - Data validation
- **JWT Authentication** - Secure API authentication
- **Role-Based Access Control** - Restrict access based on user roles

## 📂 Folder Structure

## 🔑 **User Roles**

- **Worker**: Can upload & delete their own resume.
- **Hirer**: Can view resumes of other users.

## 🛋️ **API Endpoints**

### **User Authentication**

- `POST /user/register` - Register a new user
- `POST /user/login` - Authenticate and get a token

### **Profile Management**

- `POST /user/upload_profile_picture` - Upload a profile picture

### **Resume Management**

- `POST /resume/upload_resume` - Upload a resume (Workers only)
- `GET /resume` - View all resumes (Hirers only)

## 📝 **How to Use**

### 1️⃣ **Setup & Install Dependencies**

### 2️⃣ **Run the Application**

### 3️⃣ **Test API Endpoints**

- Open **Postman** or **FastAPI Swagger UI** (`http://127.0.0.1:8000/docs`)
- Use **Bearer Token Authentication** for secured routes

## 🎯 **Future Improvements**

- Add resume downloading route 
---

### **👤 Author**

**Elijah**📧 [oreelijah33@gmail.com](mailto:oreelijah33@gmail.com)

---
