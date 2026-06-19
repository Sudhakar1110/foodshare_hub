# FoodShare Hub — Standard Operating Procedure (SOP)

**Application:** FoodShare Hub v1.0.0  
**Platform:** Frappe Framework v15 / ERPNext v15  
**Document Version:** 1.0  
**Last Updated:** June 2026

---

## Table of Contents

1. [Overview](#1-overview)
2. [System Architecture](#2-system-architecture)
3. [Installation & Setup](#3-installation--setup)
4. [Role & User Management](#4-role--user-management)
5. [Master Data Management](#5-master-data-management)
6. [Transaction Processing](#6-transaction-processing)
7. [Workflow Management](#7-workflow-management)
8. [Pickup & Delivery Operations](#8-pickup--delivery-operations)
9. [Reports & Analytics](#9-reports--analytics)
10. [Website & Public Interface](#10-website--public-interface)
11. [API Reference](#11-api-reference)
12. [Demo Data Management](#12-demo-data-management)
13. [Troubleshooting](#13-troubleshooting)
14. [Maintenance & Housekeeping](#14-maintenance--housekeeping)
15. [Appendix](#15-appendix)

---

## 1. Overview

### 1.1 Purpose

FoodShare Hub is a food redistribution platform built on Frappe v15 and ERPNext v15. It connects **Donors** (restaurants, caterers, grocery stores, individuals) with **Receivers** (shelters, NGOs, community kitchens, families in need) through a structured process of donation logging, volunteer-coordinated pickup, and delivery tracking.

### 1.2 Key Objectives

- Reduce food waste by redirecting surplus food to those in need
- Provide end-to-end traceability from donation to delivery
- Enable role-based access for donors, receivers, volunteers, and administrators
- Generate actionable reports on donation volume, fulfillment rates, and impact metrics

### 1.3 Business Flow

```
Donor logs donation → Donation marked "Available" → 
Volunteer assigned for pickup → Pickup completed → 
Delivery to Receiver → Delivery confirmed
```

### 1.4 Core Modules

| Module | Purpose |
|---|---|
| **Masters** | Food Categories, Donors, Donor Organizations, Receivers, NGO Partners, Volunteers |
| **Transactions** | Food Donations, Food Requests, Pickup Assignments, Delivery Tracking |
| **Reports** | Food Donation Report, Food Request Report |
| **Public Website** | Home, Donate Food, Request Food, Available Donations, Contact Us |

---

## 2. System Architecture

### 2.1 Technology Stack

| Component | Technology |
|---|---|
| Framework | Frappe v15 (Python 3.10+) |
| ERP | ERPNext v15 (optional) |
| Database | MariaDB 10.6+ |
| Frontend | Frappe Desk UI + Public Website |
| Task Queue | Redis + RQ Scheduler |
| Web Server | Nginx + Gunicorn |
| Assets | Node.js 16+ |

### 2.2 Application Structure

```
foodshare_hub/
├── api/              # REST API endpoints
├── config/           # Desktop configuration
├── fixtures/         # Importable fixtures (roles, workflows, workspace)
├── masters/          # Master doctype definitions
├── public/           # Static assets (CSS, JS)
├── reports/          # Script reports
│   ├── doctype/      # Report doctype definitions
│   └── report/       # Report execution modules
├── templates/        # Web page templates
├── transactions/     # Transaction doctype definitions
├── www/              # Public web pages
└── demo_data.py      # Demo data generator
```

### 2.3 Autonaming Conventions

| DocType | Pattern | Example |
|---|---|---|
| Food Category | By fieldname: `category_name` | "Fresh Produce" |
| Donor | By fieldname: `donor_name` | "Alice Johnson" |
| Donor Organization | By fieldname: `organization_name` | "Local Restaurant Association" |
| Receiver | By fieldname: `receiver_name` | "Hope Community Kitchen" |
| NGO Partner | By fieldname: `ngo_name` | "Community Food Bank" |
| Volunteer | By fieldname: `volunteer_name` | "Alex Turner" |
| Food Donation | `FD-.YYYY.-.#####` | "FD-2026-00001" |
| Food Request | `FR-.YYYY.-.#####` | "FR-2026-00001" |
| Pickup Assignment | `PA-.YYYY.-.#####` | "PA-2026-00001" |
| Delivery Tracking | `DT-.YYYY.-.#####` | "DT-2026-00001" |

---

## 3. Installation & Setup

### 3.1 Prerequisites

```bash
# Frappe Bench
bench --version  # Must be 5.22+

# Python
python3 --version  # Must be 3.10+

# Node.js
node --version  # Must be 16+

# MariaDB
mysql --version  # Must be 10.6+

# Redis
redis-cli ping  # Must respond PONG
```

### 3.2 Installation

```bash
# 1. Get the app from repository
bench get-app foodshare_hub https://github.com/Sudhakar1110/foodshare_hub.git

# 2. Install on your site
bench --site yoursite.local install-app foodshare_hub

# 3. Run migration (imports fixtures: roles, workflows, workspace)
bench --site yoursite.local migrate

# 4. Build frontend assets
bench build

# 5. Clear cache and restart
bench --site yoursite.local clear-cache
bench restart
```

### 3.3 Post-Installation Verification

```bash
# Verify all fixtures are loaded
bench --site yoursite.local console
```

```python
# Inside console:
import frappe

# Check roles
roles = frappe.get_all("Role", filters={"is_custom": 1}, pluck="name")
print("Custom roles:", roles)
# Expected: ['FoodShare Administrator', 'Donor User', 'Receiver User', 'Volunteer User']

# Check workspace
workspace = frappe.get_doc("Workspace", "FoodShare Hub")
print("Workspace links:", len(workspace.links))
# Expected: 15 (3 Card Breaks + 12 Links)

# Check workflows
workflows = frappe.get_all("Workflow", pluck="workflow_name")
print("Workflows:", workflows)
# Expected: ['Food Donation Workflow', 'Food Request Workflow']
```

---

## 4. Role & User Management

### 4.1 Available Roles

| Role | Desk Access | Permissions | Home Page |
|---|---|---|---|
| **FoodShare Administrator** | Yes | Full CRUD on all DocTypes | Food Donation list |
| **Donor User** | Yes | Create/Read/Write Food Donations (no delete) | New Food Donation form |
| **Receiver User** | Yes | Create/Read/Write Food Requests (no delete) | New Food Request form |
| **Volunteer User** | Yes | Create/Read/Write Pickup Assignments & Delivery Tracking (no delete) | New Pickup Assignment form |

### 4.2 Creating Users

**Via Frappe Desk:**
1. Go to **Users** → **User**
2. Create a new user with email and full name
3. Assign one or more roles: `FoodShare Administrator`, `Donor User`, `Receiver User`, `Volunteer User`
4. Set a password or send invitation email

**Via Bench Console:**
```python
user = frappe.get_doc({
    "doctype": "User",
    "email": "donor@example.com",
    "first_name": "John",
    "last_name": "Donor",
    "roles": [{"role": "Donor User"}],
    "send_welcome_email": 0
})
user.insert(ignore_permissions=True)
user.new_password = "temporary-password-123"
frappe.db.commit()
```

### 4.3 Permission Matrix

| DocType | FoodShare Admin | Donor User | Receiver User | Volunteer User |
|---|---|---|---|---|
| Food Category | CRUD | — | — | — |
| Donor | CRUD | Read | — | — |
| Donor Organization | CRUD | — | — | — |
| Receiver | CRUD | — | Read | — |
| NGO Partner | CRUD | — | — | — |
| Volunteer | CRUD | — | — | Read |
| Food Donation | CRUD | CRU | — | — |
| Food Request | CRUD | — | CRU | — |
| Pickup Assignment | CRUD | — | — | CRU |
| Delivery Tracking | CRUD | — | — | CRU |
| Reports | Read | Read | Read | Read |

*C=Create, R=Read, U=Update, D=Delete*

---

## 5. Master Data Management

### 5.1 Food Category

**Purpose:** Classifies types of food for reporting and filtering.

**Fields:**

| Field | Type | Required | Unique | Notes |
|---|---|---|---|---|
| Category Name | Data | ✅ | ✅ | Used as document name |
| Description | Small Text | — | — | Free-text description |
| Status | Select | — | — | Active / Inactive (default: Active) |

**SOP:**
1. Navigate to **FoodShare Hub → Masters → Food Category**
2. Click **+ Add Food Category**
3. Enter a descriptive category name (e.g., "Cooked Meals", "Fresh Produce")
4. Add a brief description
5. Set Status to "Active"
6. Save

**Validation:** Category Name cannot be empty or duplicate.

### 5.2 Donor Organization

**Purpose:** Groups individual donors under organizations (e.g., restaurants, caterers).

**Fields:**

| Field | Type | Required | Unique | Notes |
|---|---|---|---|---|
| Organization Name | Data | ✅ | ✅ | Used as document name |
| Contact Person | Data | — | — | Primary contact name |
| Contact Email | Data | — | — | Must be valid email format |
| Contact Phone | Data | — | — | — |
| Address | Small Text | — | — | — |
| Status | Select | — | — | Active / Inactive (default: Active) |

**SOP:**
1. Navigate to **FoodShare Hub → Masters → Donor Organization**
2. Click **+ Add Donor Organization**
3. Enter organization details
4. Set Status to "Active"
5. Save

### 5.3 Donor

**Purpose:** Represents an individual or entity that donates food.

**Fields:**

| Field | Type | Required | Unique | Notes |
|---|---|---|---|---|
| Donor Name | Data | ✅ | Yes | Used as document name |
| Email | Data | — | — | Validated for email format |
| Phone | Data | — | — | Minimum 10 characters |
| Donor Organization | Link | — | — | Links to Donor Organization |
| Address | Small Text | — | — | — |
| Status | Select | — | — | Active / Inactive (default: Active) |

**SOP:**
1. Navigate to **FoodShare Hub → Masters → Donor**
2. Click **+ Add Donor**
3. Enter donor name (unique)
4. Optionally link to a Donor Organization
5. Provide contact details
6. Set Status to "Active"
7. Save

### 5.4 Receiver

**Purpose:** Represents an organization or individual that receives food donations.

**Fields:**

| Field | Type | Required | Unique | Notes |
|---|---|---|---|---|
| Receiver Name | Data | ✅ | Yes | Used as document name |
| Email | Data | — | — | Validated for email format |
| Phone | Data | — | — | Minimum 10 characters |
| Address | Small Text | — | — | — |
| Organization | Data | — | — | Free-text organization name |
| Status | Select | — | — | Active / Inactive (default: Active) |

**SOP:**
1. Navigate to **FoodShare Hub → Masters → Receiver**
2. Click **+ Add Receiver**
3. Enter receiver details
4. Set Status to "Active"
5. Save

### 5.5 NGO Partner

**Purpose:** Tracks NGO partner organizations.

**Fields:**

| Field | Type | Required | Unique | Notes |
|---|---|---|---|---|
| NGO Name | Data | ✅ | ✅ | Used as document name |
| Contact Person | Data | — | — | — |
| Phone | Data | — | — | — |
| Email | Data | — | — | Validated for email format |
| Address | Small Text | — | — | — |
| Status | Select | — | — | Active / Inactive (default: Active) |
| Registration Number | Data | — | — | Hidden field |

**SOP:**
1. Navigate to **FoodShare Hub → Masters → NGO Partner**
2. Click **+ Add NGO Partner**
3. Enter NGO details
4. Set Status to "Active"
5. Save

### 5.6 Volunteer

**Purpose:** Represents individuals who pick up and deliver food donations.

**Fields:**

| Field | Type | Required | Unique | Notes |
|---|---|---|---|---|
| Volunteer Name | Data | ✅ | Yes | Used as document name |
| Email | Data | — | — | Validated for email format |
| Phone | Data | — | — | Minimum 10 characters |
| Address | Small Text | — | — | — |
| Availability | Select | — | — | Full Time / Part Time / Weekends Only |
| Status | Select | — | — | Active / Inactive (default: Active) |

**SOP:**
1. Navigate to **FoodShare Hub → Masters → Volunteer**
2. Click **+ Add Volunteer**
3. Enter volunteer details
4. Select availability
5. Set Status to "Active"
6. Save

---

## 6. Transaction Processing

### 6.1 Food Donation

**Purpose:** Records a food donation offer from a donor.

**Fields:**

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| Donor | Link (Donor) | ✅ | — | Must exist in system |
| Food Category | Link (Food Category) | ✅ | — | Must exist in system |
| Food Description | Small Text | — | — | Describe the food items |
| Quantity | Float | ✅ | — | Must be > 0 |
| Unit | Select | — | Kg | Kg / Liters / Pieces / Boxes / Packages |
| Pickup Date & Time | Datetime | ✅ | — | When food can be picked up |
| Expiry Date & Time | Datetime | ✅ | — | Must be after Pickup time |
| Pickup Address | Small Text | — | — | Where to pick up from |
| Status | Select | — | Draft | Draft / Available / Collected / Expired |
| Remarks | Text | — | — | Hidden internal notes |

**SOP — Creating a Donation:**

1. Navigate to **FoodShare Hub → Transactions → Food Donation**
2. Click **+ Add Food Donation**
3. Select the **Donor** from the list
4. Select the **Food Category**
5. Describe the food items
6. Enter **Quantity** and select **Unit**
7. Set **Pickup Date & Time** (when the food is ready)
8. Set **Expiry Date & Time** (must be after pickup)
9. Enter **Pickup Address**
10. Save (status defaults to "Draft")
11. To make it available for pickup, use the **"Make Available"** workflow action

**Validation Rules:**
- Quantity must be greater than zero
- Expiry Date & Time must be after Pickup Date & Time
- Donor must exist and be active
- Food Category must exist and be active

### 6.2 Food Request

**Purpose:** Records a food request from a receiver organization.

**Fields:**

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| Receiver | Link (Receiver) | ✅ | — | Must exist in system |
| Food Category | Link (Food Category) | ✅ | — | Must exist in system |
| Required Quantity | Float | ✅ | — | Must be > 0 |
| Unit | Select | — | Kg | Kg / Liters / Pieces / Boxes / Packages |
| Request Date | Date | ✅ | Today | When the request was made |
| Preferred Delivery Date | Date | — | — | Cannot be before Request Date |
| Delivery Address | Small Text | — | — | Where food should be delivered |
| Priority | Select | — | Medium | Low / Medium / High / Urgent |
| Status | Select | — | Draft | Draft / Submitted / Approved / Fulfilled / Rejected |
| Remarks | Text | — | — | Hidden internal notes |

**SOP — Creating a Request:**

1. Navigate to **FoodShare Hub → Transactions → Food Request**
2. Click **+ Add Food Request**
3. Select the **Receiver**
4. Select the **Food Category**
5. Enter **Required Quantity** and select **Unit**
6. Set **Request Date** (defaults to today)
7. Optionally set **Preferred Delivery Date**
8. Set **Priority** level
9. Enter **Delivery Address**
10. Save (status defaults to "Draft")
11. Use the **"Submit"** workflow action to begin the approval process

**Validation Rules:**
- Required Quantity must be greater than zero
- Preferred Delivery Date cannot be before Request Date
- Receiver must exist and be active
- Food Category must exist and be active

---

## 7. Workflow Management

### 7.1 Food Donation Workflow

**States and Transitions:**

```
                        ┌──────────────┐
                        │    Draft     │
                        └──────┬───────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
         Make Available        │      Mark Expired
                 │             │             │
                 ▼             │             ▼
          ┌────────────┐       │      ┌──────────┐
          │ Available  │       │      │ Expired  │
          └─────┬──────┘       │      └──────────┘
                 │             │
       ┌─────────┼─────────┐   │
       │         │         │   │
Mark Collected    │  Mark Expired
       │         │         │   │
       ▼         │         ▼   │
┌──────────┐     │   ┌──────────┐
│ Collected│     │   │ Expired  │
└──────────┘     │   └──────────┘
                 │
```

**Workflow Actions:**

| Current State | Action | Next State | Allowed Role |
|---|---|---|---|
| Draft | Make Available | Available | FoodShare Administrator |
| Draft | Mark Expired | Expired | FoodShare Administrator |
| Available | Mark Collected | Collected | FoodShare Administrator |
| Available | Mark Expired | Expired | FoodShare Administrator |

### 7.2 Food Request Workflow

**States and Transitions:**

```
┌────────┐     Submit     ┌───────────┐
│ Draft  │ ─────────────→ │ Submitted │
└────────┘                └─────┬─────┘
                                │
                    ┌───────────┼───────────┐
                    │           │           │
                Approve         │       Reject
                    │           │           │
                    ▼           │           ▼
             ┌──────────┐      │    ┌──────────┐
             │ Approved │      │    │ Rejected │
             └─────┬────┘      │    └──────────┘
                   │           │
           Mark Fulfilled       │
                   │           │
                   ▼           │
            ┌───────────┐      │
            │ Fulfilled │      │
            └───────────┘      │
```

**Workflow Actions:**

| Current State | Action | Next State | Allowed Role |
|---|---|---|---|
| Draft | Submit | Submitted | FoodShare Administrator |
| Submitted | Approve | Approved | FoodShare Administrator |
| Submitted | Reject | Rejected | FoodShare Administrator |
| Approved | Mark Fulfilled | Fulfilled | FoodShare Administrator |

### 7.3 Performing Workflow Actions

**Via Frappe Desk:**
1. Open the document (Food Donation or Food Request)
2. Look for the workflow action buttons in the toolbar
3. Click the desired action (e.g., "Make Available")
4. The status updates automatically

**Via API:**
```python
# Programmatic workflow transition
doc = frappe.get_doc("Food Donation", "FD-2026-00001")
doc.status = "Available"
doc.save(ignore_permissions=True)
frappe.db.commit()
```

**Note:** For bulk operations via `db_set_value()`, workflow validation is bypassed — use this only for internal/administrative operations.

---

## 8. Pickup & Delivery Operations

### 8.1 Pickup Assignment

**Purpose:** Assigns a volunteer to pick up a food donation from a donor.

**Important Validation Rules:**
- The linked Food Donation must have **status "Available"** — otherwise validation fails
- The linked Volunteer must have **status "Active"** — otherwise validation fails
- When Pickup Status changes to **"Completed"**, the Food Donation status is automatically set to **"Collected"**

**Fields:**

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| Food Donation | Link (Food Donation) | ✅ | — | Must be in "Available" status |
| Volunteer | Link (Volunteer) | ✅ | — | Must be "Active" |
| Pickup Date | Date | ✅ | — | When pickup occurs |
| Pickup Time | Time | — | — | Optional time |
| Pickup Status | Select | — | Pending | Pending / In Progress / Completed / Cancelled |
| Contact Phone | Data | — | — | — |
| Remarks | Small Text | — | — | Hidden notes |

**SOP:**

1. Navigate to **FoodShare Hub → Transactions → Pickup Assignment**
2. Click **+ Add Pickup Assignment**
3. Select a **Food Donation** with status "Available"
4. Select an **Active Volunteer**
5. Set **Pickup Date** and optionally **Pickup Time**
6. Set **Pickup Status** to "Pending"
7. Save
8. As pickup progresses, update status:
   - **"In Progress"** — volunteer has started pickup
   - **"Completed"** — food collected → donation auto-updates to "Collected"
   - **"Cancelled"** — pickup abandoned

### 8.2 Delivery Tracking

**Purpose:** Tracks the delivery of collected food to a receiver.

**Important Validation Rules:**
- The linked Pickup Assignment must have **status "Completed"** — otherwise validation fails
- The linked Receiver must have **status "Active"** — otherwise validation fails
- The linked Food Donation is copied from the Pickup Assignment (ensures traceability)

**Fields:**

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| Pickup Assignment | Link (Pickup Assignment) | ✅ | — | Must be "Completed" |
| Food Donation | Link (Food Donation) | ✅ | — | Auto-populated from pickup |
| Receiver | Link (Receiver) | ✅ | — | Must be "Active" |
| Delivery Date | Date | ✅ | — | When delivery occurs |
| Delivery Time | Time | — | — | Optional time |
| Delivery Status | Select | — | Pending | Pending / In Transit / Delivered / Failed |
| Delivery Address | Small Text | — | — | Receiver's address |
| Receiver Contact | Data | — | — | Contact phone number |
| Remarks | Small Text | — | — | Hidden notes |

**SOP:**

1. Navigate to **FoodShare Hub → Transactions → Delivery Tracking**
2. Click **+ Add Delivery Tracking**
3. Select a **Pickup Assignment** with status "Completed"
4. The **Food Donation** field auto-populates from the pickup
5. Select the **Receiver** (must be Active)
6. Set **Delivery Date** and optionally **Delivery Time**
7. The **Delivery Address** defaults to the Receiver's address
8. Set **Delivery Status** to "Pending"
9. Save
10. Update **Delivery Status** as delivery progresses:
    - **"In Transit"** — food is on the way
    - **"Delivered"** — successfully delivered
    - **"Failed"** — delivery could not be completed

### 8.3 End-to-End Process Flow

```
┌─────────────────────────────────────────────────────────┐
│                   COMPLETE OPERATIONS FLOW               │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Donor creates Food Donation (status: Draft)          │
│  2. Admin marks "Make Available" (status: Available)     │
│  3. Volunteer assigned via Pickup Assignment             │
│     - Donation must be "Available"                       │
│     - Volunteer must be "Active"                         │
│  4. Volunteer completes pickup (status: Completed)        │
│     → Donation auto-updates to "Collected"               │
│  5. Delivery Tracking created                            │
│     - Pickup must be "Completed"                         │
│     - Receiver must be "Active"                          │
│  6. Food delivered (status: Delivered)                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 9. Reports & Analytics

### 9.1 Food Donation Report

**Type:** Script Report  
**Module:** Reports  
**Ref DocType:** Food Donation

**Columns:**

| Fieldname | Label | Type |
|---|---|---|
| donation_id | Donation ID | Link (Food Donation) |
| donor | Donor | Link (Donor) |
| food_category | Food Category | Link (Food Category) |
| food_description | Description | Data |
| quantity | Quantity | Float |
| unit | Unit | Data |
| pickup_datetime | Pickup Date & Time | Datetime |
| expiry_datetime | Expiry Date & Time | Datetime |
| status | Status | Select |

**Filters:**
- Donor
- Food Category
- Status
- From Date (pickup_datetime >=)
- To Date (pickup_datetime <=)

**How to Run:**
1. Navigate to **FoodShare Hub → Reports → Food Donation Report**
2. (Optional) Set filters
3. Click **Show Report**

### 9.2 Food Request Report

**Type:** Script Report  
**Module:** Reports  
**Ref DocType:** Food Request

**Columns:**

| Fieldname | Label | Type |
|---|---|---|
| request_id | Request ID | Link (Food Request) |
| receiver | Receiver | Link (Receiver) |
| food_category | Food Category | Link (Food Category) |
| required_quantity | Required Quantity | Float |
| unit | Unit | Data |
| request_date | Request Date | Date |
| delivery_date | Preferred Delivery Date | Date |
| priority | Priority | Select |
| status | Status | Select |

**Filters:**
- Receiver
- Food Category
- Status
- Priority
- From Date (request_date >=)
- To Date (request_date <=)

**How to Run:**
1. Navigate to **FoodShare Hub → Reports → Food Request Report**
2. (Optional) Set filters
3. Click **Show Report**

### 9.3 Viewing Report Data via Console

```python
# Food Donation Report
from foodshare_hub.reports.report.food_donation_report.food_donation_report import execute
columns, data = execute(frappe._dict({"status": "Available"}))
print(f"Available donations: {len(data)}")

# Food Request Report
from foodshare_hub.reports.report.food_request_report.food_request_report import execute
columns, data = execute(frappe._dict({"status": "Submitted"}))
print(f"Pending requests: {len(data)}")
```

---

## 10. Website & Public Interface

### 10.1 Public Routes

| Route | Page | Description |
|---|---|---|
| `/` | Home | Landing page with stats |
| `/donate-food` | Donate Food | Register a food donation (public) |
| `/request-food` | Request Food | Submit a food request (public) |
| `/available-donations` | Available Donations | Browse available food |
| `/contact-us` | Contact Us | Contact form |

### 10.2 Web View

Food Donations with status "Available" are published as web views at:
- Route: `/food-donation/{name}`
- Shows: donor, description, quantity, pickup info
- Condition: `status == "Available"`

---

## 11. API Reference

### 11.1 Donation APIs

| Endpoint | Method | Description |
|---|---|---|
| `foodshare_hub.api.donation.get_donation` | GET | Get donation by name |
| `foodshare_hub.api.donation.get_donations_by_donor` | GET | List donations by donor |
| `foodshare_hub.api.donation.update_donation_status` | POST | Update donation status |
| `foodshare_hub.api.donation.get_available_donations_count` | GET | Count of available donations |

### 11.2 Request APIs

| Endpoint | Method | Description |
|---|---|---|
| `foodshare_hub.api.request.get_request` | GET | Get request by name |
| `foodshare_hub.api.request.get_requests_by_receiver` | GET | List requests by receiver |
| `foodshare_hub.api.request.update_request_status` | POST | Update request status |
| `foodshare_hub.api.request.get_pending_requests_count` | GET | Count of pending requests |

### 11.3 Utility APIs

| Endpoint | Method | Description |
|---|---|---|
| `foodshare_hub.api.utils.get_available_donations` | GET | List available donations (with optional category filter) |
| `foodshare_hub.api.utils.get_pending_requests` | GET | List pending requests (with optional filters) |
| `foodshare_hub.api.utils.create_donation` | POST | Create a new donation |
| `foodshare_hub.api.utils.create_request` | POST | Create a new request |
| `foodshare_hub.api.utils.get_donation_stats` | GET | Donation statistics |
| `foodshare_hub.api.utils.get_request_stats` | GET | Request statistics |

### 11.4 API Usage Examples

```python
import frappe

# Get donation stats
stats = frappe.call("foodshare_hub.api.utils.get_donation_stats")
print(stats)
# {'total_donations': 55, 'available_donations': 22, ...}

# Get available donations
donations = frappe.call(
    "foodshare_hub.api.utils.get_available_donations",
    food_category="Fresh Produce",
    limit=10
)

# Create a donation (logged-in user required)
result = frappe.call(
    "foodshare_hub.api.utils.create_donation",
    donor="Alice Johnson",
    food_category="Cooked Meals",
    food_description="Vegetable curry with rice",
    quantity=25,
    unit="Kg",
    pickup_datetime="2026-06-20 10:00:00",
    expiry_datetime="2026-06-22 10:00:00",
    pickup_address="123 Main St, Food City"
)
```

### 11.5 Calling APIs from Outside Frappe

```bash
# Get session token first (requires a user with API access)
curl -X POST https://yoursite.local/api/method/login \
  -H "Content-Type: application/json" \
  -d '{"usr": "admin@example.com", "pwd": "password"}'

# Use the session cookie or API key to call endpoints
curl https://yoursite.local/api/method/foodshare_hub.api.utils.get_donation_stats \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET"

curl https://yoursite.local/api/method/foodshare_hub.api.utils.get_available_donations \
  -H "Authorization: token YOUR_API_KEY:YOUR_API_SECRET" \
  -d '{"food_category": "Fresh Produce", "limit": 5}'
```

---

## 12. Demo Data Management

### 12.1 Generating Demo Data

FoodShare Hub includes a comprehensive Python-based demo data generator.

**Run the demo data generator:**

```bash
bench --site yoursite.local execute foodshare_hub.demo_data.create_demo_data
```

**Quiet mode (no output):**

```bash
bench --site yoursite.local execute foodshare_hub.demo_data.create_demo_data --kwargs '{"verbose": false}'
```

### 12.2 What Gets Created

| DocType | Count | Data Source |
|---|---|---|
| Food Categories | 12 | Predefined in script |
| Donor Organizations | 11 | Predefined in script |
| NGO Partners | 11 | Predefined in script |
| Donors | 24 | Generated from name list |
| Receivers | 24 | Generated from name list |
| Volunteers | 20 | Generated from name list |
| Food Donations | 55 | Randomly generated with realistic data |
| Food Requests | 45 | Randomly generated with realistic data |
| Pickup Assignments | 35 | Linked to available donations |
| Delivery Tracking | ~12-30 | Linked to completed pickups |

### 12.3 Safe Re-Running

The generator is **idempotent** — running it multiple times:
- Skips existing master records (checks by unique name field)
- Creates only missing transaction records (up to target count)
- Never duplicates or overwrites existing data

### 12.4 Legacy JSON Fixture

An older `fixtures/demo_data.json` file exists with basic data for Food Categories, Donor Organizations, and NGO Partners. This is loaded automatically during `after_install()`. The Python-based generator (`demo_data.py`) is the recommended approach for comprehensive demo data.

### 12.5 Verifying Demo Data

```bash
bench --site yoursite.local console
```

```python
# Quick count check
for dt in ["Food Category", "Donor", "Donor Organization", "Receiver", 
           "NGO Partner", "Volunteer", "Food Donation", "Food Request",
           "Pickup Assignment", "Delivery Tracking"]:
    print(f"{dt:25s}: {frappe.db.count(dt)}")
```

```python
# Check link integrity
for dt, link, target in [
    ("Donor", "organization", "Donor Organization"),
    ("Food Donation", "donor", "Donor"),
    ("Food Donation", "food_category", "Food Category"),
    ("Food Request", "receiver", "Receiver"),
    ("Food Request", "food_category", "Food Category"),
    ("Pickup Assignment", "food_donation", "Food Donation"),
    ("Pickup Assignment", "volunteer", "Volunteer"),
    ("Delivery Tracking", "pickup_assignment", "Pickup Assignment"),
    ("Delivery Tracking", "food_donation", "Food Donation"),
    ("Delivery Tracking", "receiver", "Receiver"),
]:
    records = frappe.get_all(dt, fields=["name", link], limit=100)
    broken = [r.name for r in records if r.get(link) and not frappe.db.exists(target, r[link])]
    print(f"{dt}.{link}: {'✅' if not broken else '❌ ' + str(len(broken)) + ' broken'}")
```

---

## 13. Troubleshooting

### 13.1 Common Errors & Solutions

#### "Workflow State transition not allowed from Draft to Available"

**Cause:** Active workflow prevents setting status directly on insert via API.

**Solution (for programmatic data creation):**
```python
# Insert with status="Draft" first, then update via db_set_value
doc = frappe.get_doc({"doctype": "Food Donation", ..., "status": "Draft"})
doc.insert(ignore_permissions=True)
frappe.db.set_value("Food Donation", doc.name, "status", "Available")
```

#### "Food Donation 'X' is not available for pickup"

**Cause:** Pickup Assignment requires the linked Food Donation to be in "Available" status.

**Solution:** Change the Food Donation status to "Available" first, then create the Pickup Assignment.

#### "Pickup Assignment 'X' must be completed before delivery"

**Cause:** Delivery Tracking requires the linked Pickup Assignment to be "Completed".

**Solution:** Update the Pickup Assignment status to "Completed" first, then create the Delivery Tracking.

#### "X is not a valid Email Address"

**Cause:** Email format validation failed, often due to special characters in the name.

**Solution:** Use alphanumeric characters and dots only in the email local-part. Avoid apostrophes and special characters.

#### Workspace shows empty in browser but data exists in DB

**Cause:** Stale cache or incorrect content format in the workspace fixture.

**Solution:**
```bash
bench --site yoursite.local clear-cache
bench restart
```

Then hard-refresh browser (Ctrl+Shift+R).

If still empty:
```python
# Check the API response directly
from frappe.desk.desktop import get_desktop_page
result = get_desktop_page('{"name":"FoodShare Hub","title":"FoodShare Hub","public":true}')
print(f"Cards: {len(result['cards']['items'])}")
```

### 13.2 Cache Issues

```bash
# Clear all caches
bench --site yoursite.local clear-cache
frappe.cache().flushall()  # Inside console

# Restart processes
bench restart
```

### 13.3 Debugging

```bash
# Enable developer mode
bench set-config -s developer_mode 1

# Set log level
bench set-log-level DEBUG

# Monitor logs in real-time
bench console
bench frappe --logs

# Check error logs
bench --site yoursite.local console
```

```python
# Inside console - check recent errors
import frappe
errors = frappe.get_all("Error Log", fields=["name", "error", "creation"], 
                        limit=10, order_by="creation desc")
for e in errors:
    print(f"[{e.creation}] {e.name}: {e.error[:200]}")
```

---

## 14. Maintenance & Housekeeping

### 14.1 Regular Tasks

| Frequency | Task | Command |
|---|---|---|
| Daily | Backup database | `bench --site yoursite.local backup` |
| Weekly | Clear old logs | `bench --site yoursite.local clear-log` |
| Monthly | Rebuild search index | `bench --site yoursite.local rebuild-search-index` |
| As needed | Rebuild assets | `bench build` |
| As needed | Clear cache | `bench --site yoursite.local clear-cache && bench restart` |

### 14.2 Exporting Fixtures

When making changes to Fixture data (roles, workflows, workspace) in the UI:

```bash
bench --site yoursite.local export-fixtures --app foodshare_hub
```

This updates the JSON files in `foodshare_hub/fixtures/` with the current database state.

### 14.3 Module-Level Exports

In developer mode, certain document changes auto-export to module files:
- Workspace changes → `foodshare_hub/workspace/`
- Report changes → `foodshare_hub/reports/`

### 14.4 Upgrading

```bash
# Pull latest code
cd ~/f15-su/apps/foodshare_hub
git fetch origin main
git reset --hard origin/main

# Run migration
cd ~/f15-su
bench --site yoursite.local migrate

# Rebuild assets
bench build

# Clear cache and restart
bench --site yoursite.local clear-cache
bench restart
```

---

## 15. Appendix

### 15.1 Fixture Files

| File | Purpose |
|---|---|
| `fixtures/role.json` | Custom roles (FoodShare Administrator, Donor User, etc.) |
| `fixtures/workflow.json` | Workflows for Food Donation and Food Request |
| `fixtures/workspace.json` | FoodShare Hub workspace with 3 cards and 15 links |
| `fixtures/custom_docperm.json` | Custom document permissions |
| `fixtures/property_setter.json` | Property customizations |
| `fixtures/demo_data.json` | Legacy demo data (basic masters) |

### 15.2 Key Hooks Configuration

| Hook | Value | Purpose |
|---|---|---|
| `app_name` | `foodshare_hub` | Python module name |
| `app_title` | `FoodShare Hub` | Display name |
| `fixtures` | Role, Custom DocPerm, Workflow, etc. | Auto-imported on migration |
| `doc_events.*.on_update` | `api.utils.update_modified` | Global hook for all DocTypes |

### 15.3 Requirements Dependencies

| Package | Purpose |
|---|---|
| frappe (v15) | Web framework |
| erpnext (v15, optional) | ERP integration |

### 15.4 File Reference

```
foodshare_hub/
├── demo_data.py                          # Python demo data generator (~380 lines)
├── install.py                            # Post-install hooks
├── hooks.py                              # Application hooks & configuration
├── api/
│   ├── donation.py                       # Donation REST API endpoints
│   ├── request.py                        # Request REST API endpoints
│   └── utils.py                          # Utility API functions
├── fixtures/
│   ├── role.json                         # Custom role definitions
│   ├── workflow.json                     # Workflow definitions
│   ├── workspace.json                    # Workspace layout
│   ├── custom_docperm.json               # Custom DocPerm overrides
│   ├── property_setter.json              # Property setter overrides
│   └── demo_data.json                    # Legacy basic demo data
├── masters/doctype/                      # 6 Master DocTypes
│   ├── food_category/                    # Autoname: field:category_name
│   ├── donor/                            # Autoname: field:donor_name
│   ├── donor_organization/               # Autoname: field:organization_name
│   ├── receiver/                         # Autoname: field:receiver_name
│   ├── ngo_partner/                      # Autoname: field:ngo_name
│   └── volunteer/                        # Autoname: field:volunteer_name
├── transactions/doctype/                 # 4 Transaction DocTypes
│   ├── food_donation/                    # Autoname: FD-.YYYY.-.#####
│   ├── food_request/                     # Autoname: FR-.YYYY.-.#####
│   ├── pickup_assignment/                # Autoname: PA-.YYYY.-.#####
│   └── delivery_tracking/                # Autoname: DT-.YYYY.-.#####
├── reports/
│   ├── doctype/food_donation_report/     # Report DocType definition
│   ├── doctype/food_request_report/      # Report DocType definition  
│   ├── report/food_donation_report/      # Report execution module
│   └── report/food_request_report/       # Report execution module
├── www/                                  # Public web pages
│   ├── home.html / home.py               # Landing page
│   ├── donate-food.html / donate-food.py # Donation form
│   ├── request-food.html / request-food.py # Request form
│   ├── available-donations.html / .py    # Browse donations
│   └── contact-us.html / contact-us.py   # Contact form
└── templates/web.html                    # Base web template
```

### 15.5 Quick Reference Commands

```bash
# ─── Installation ───
bench get-app foodshare_hub https://github.com/Sudhakar1110/foodshare_hub.git
bench --site yoursite.local install-app foodshare_hub
bench --site yoursite.local migrate
bench build
bench --site yoursite.local clear-cache && bench restart

# ─── Demo Data ───
bench --site yoursite.local execute foodshare_hub.demo_data.create_demo_data

# ─── Data Verification ───
bench --site yoursite.local console
# Then run the verification script from Section 12.5

# ─── Cache & Restart ───
bench --site yoursite.local clear-cache
bench restart

# ─── Export Fixtures ───
bench --site yoursite.local export-fixtures --app foodshare_hub

# ─── Upgrade ───
cd ~/apps/foodshare_hub && git fetch origin main && git reset --hard origin/main
cd ~ && bench --site yoursite.local migrate && bench build
bench --site yoursite.local clear-cache && bench restart

# ─── Backup ───
bench --site yoursite.local backup

# ─── Reports (via console) ───
bench --site yoursite.local console
from foodshare_hub.reports.report.food_donation_report.food_donation_report import execute
cols, data = execute(frappe._dict())
print(f"Donation Report: {len(data)} rows")
```

---

*End of Document — FoodShare Hub SOP v1.0*
