# 🏛️ CampusFix

> **Smart College Issue & Complaint Management System**
>
> A role-based Streamlit application for reporting, tracking, assigning, resolving, and analyzing campus maintenance and service issues through a centralized workflow.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00)](https://www.sqlalchemy.org/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Analytics-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)

CampusFix turns scattered campus complaints into a structured service-management workflow. Students can submit issues with evidence, staff can work on assigned tickets, and administrators can monitor operations through KPIs, charts, staff workload metrics, and CSV reports.

---

## ✨ Why CampusFix?

Campus maintenance issues are often reported through informal channels such as messages, calls, paper forms, or verbal communication. That makes it difficult to answer basic operational questions:

- What issues are currently open?
- Who is responsible for a particular issue?
- Where was the issue reported?
- How long did resolution take?
- Was the student satisfied with the resolution?
- Which categories generate the most complaints?

**CampusFix provides one workflow for the complete complaint lifecycle:**

```text
Student reports issue
        ↓
Ticket is created
        ↓
Admin reviews / assigns staff
        ↓
Staff investigates and updates status
        ↓
Resolution is recorded
        ↓
Student reviews the outcome
        ↓
Rating + feedback
        ↓
Admin analytics & reports
```

---

## 🚀 Core Features

### 🎓 Student Portal

- Student registration and login
- Submit a new campus complaint
- Select complaint category and priority
- Provide exact issue location
- Add detailed issue description
- Upload optional evidence photos
- View only the student's own complaints
- Search complaints by ID, title, description, or location
- Filter complaints by status and category
- View assigned technician/staff information
- Follow a complaint's resolution timeline
- Participate in public complaint discussions
- Rate resolved complaints from 1–5
- Add satisfaction feedback
- Reopen a resolved complaint with a reason

### 🛠️ Staff Workspace

- Role-specific staff dashboard
- View assigned and unassigned work available to the staff workflow
- Search and filter complaint tickets
- Filter by priority and status
- Inspect complaint details and uploaded evidence
- Update ticket status
- Add mandatory status/resolution notes
- View the complete status audit timeline
- Post public responses
- Add staff-only internal notes
- See student satisfaction ratings and feedback

### 👑 Admin Command Center

- System-wide complaint KPIs
- Total complaints monitoring
- Active/pending workload tracking
- Resolution-rate calculation
- Average resolution SLA calculation
- Complaint category visualization
- Priority distribution visualization
- Status distribution visualization
- Ticket assignment to staff members
- Staff account creation
- User directory
- Master complaint dataset view
- CSV report download
- Staff workload and satisfaction metrics

### 🔐 Authentication & Roles

CampusFix implements three application roles:

| Role | Main responsibility |
|---|---|
| **STUDENT** | Submit, track, discuss, rate, and reopen personal complaints |
| **STAFF** | Work on assigned tickets and update operational progress |
| **ADMIN** | Manage assignments, staff, users, analytics, and reports |

Passwords are hashed with **bcrypt**, while authenticated user information is maintained through Streamlit session state.

---

## 🧩 Complaint Lifecycle

A complaint can move through the following operational states:

```text
Submitted
   ↓
Under Review
   ↓
Assigned
   ↓
In Progress
   ↓
Resolved
```

A complaint may also be marked **Rejected** where appropriate. Resolved complaints can be reopened by the student, returning the ticket to an active workflow.

Every important status change is recorded in `ComplaintHistory`, creating an auditable timeline.

---

## 🗂️ Complaint Categories

The current configuration supports:

- Infrastructure
- Electrical
- Water
- Internet/Wi-Fi
- Hostel
- Library
- Classroom
- Transport
- Cleanliness
- Security
- Other

### Priority Levels

- **Low**
- **Medium**
- **High**
- **Critical**

---

## 🏗️ Architecture

CampusFix follows a lightweight layered architecture built around Streamlit, service modules, SQLAlchemy models, and an SQLite database.

```text
┌─────────────────────────────────────────────┐
│              Streamlit UI Layer             │
│                                             │
│ Auth View │ Student │ Staff │ Admin         │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│              Service Layer                  │
│                                             │
│ Complaint Service │ User Service             │
│ Analytics Service │ Utilities                │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│             Data / ORM Layer                │
│                                             │
│ SQLAlchemy Models + Session Management      │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│                 SQLite DB                   │
│                                             │
│ Users │ Complaints │ History │ Comments     │
└─────────────────────────────────────────────┘
```

---

## 🗄️ Data Model

The application models the core entities required for an issue-management system.

### `User`

Stores account and role information:

- Name
- Email
- Password hash
- Role
- Department
- Phone
- Account creation timestamp

### `Complaint`

Stores the main ticket:

- Complaint ID
- Student/creator
- Category and subcategory
- Title and description
- Location
- Priority
- Current status
- Assigned staff member
- Optional evidence image
- Satisfaction rating and feedback
- Reopen count
- Creation/update/resolution timestamps

### `ComplaintHistory`

Provides the audit trail for status changes, including:

- Complaint ID
- New status
- Status note
- User who made the change
- Timestamp

### `Comment`

Supports communication around a complaint:

- Complaint ID
- Author
- Message
- Public/internal visibility
- Timestamp

Relationships are implemented using SQLAlchemy ORM relationships and foreign keys.

---

## 📁 Project Structure

The application is organized around UI views, services, models, configuration, authentication, and shared UI utilities.

```text
CampusFix/
├── app.py                  # Streamlit application entry point
├── auth.py                 # Session authentication helpers
├── auth_view.py            # Login and student registration UI
├── admin_view.py           # Admin dashboard UI
├── staff_view.py           # Staff workspace UI
├── student_view.py         # Student portal UI
│
├── models.py               # SQLAlchemy ORM models
├── database.py             # Database engine, initialization and seed data
├── config.py               # Environment configuration and application constants
│
├── complaint_service.py    # Complaint creation, assignment and lifecycle logic
├── user_service.py         # Registration, authentication and user management
├── analytics_service.py    # KPIs, DataFrames and Plotly analytics
├── utils.py                # File upload, formatting and CSV utilities
│
├── styles.py               # Custom Streamlit CSS
├── ui_elements.py          # Reusable UI components
├── __init__.py
└── README.md
```

> **Repository note:** The current GitHub `main` tree contains these Python modules at the repository root, while several source files import them through `services.*` and `components.*` namespaces. If your local working copy is flattened in the same way as the GitHub tree, align the imports/package directories before deployment (for example, either restore the `services/` and `components/` packages or update the imports consistently). The README intentionally documents the architecture reflected by the source code rather than silently hiding this discrepancy.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Application development |
| **Streamlit** | Interactive web UI |
| **SQLAlchemy** | ORM and database access |
| **SQLite** | Default local database |
| **bcrypt** | Password hashing |
| **python-dotenv** | Environment configuration |
| **Pandas** | Data processing and report generation |
| **Plotly** | Interactive analytics charts |

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/DeekshithGowda1/CampusFix.git
cd CampusFix
```

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

The repository currently does not include a committed `requirements.txt`, so install the libraries used by the application:

```bash
pip install streamlit sqlalchemy bcrypt python-dotenv pandas plotly
```

For reproducible deployments, generate and commit a dependency file after validating the working environment:

```bash
pip freeze > requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DB_URL=sqlite:///./campusfix.db
SECRET_KEY=replace_with_a_long_random_secret
UPLOAD_DIR=./uploads
DEFAULT_ADMIN_EMAIL=admin@campusfix.edu
DEFAULT_ADMIN_PASS=change_this_password
APP_NAME=CampusFix
```

**Do not commit real credentials or secrets to Git.**

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL, normally similar to:

```text
http://localhost:8501
```

---

## 🧪 Demo Accounts

The current application seeds demonstration users when the database is empty. The authentication view also exposes quick demo-login buttons.

| Role | Email | Password |
|---|---|---|
| Student | `alex@student.edu` | `student123` |
| IT Staff | `staff.it@campusfix.edu` | `staff123` |
| Infrastructure Staff | `staff.infra@campusfix.edu` | `staff123` |
| Admin | `admin@campusfix.edu` | `admin123` |

> ⚠️ **Development/demo only:** These credentials are defined in the current demo-seeding flow and should not be used for a production deployment. Change or remove seeded credentials before exposing the application publicly.

---

## 📊 Analytics & KPIs

The administrator dashboard derives operational metrics from complaint data.

### Resolution Rate

```text
Resolved Complaints
──────────────────── × 100
Total Complaints
```

### Average Resolution SLA

For resolved complaints, CampusFix calculates the elapsed time between creation and resolution timestamps and reports the average in hours.

### Visual Reports

The analytics layer currently supports:

- Complaint category distribution
- Complaint priority breakdown
- Complaint status distribution
- Staff workload
- Staff resolution counts
- Average satisfaction ratings
- Master complaint dataset export

---

## 🔒 Security Considerations

CampusFix includes several useful security foundations:

- Password hashing using bcrypt
- Role-aware application views
- Student complaint filtering by authenticated user ID
- Staff-specific complaint workflow
- Internal staff notes separated from public comments
- Environment-variable configuration support
- Unique generated evidence filenames

### Before production deployment

The current project should be hardened further before handling real institutional data:

1. Replace default/demo credentials.
2. Use a strong, randomly generated secret key.
3. Add strict server-side authorization checks for every mutation.
4. Validate uploaded files by MIME type, extension, size, and content.
5. Store uploads outside the public application path or in controlled object storage.
6. Add CSRF/session hardening appropriate to the deployment architecture.
7. Use a production database such as PostgreSQL for multi-user deployments.
8. Add audit logging for administrative actions.
9. Add automated tests for authentication, authorization, complaint transitions, and data access.
10. Avoid exposing sensitive student information in reports or logs.
11. Add database migrations instead of relying only on `create_all()` for schema evolution.
12. Use HTTPS and secure deployment secrets.

---

## 🔄 Example User Journeys

### Student Journey

```text
Register / Sign In
       ↓
Submit Complaint
       ↓
Receive Ticket ID
       ↓
Track Status
       ↓
View Timeline / Discussion
       ↓
Issue Resolved
       ↓
Rate Resolution
```

### Staff Journey

```text
Sign In
   ↓
Open Work Queue
   ↓
Review Ticket + Evidence
   ↓
Update Status
   ↓
Add Resolution Note
   ↓
Mark Resolved
```

### Admin Journey

```text
Sign In
   ↓
Review KPIs
   ↓
Inspect Incoming Complaints
   ↓
Assign Staff
   ↓
Monitor Progress
   ↓
Review Analytics
   ↓
Export Reports
```

---

## 🧱 Design Principles

CampusFix is structured around a few practical principles:

- **Role-based experience:** each user type gets a focused workspace.
- **Traceability:** complaint status changes are recorded as history entries.
- **Accountability:** tickets can be assigned to specific staff members.
- **Feedback loop:** students can rate completed work and provide feedback.
- **Operational visibility:** administrators receive aggregated KPIs and charts.
- **Evidence-driven reporting:** complaints can include uploaded images.
- **Separation of concerns:** UI, services, data models, and configuration are separated conceptually.

---

## 🧪 Testing Recommendations

Automated tests are not currently included in the repository. A production-ready test suite should cover at least:

```text
tests/
├── test_auth.py
├── test_users.py
├── test_complaints.py
├── test_permissions.py
├── test_analytics.py
└── test_database.py
```

Important test cases include:

- Student registration with duplicate email
- Correct and incorrect password authentication
- Student access restricted to their own complaints
- Staff ticket access
- Admin assignment workflow
- Valid/invalid status transitions
- Complaint reopening
- Satisfaction rating validation
- Internal comment visibility
- Complaint ID generation
- CSV export
- Analytics calculations

---

## 🚧 Current Limitations

The current repository is best treated as a **prototype / academic project / functional demonstration** rather than a production campus service.

Known areas to address include:

- Dependency file is not currently committed.
- The GitHub tree and import namespaces should be aligned (`services.*` / `components.*` vs root-level modules).
- Demo credentials are included in the current seed/demo workflow.
- Default configuration contains a fallback secret and admin password.
- SQLite is suitable for local development but is not the ideal production database for a multi-user institution.
- Automated tests are not currently present.
- Database migrations are not configured.
- File upload validation and storage hardening should be strengthened.
- Fine-grained authorization should be reviewed before production use.

These limitations do not change the project's core workflow; they identify the work required to move from a demonstration system toward an institution-ready deployment.

---

## 🗺️ Suggested Roadmap

### Phase 1 — Project Hardening

- [ ] Add `requirements.txt`
- [ ] Add `.env.example`
- [ ] Add `.gitignore`
- [ ] Resolve package/import structure
- [ ] Remove hard-coded demo secrets from production configuration
- [ ] Add automated tests

### Phase 2 — Production Readiness

- [ ] PostgreSQL support
- [ ] Database migrations with Alembic
- [ ] Stronger authorization policies
- [ ] Secure file storage
- [ ] Centralized application logging
- [ ] Error monitoring
- [ ] Production deployment configuration

### Phase 3 — Campus Operations

- [ ] Email notifications
- [ ] In-app notifications
- [ ] SLA deadline alerts
- [ ] Department-level dashboards
- [ ] Advanced search and reporting
- [ ] Bulk ticket operations
- [ ] Service-level performance history
- [ ] Mobile-friendly workflow improvements

---

## 🤝 Contributing

Contributions are welcome.

A simple contribution workflow:

```bash
git checkout -b feature/your-feature
# make your changes
git add .
git commit -m "feat: describe your change"
git push origin feature/your-feature
```

Then open a pull request describing:

- What changed
- Why it changed
- How it was tested
- Any known limitations

---

## 📌 Project Status

**Status:** Functional prototype / academic project

The repository contains the main application workflow for authentication, complaint submission, ticket management, role-based dashboards, analytics, feedback, and reporting. The next step toward a production-grade system is primarily engineering hardening: dependency management, package consistency, automated testing, authorization review, secure configuration, database migration, and deployment practices.

---

## 👨‍💻 Author

**Deekshith Gowda**

GitHub: [@DeekshithGowda1](https://github.com/DeekshithGowda1)

Project: [CampusFix](https://github.com/DeekshithGowda1/CampusFix)

---

## 📄 License

No license file is currently present in the repository. Until a license is added, the project's source code should be treated as **all rights reserved** rather than assuming an open-source license.

If you want others to legally reuse, modify, and distribute the project, add an appropriate `LICENSE` file to the repository.

---

<div align="center">

**CampusFix — From campus complaints to accountable resolution.**

</div>
