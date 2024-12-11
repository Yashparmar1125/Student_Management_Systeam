# Student Management System

## Overview
The **Student Management System (SMS)** is an advanced web application aimed at streamlining classroom management processes. It enhances communication between students, teachers, and school administration while simplifying administrative tasks. SCMS is designed to improve the efficiency and effectiveness of educational institutions through innovative tools and user-friendly features.

---

## Key Features

### **User Roles and Capabilities**
1. **Students**
   - Access personalized schedules and calendars.
   - View assignments, deadlines, and results.
   - Track attendance records.

2. **Teachers**
   - Manage class attendance efficiently.
   - Assign and track homework and assignments.
   - Record and manage student results.

3. **School Management**
   - Add, modify, and delete classes.
   - Create and update class schedules.
   - Oversee system-wide activities and user management.

### **Core Functionalities**
1. **User Authentication**
   - Secure login for Students, Teachers, and School Management roles.

2. **Administrative Tools**
   - Comprehensive control for school administrators to manage academic and operational workflows.

3. **Teacher Tools**
   - Attendance marking and tracking.
   - Assignment and homework management.
   - Student performance monitoring.

4. **Student Dashboard**
   - Access to academic schedules, assignments, and results.
   - Real-time updates on attendance and deadlines.

---

## Installation Guide

Follow the steps below to set up and run the SCMS locally:

### **1. Clone the Repository**
```bash
git clone https://github.com/Yashparmar1125/Student_Management_System.git
```

### **2. Navigate to the Project Directory**
```bash
cd scms
```

### **3. Set Up a Virtual Environment**
Create and activate a virtual environment to manage dependencies.

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**For macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **4. Install Dependencies**
Install all required Python packages using `pip`:
```bash
pip install -r requirements.txt
```

### **5. Apply Database Migrations**
Set up the database by applying migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### **6. Run the Development Server**
Start the application on your local machine:
```bash
python manage.py runserver
```

Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Technologies Used
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default), with options for PostgreSQL or MySQL
- **Version Control**: Git

---

## Contributing
We welcome contributions to enhance the SCMS! Follow these steps to contribute:

1. Fork the repository.
2. Create a new feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact
For any queries or support, feel free to reach out:
- **Author**: Yash Parmar
- **GitHub**: [https://github.com/Yashparmar1125](https://github.com/Yashparmar1125)
- **Email**: [yashparmar11y@gmail.com](mailto:yashparmar11y@gmail.com)

We hope you enjoy using the Smart Classroom Management System!

