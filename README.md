# Smart Classroom Management System

## Overview
The Smart Classroom Management System is a web application designed to facilitate the management of classroom activities, enhance communication among students, teachers, and school management, and streamline various administrative tasks.

## Features

### Users of the System
- **Students**: Access their schedules, assignments, and attendance.
- **Teachers**: Manage class activities, attendance, and assignments.
- **School Management**: Oversee the entire system, including classes and schedules.

### Project Features
1. **User Authentication**
   - Login page for all three user roles (Students, Teachers, School Management).

2. **School Management Functions**
   - Ability to add, delete, and modify classes.
   - Create and alter class schedules.

3. **Teacher Functions**
   - Mark student attendance.
   - Assign homework and assignments.
   - Mark and manage student results.

4. **Student Functions**
   - View personal calendars and schedules.
   - Check assignment deadlines and results.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Yashparmar1125/SCMS_FINAL.git
   
2. Navigate to the project directory:
   ```bash
   cd scms

3. Create a Virtual Env:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
 
4. Install the required packages::
   ```bash
   pip install -r requirements.txt

5. Apply Database Migrations (in case of new database):
   ```bash
   python manage.py makemigrations
   python manage.py migrate

6. Run Devlopment Server:
   ```bash
   python manage.py runserver
   




