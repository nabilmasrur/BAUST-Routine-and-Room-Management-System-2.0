# BAUST-Routine-and-Room-Management-System-2.0
# BAUST Routine and Room Management System 2.0

A comprehensive web-based solution designed for **Bangladesh Army University of Science and Technology (BAUST)** to streamline the process of academic routine creation and classroom allocation.

## 📌 Project Overview
Managing university routines and vacant rooms manually can be complex and prone to errors. This system automates the scheduling process, ensuring that there are no overlaps in teacher schedules or room bookings. It provides an intuitive interface for administrators to manage courses, teachers, and time slots efficiently.

## ✨ Key Features
* **Automated Routine Generation:** Simplifies the creation of weekly academic schedules.
* **Conflict Detection:** Prevents double-booking of teachers and classrooms in the same time slot.
* **Teacher Management:** Dedicated module to assign teachers to specific courses and view their individual schedules.
* **Room Allocation:** Tracks room availability and manages classroom resources effectively.
* **Interactive Admin Dashboard:** A centralized panel for full control over departments, batches, and sessions.
* **Responsive UI:** User-friendly frontend built for seamless navigation on both desktop and mobile.

## 🛠️ Tech Stack
* **Backend:** Python (Django Web Framework)
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS/jQuery)
* **Database:** SQLite3 (Default for development)
* **Tools:** Git & GitHub for Version Control

## 🚀 Getting Started

### Prerequisites
Make sure you have Python installed on your system.

### Installation
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/nabilmasrur/BAUST-Routine-and-Room-Management-System-2.0.git](https://github.com/nabilmasrur/BAUST-Routine-and-Room-Management-System-2.0.git)
    cd BAUST-Routine-and-Room-Management-System-2.0
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    * **Windows:** `venv\Scripts\activate`
    * **Mac/Linux:** `source venv/bin/activate`

4.  **Run Database Migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Start the Development Server:**
    ```bash
    python manage.py runserver
    ```
    Now, visit `http://127.0.0.1:8000/` in your browser.

## 📂 Project Structure
* `backend/`: Contains Django logic, models, and API views.
* `frontend/`: Contains HTML templates and CSS/JS assets.
* `database/`: Local storage for the system data.

## 👨‍💻 Author
**Nabil Masrur**
* GitHub: [@nabilmasrur](https://github.com/nabilmasrur)
