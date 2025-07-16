# Raahnuma – University Guidance System

**Raahnuma** is a comprehensive university guidance system built using **SQL Server** for backend and **Python** for frontend integration. The system is designed to assist students in exploring academic programs across universities in Pakistan, viewing eligibility, fee structures, timelines, and saving programs for future reference. It also features role-based access, notifications, real-time chat, and data logging mechanisms for administrative insights.

---

## 📁 Project Structure

* **SQL Server (Database)**: Core data storage, relational modeling, indexing, stored procedures, views, and triggers.
* **Python (Frontend/API)**: Provides interaction between users and database via UI (e.g., Flask, Tkinter, or Streamlit).

---

## 🔢 Key SQL Components

### 🏢 Database Schema Highlights:

* `University`, `Program`, `Eligibility`, `FeeStructure`, `AdmissionDates`, `Subject`, `Timeline`
* `User`, `Role`, `RolePermission`, `Filter`, `SavedPrograms`, `Notification`, `ChatGroup`, `ChatMessage`

### ⚡ Key Functionalities:

* **Referential Integrity** using `FOREIGN KEY` constraints
* **Business Logic Enforcement** using:

  * `CHECK` constraints (e.g., duration range, fee non-negativity)
  * `TRIGGERS` to handle logging, archiving, and automatic notifications
* **Advanced Data Management**

  * `Stored Procedures`: Reusable SQL logic for filtering, saving, and managing data
  * `Views`: Simplified representations (including materialized and indexed views)
  * `Indexes`: Performance-optimized searches on critical fields

---

## 🔧 Python Integration

Python connects to the SQL Server backend using libraries such as:

* `pyodbc` / `pymssql` for database connectivity
* `Flask` or `Streamlit` for frontend user experience
* `Jinja2` templating (for web apps)

### Frontend Features:

* **Login/Register UI** (linked to `User`, `Role` tables)
* **Search & Filter** programs by city, degree, and tags
* **Save Programs** with feedback from backend triggers
* **View Notifications**, timelines, and fee structures
* **Join Chat Groups**, post messages, and track last activity
* **Role-Based Access Control** enforced via stored procedures and `RolePermission` table

---

## 🏆 Highlights

* ✅ Fully normalized schema
* 🔒 Role-based access (admin vs student)
* ✨ Trigger-driven automation
* ⚖️ Real-world universities & programs pre-populated
* 🎓 Designed for extensibility and scalability

---

## 📊 How to Use

1. Run SQL script to set up the full database
2. Connect via Python frontend
3. Browse, search, filter, save, and interact with academic data
4. Admins can manage structure, log changes, and view historical data

---

## 👤 Author

**Maha Rauf**
BS Computer Science, 5th Semester
---

> For demo purposes or collaboration, feel free to fork this repo or contribute with enhancements!
