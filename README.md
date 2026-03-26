# Secure Authentication System

## Overview

This project demonstrates a secure authentication system using Flask and JWT with role-based access control and security testing.

## Features

* User Registration & Login
* JWT Authentication
* Role-Based Access (Admin/User)
* Protected Routes
* XSS Testing
* Token Manipulation Testing

## Tech Stack

* Python (Flask)
* HTML, CSS, JavaScript
* SQLite
* Postman

## Setup

1. Clone repo
2. Install dependencies
3. Run `python app.py`
4. Open frontend in browser

## 📸 Screenshots

### 🔹 Registration API

<img width="1551" height="901" alt="image" src="https://github.com/user-attachments/assets/b8b13b47-133b-4bb4-8138-3010168c15dc" />

### 🔹 Login with JWT

<img width="1522" height="916" alt="image" src="https://github.com/user-attachments/assets/48ebbc49-7328-4a35-a9ec-f38a90763c3c" />

### 🔹 Dashboard (Role-based)

<img width="1919" height="851" alt="image" src="https://github.com/user-attachments/assets/af3f2351-3277-414f-ae80-8e56cd8b98cd" />

### 🔹 XSS Test

<img width="940" height="552" alt="image" src="https://github.com/user-attachments/assets/d89d4970-6412-49c9-a5e9-9687eb7bf370" />


### 🔹 SQL Injection Test

<img width="940" height="536" alt="image" src="https://github.com/user-attachments/assets/7e55c315-ef1b-45ca-9c1f-b3889401fef3" />


##  Challenges Faced & Solutions

* JWT token issues → Fixed encoding/decoding
* Role assignment issue → Added role in backend
* Unauthorized access → Implemented RBAC
* XSS vulnerability → Input sanitization
* Token tampering → Backend validation added


## Security Testing

* XSS attack testing
* Token tampering prevention

## Conclusion

This project demonstrates secure authentication and common vulnerability handling.
