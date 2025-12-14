# Champions API (Flask + MySQL)

## 📌 Project Overview

This project is a **RESTful API** built using **Flask** and **MySQL** that manages game champions data. It supports full **CRUD operations**, **search functionality**, **JWT-based authentication**, and **multiple response formats (JSON / XML)**.

This project was developed as part of an academic drill focusing on API design, security, testing, and documentation best practices.

---

📌 Project Features

CRUD operations for champions

MySQL database integration

Input validation & error handling

JSON and XML response formats

Search functionality with filters

JWT authentication for protected routes

Automated unit tests

API tested using Postman

## 🛠️ Technologies Used

* Python 3
* Flask
* MySQL
* flask-mysqldb
* flask-jwt-extended (JWT Authentication)
* dicttoxml
* unittest (API testing)
* Postman (API testing & demo)

---

## 📂 Project Structure

```
Final_CSelect/
│── app.py              # Main Flask application
│── test_app.py         # Unit tests for CRUD & search
│── requirements.txt    # Python dependencies
│── README.md           # Project documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone
cd Final_CSelect
```

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv project
project\Scripts\activate   
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure MySQL Database

Create a MySQL database named:

```
game
```

Example `champions` table:

```sql
CREATE TABLE champions (
  championid INT AUTO_INCREMENT PRIMARY KEY,
  champion_name VARCHAR(100),
  roleid INT,
  difficulty_level VARCHAR(50)
);
```

> ⚠️ Note: Some champions may be referenced by other tables (e.g., `matches`), which may prevent deletion due to foreign key constraints.

---

## ▶️ Running the Application

```bash
python app.py
```

The API will run at:

```
http://127.0.0.1:5000
```

---

## 🔐 Authentication (JWT)

Some endpoints are **protected** using JWT.

### Login Endpoint

**POST** `/login`

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**

```json
{
  "access_token": "<JWT_TOKEN>"
}
```

### Using the Token

Include this header in protected requests:

```
Authorization: Bearer <JWT_TOKEN>
```

---

## 📡 API Endpoints

### 🔹 Get All Champions

**GET** `/champions`

Optional format:

```
/champions?format=xml
```

---

### 🔹 Get Champion by ID

**GET** `/champions/<id>`

---

### 🔹 Create Champion (JWT Required)

**POST** `/champions`

```json
{
  "champion_name": "Teemo",
  "roleid": 2,
  "difficulty_level": "easy"
}
```

---

### 🔹 Update Champion (JWT Required)

**PUT** `/champions/<id>`

```json
{
  "champion_name": "Teemo Updated",
  "roleid": 2,
  "difficulty_level": "medium"
}
```

---

### 🔹 Delete Champion (JWT Required)

**DELETE** `/champions/<id>`

Possible responses:

* `200` Deleted successfully
* `404` Champion not found
* `400` Cannot delete due to foreign key constraint

---

### 🔎 Search Champions

**GET** `/champions/search`

Query Parameters:

* `name`
* `roleid`
* `difficulty_level`
* `format=json | xml`

Example:

```
/champions/search?name=Teemo&format=xml
```

---

## 🧪 Running Tests

Run all unit tests:

```bash
python -m unittest test_app.py
```

All CRUD, search, and error-handling scenarios are covered.

---

## 📬 Using Postman

1. Login via `/login` to get JWT token
2. Add `Authorization: Bearer <token>` header
3. Test CRUD, search, and XML/JSON responses

---

## 📌 Notes

* Default response format is **JSON**
* XML format available using `?format=xml`
* JWT protects CREATE, UPDATE, DELETE routes
* Proper HTTP status codes are returned for all operations

---

## 👤 Author

**Scott Franklin T. Maher**

---

