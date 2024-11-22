---

# **Venue Booking System**

Welcome to the **Venue Booking System** repository! This application allows users to securely book venues like tutorial rooms, classrooms, boardrooms, and auditoriums. It's designed to be intuitive and efficient, while also ensuring that administrators can manage bookings effectively. 

This project utilizes a secure login system, password hashing, and robust database management to make venue booking smooth for all users. Whether you're an admin or a regular user, this system has features tailored to your needs.

## **Table of Contents**
1. [About the Project](#about-the-project)
2. [Tech Stack](#tech-stack)
3. [Features](#features)
4. [Database Schema](#database-schema)
5. [Setup and Installation](#setup-and-installation)
6. [Usage](#usage)
7. [How to Contribute](#how-to-contribute)
8. [License](#license)

---

## **About the Project**

This **Venue Booking System** is a web-based application that allows users to log in, select a venue, choose a time, and submit a booking request for approval by the admin. It ensures that booking data is well-managed, past bookings are archived, and real-time availability is tracked for each venue.

Key Features:
- **User Authentication**: Users can securely log in with password hashing.
- **Venue Booking**: Choose from various venues and times, and submit a request.
- **Admin Console**: Manage bookings, approve or deny requests, and view past bookings.
- **Database Management**: Uses MySQL for data storage and queries.

The system is designed using Python with **Tkinter** for the front end, **MySQL** for the database backend, and **bcrypt** for password hashing.

---

## **Tech Stack**

- **Frontend**: 
    - Python (with Tkinter for GUI)
    - CustomTkinter (for modern UI elements)
- **Backend**:
    - MySQL (for storing user data, bookings, and venues)
    - Python (for backend logic)
- **Database**:
    - MySQL database to store user data, venue details, and booking records.
    - `bcrypt` for password hashing and validation.
- **Libraries**:
    - `customtkinter` (for customizable UI components)
    - `mysql.connector` (to interact with MySQL)
    - `tkinter` (for building the application’s interface)

---

## **Features**

1. **Login Page**:
    - Users log in with their **user ID** and **password**.
    - Admin users and regular users have different privileges.
    - Passwords are securely hashed before storing in the database for security.

2. **User Console**:
    - After login, users can view their **current bookings**.
    - Users can submit new booking requests for venues.

3. **Admin Console**:
    - Admins can **approve** or **deny** booking requests.
    - Admins can view all **past bookings** and archive old data.
    - Admins can easily manage venue availability and bookings.

4. **Venue Booking**:
    - Users can select a venue, choose a time slot, and submit a booking request.
    - The application validates the booking time against existing bookings for conflicts.

5. **Secure Data Storage**:
    - User credentials (passwords) are securely stored using `bcrypt` hashing.
    - All other data is stored in MySQL and can be queried and modified through the application.

---

## **Database Schema**

The project uses a **MySQL** database with the following key tables:

### 1. **Users**
Stores user information such as login credentials and roles.

| Column Name | Type                | Description                                  |
|-------------|---------------------|----------------------------------------------|
| user_id     | varchar(10)          | Primary Key, Unique User ID                 |
| user_name   | varchar(50)          | User’s full name                             |
| pswd        | varchar(255)         | Hashed password                              |
| email_id    | varchar(60)          | Unique email ID                             |
| role        | enum('user', 'admin')| Role (either 'user' or 'admin')             |

### 2. **Venues**
Stores details of each venue available for booking.

| Column Name  | Type                                                                 | Description                                           |
|--------------|----------------------------------------------------------------------|-------------------------------------------------------|
| venue_id     | varchar(4)                                                           | Primary Key, Unique Venue ID                         |
| venue_name   | varchar(50)                                                          | Venue name (e.g., Auditorium, Classroom)             |
| type         | enum('Classroom', 'Auditorium', 'Lecture Theatre', 'Tutorial Room', 'Meeting Room', 'Laboratory') | Type of venue (classroom, auditorium, etc.)          |
| capacity     | smallint                                                             | Venue seating capacity                               |
| location     | varchar(50)                                                          | Venue location (e.g., building, floor)               |

### 3. **Booking Requests**
Tracks the booking requests made by users.

| Column Name  | Type                                  | Description                                            |
|--------------|---------------------------------------|--------------------------------------------------------|
| booking_id   | int                                   | Primary Key, Unique Booking ID                         |
| user_id      | varchar(10)                           | Foreign Key to `Users`                                 |
| venue_id     | varchar(4)                            | Foreign Key to `Venues`                                |
| date         | date                                  | Date of the booking                                   |
| start_time   | time                                  | Start time of the booking                              |
| end_time     | time                                  | End time of the booking (optional)                     |
| status       | enum('pending', 'approved', 'rejected')| Booking status (pending, approved, rejected)           |

### 4. **Booking Logs**
Stores past booking data for archival purposes.

| Column Name  | Type                                  | Description                                            |
|--------------|---------------------------------------|--------------------------------------------------------|
| log_id       | int                                   | Primary Key, Unique Log ID                             |
| user_id      | varchar(10)                           | Foreign Key to `Users`                                 |
| venue_id     | varchar(4)                            | Foreign Key to `Venues`                                |
| booking_date | date                                  | Date of the booking                                   |
| start_time   | time                                  | Start time of the booking                              |
| end_time     | time                                  | End time of the booking                                |
| status       | enum('Expired', 'Canceled')           | Status of the booking log (Expired, Canceled)          |

### 5. **Approved Bookings**
Stores data on approved booking requests.

| Column Name  | Type                                  | Description                                            |
|--------------|---------------------------------------|--------------------------------------------------------|
| approval_id  | int                                   | Primary Key, Unique Approval ID                        |
| admin_id     | varchar(10)                           | Foreign Key to `Users` (admin who approved the booking)|
| approval_date| date                                  | Date of approval                                      |
| user_id      | varchar(10)                           | Foreign Key to `Users`                                 |
| venue_id     | varchar(4)                            | Foreign Key to `Venues`                                |
| booking_date | date                                  | Date of the booking                                   |
| start_time   | time                                  | Start time of the booking                              |
| end_time     | time                                  | End time of the booking (optional)                     |
| status       | enum('Approved', 'Rejected')          | Status of the approved booking (Approved, Rejected)    |
| comments     | varchar(1024)                         | Optional comments on the booking approval              |

---

## **Setup and Installation**

Follow the steps below to set up the **Venue Booking System** locally:

### 1. **Clone the Repository**
Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/venue-booking-system.git
```

### 2. **Install Dependencies**
Ensure you have **Python 3.x** installed. Then install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 3. **Database Setup**
- Install **MySQL** and create a database named `venue_booking_system`.
- Create the necessary tables as per the schema above.
  
Run the following script to set up your MySQL database:
```sql
CREATE DATABASE venue_booking_system;
USE venue_booking_system;

-- Create Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    pswd VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- Create Venues Table
CREATE TABLE venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    capacity INT,
    location VARCHAR(100)
);

-- Create Bookings Table
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    venue_id INT,
    booking_date DATE,
    start_time TIME,
    end_time TIME,
    status VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
);

-- Create Booking Logs Table
CREATE TABLE booking_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT,
    timestamp DATETIME,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);
```

### 4. **Configure Database Connection**
In the Python code, ensure that the **MySQL credentials** in the `common.py` file are correctly set to your local MySQL database connection.

---

## **Usage**

1. **Run the Application**
    - Run the Python script to start the login page:
    ```bash
    python login_page.py
    ```
    - Follow the prompts to log in as a user or admin.

2. **Admin Features**
    - Admin users can approve or deny booking requests and view past bookings.

3. **User Features**
    - Users can view their current bookings and make new booking requests.

---

## **How to Contribute**

We welcome contributions to the **Venue Booking System**! Here’s how you can contribute:

1. Fork the repository.
2. Clone your fork to your local machine.
3. Create a new branch:
    ```bash
    git checkout -b feature-branch
    ```
4. Make your changes and commit:
    ```bash
    git commit -m "Add new feature"
    ```
5. Push your changes:
    ```bash
    git push origin feature-branch
    ```
6. Create a pull request to the main repository.

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Thank you for checking out the Venue Booking System!** We hope this project helps simplify venue booking and management. Feel free to contribute and make it better! 😄

---
