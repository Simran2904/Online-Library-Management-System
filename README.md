# 📚 Online Library Management System

An Online Library Management System developed using **Python Flask, HTML, CSS, JavaScript, and MySQL**. This web-based application allows students to explore books, search for books, view book details, manage their profiles, and keep track of their borrowed books.

## 🚀 Features

### Student Side
- Student Registration and Login
- Student Dashboard
- Browse and Explore Books
- Search Books by Title or Author
- View Detailed Book Information
- My Books Section
- Student Profile Management
- Background Images and Responsive UI

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| HTML5 | Website Structure |
| CSS3 | Styling and Design |
| JavaScript | Frontend Interactivity |
| Python | Backend Programming |
| Flask | Web Framework |
| MySQL | Database Management |
| MySQL Connector | Database Connectivity |

## 📁 Project Structure

```text
Online Library Management System/
│
├── app.py
├── config.py
├── db_connection.py
├── requirements.txt
├── test.py
├── profile.jpeg
│
├── database/
│   ├── library_db.sql
│   └── sample_books.sql
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── images/
│       ├── 1.jpeg
│       ├── 2.jpeg
│       ├── 3.jpeg
│       ├── 4.jpeg
│       ├── home_bg.jpeg
│       └── profile.jpg
│
└── templates/
    ├── index.html
    ├── login.html
    ├── register.html
    │
    └── student/
        ├── dashboard.html
        ├── view_books.html
        ├── book_details.html
        ├── my_books.html
        └── profile.html
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Simran2904/Online-Library-Management-System.git
```

### 2. Navigate to the Project Folder

```bash
cd Online-Library-Management-System
```

### 3. Install Required Packages

```bash
py -m pip install -r requirements.txt
```

### 4. Setup MySQL Database

- Open MySQL Community Server.
- Open MySQL Workbench or MySQL Command Line Client.
- Execute the SQL file `database/library_db.sql`.
- Execute `database/sample_books.sql` to insert sample book records.
- Configure your MySQL database credentials in `config.py` or your database connection settings.

### 5. Run the Flask Application

```bash
py app.py
```

### 6. Open in Browser

```text
http://127.0.0.1:5000/
```

## 🗄️ Database

The application uses **MySQL** to store and manage library-related information, including student and book records.

Database initialization files are available in the `database` folder.

## 🎯 Project Objective

The main objective of this project is to develop a simple and user-friendly online library platform that makes it easier for students to browse books and manage their library activities digitally.

## 👩‍💻 Developed By

**Simran**

GitHub: [@Simran2904](https://github.com/Simran2904)

## 📌 Future Enhancements

- Admin Dashboard
- Book Issue and Return Management
- Fine Calculation
- Book Availability Tracking
- Advanced Search and Filtering
- Email Notifications

---

⭐ If you find this project useful, consider giving the repository a star!
