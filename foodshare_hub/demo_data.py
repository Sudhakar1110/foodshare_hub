# Copyright (c) 2024, FoodShare Hub and contributors
# For license information, please see license.txt

"""Demo data generator for FoodShare Hub application.

Usage:
    bench --site yoursite.local execute foodshare_hub.demo_data.create_demo_data
    bench --site yoursite.local execute foodshare_hub.demo_data.create_demo_data --kwargs '{"verbose": true}'
"""

import random
import re
from datetime import datetime, timedelta

import frappe
from frappe.utils import now_datetime, getdate, add_days, get_datetime
from frappe import _


# ──────────────────────────────────────────────
# Data pools
# ──────────────────────────────────────────────

FOOD_CATEGORIES = [
    {"category_name": "Cooked Meals", "description": "Ready to eat cooked meals and prepared food"},
    {"category_name": "Fresh Produce", "description": "Fresh fruits and vegetables"},
    {"category_name": "Baked Goods", "description": "Bread, pastries, cakes and bakery items"},
    {"category_name": "Dairy Products", "description": "Milk, cheese, yogurt and other dairy items"},
    {"category_name": "Beverages", "description": "Drinks, juices, water and other beverages"},
    {"category_name": "Canned Goods", "description": "Canned and preserved food items"},
    {"category_name": "Dry Grains", "description": "Rice, wheat, lentils and other dry grains"},
    {"category_name": "Frozen Foods", "description": "Frozen vegetables, meats and ready meals"},
    {"category_name": "Snacks", "description": "Packaged snacks, chips, biscuits and confectionery"},
    {"category_name": "Baby Food", "description": "Baby formula, purees and toddler snacks"},
    {"category_name": "Condiments", "description": "Sauces, spices, oil and cooking essentials"},
    {"category_name": "Non-Perishable", "description": "Long shelf life packaged food items"},
]

DONOR_ORGANIZATIONS = [
    {"organization_name": "Local Restaurant Association", "contact_person": "John Smith", "contact_email": "john@localrestaurants.com", "contact_phone": "+1-555-0101", "address": "123 Restaurant Row, Food City, FC 10001"},
    {"organization_name": "Corporate Catering Inc", "contact_person": "Sarah Johnson", "contact_email": "sarah@corporatecatering.com", "contact_phone": "+1-555-0102", "address": "456 Business Park, Metro City, MC 20002"},
    {"organization_name": "Grocery Store Chain", "contact_person": "Mike Brown", "contact_email": "mike@grocerystores.com", "contact_phone": "+1-555-0103", "address": "789 Market Street, Downtown, DT 30003"},
    {"organization_name": "Hotel Grand Kitchen", "contact_person": "Anna Williams", "contact_email": "anna@hotelgrand.com", "contact_phone": "+1-555-0104", "address": "100 Luxury Blvd, Uptown, UP 40004"},
    {"organization_name": "Community Garden Project", "contact_person": "David Lee", "contact_email": "david@communitygarden.org", "contact_phone": "+1-555-0105", "address": "50 Green Thumb Lane, Eco City, EC 50005"},
    {"organization_name": "Tech Campus Cafeteria", "contact_person": "Priya Patel", "contact_email": "priya@techcampus.com", "contact_phone": "+1-555-0106", "address": "200 Innovation Drive, Silicon Valley, SV 60006"},
    {"organization_name": "Farmers Market Collective", "contact_person": "Tom Garcia", "contact_email": "tom@farmerscollective.com", "contact_phone": "+1-555-0107", "address": "30 Harvest Road, Rural Town, RT 70007"},
    {"organization_name": "University Dining Services", "contact_person": "Rachel Kim", "contact_email": "rachel@universitydining.edu", "contact_phone": "+1-555-0108", "address": "1 College Avenue, Campus City, CC 80008"},
    {"organization_name": "Wholesale Food Distributors", "contact_person": "James Wilson", "contact_email": "james@wholesalefoods.com", "contact_phone": "+1-555-0109", "address": "500 Industrial Park, Commerce City, CC 90009"},
    {"organization_name": "Organic Farm Cooperative", "contact_person": "Maria Lopez", "contact_email": "maria@organicfarmcoop.com", "contact_phone": "+1-555-0110", "address": "75 Nature Trail, Green Valley, GV 10010"},
    {"organization_name": "Airline Catering Services", "contact_person": "Kevin Chen", "contact_email": "kevin@airlinecatering.aero", "contact_phone": "+1-555-0111", "address": "88 Airport Road, Flight City, FC 11011"},
]

NGO_PARTNERS = [
    {"ngo_name": "Community Food Bank", "contact_person": "Emily Davis", "phone": "+1-555-0201", "email": "emily@cfoodbank.org", "address": "100 Charity Lane, Help Town, HT 20001"},
    {"ngo_name": "Shelter Support Network", "contact_person": "Robert Wilson", "phone": "+1-555-0202", "email": "robert@shelternetwork.org", "address": "200 Hope Avenue, Care City, CC 30002"},
    {"ngo_name": "Youth Education Foundation", "contact_person": "Lisa Anderson", "phone": "+1-555-0203", "email": "lisa@yef.org", "address": "300 Learning Road, Grow Village, GV 40003"},
    {"ngo_name": "Elderly Care Alliance", "contact_person": "Margaret Thompson", "phone": "+1-555-0204", "email": "margaret@elderlycare.org", "address": "150 Senior Lane, Silver Town, ST 50004"},
    {"ngo_name": "Homeless Outreach Program", "contact_person": "Carlos Rivera", "phone": "+1-555-0205", "email": "carlos@homelessoutreach.org", "address": "75 Hope Street, Downtown, DT 60005"},
    {"ngo_name": "Children's Nutrition Initiative", "contact_person": "Jennifer Park", "phone": "+1-555-0206", "email": "jennifer@kidsnutrition.org", "address": "25 Kids Plaza, Family City, FC 70006"},
    {"ngo_name": "Disaster Relief Fund", "contact_person": "Ahmed Hassan", "phone": "+1-555-0207", "email": "ahmed@disasterrelief.org", "address": "500 Emergency Drive, Safe Haven, SH 80007"},
    {"ngo_name": "Women's Empowerment Network", "contact_person": "Sophia Martinez", "phone": "+1-555-0208", "email": "sophia@womensnetwork.org", "address": "60 Equality Blvd, Justice City, JC 90008"},
    {"ngo_name": "Health & Nutrition Foundation", "contact_person": "Dr. James Brown", "phone": "+1-555-0209", "email": "james@healthnutrition.org", "address": "200 Wellness Way, Healthy Town, HT 10009"},
    {"ngo_name": "Interfaith Food Alliance", "contact_person": "Michael Chang", "phone": "+1-555-0210", "email": "michael@interfaithfood.org", "address": "90 Unity Road, Harmony City, HC 11010"},
    {"ngo_name": "Rural Development Trust", "contact_person": "Nalini Sharma", "phone": "+1-555-0211", "email": "nalini@ruraltrust.org", "address": "40 Village Square, Countryside, CS 12011"},
]

DONOR_NAMES = [
    "Alice Johnson", "Bob Martinez", "Carol White", "Daniel Kim",
    "Eva Chen", "Frank Wilson", "Grace Lee", "Henry Davis",
    "Iris Wang", "Jack Brown", "Karen Miller", "Leo Garcia",
    "Mia Anderson", "Noah Taylor", "Olivia Thomas", "Peter Jackson",
    "Quinn Roberts", "Rosa Hernandez", "Sam Patel", "Tina Nguyen",
    "Uma Desai", "Victor Singh", "Wendy Cooper", "Xander Brooks",
]

RECEIVER_NAMES = [
    "St. Mary's Shelter", "Hope Community Kitchen", "Sunrise Children's Home",
    "Grace Elderly Home", "Downtown Outreach Center", "Riverdale Community Center",
    "Maple Leaf School", "Harmony Family Services", "Bright Future Academy",
    "Caring Hands Foundation", "New Beginnings Shelter", "Unity Food Program",
    "Safe Harbor Mission", "Lighthouse Community", "Compassion Network",
    "Bridge to Hope", "Rising Star Academy", "Peaceful Valley Home",
    "Serenity Care Center", "Golden Age Senior Home", "Little Stars Daycare",
    "Neighborly Help Center", "Community Table", "Mercy Food Kitchen",
]

VOLUNTEER_NAMES = [
    "Alex Turner", "Bella Sanchez", "Chris Young", "Diana Foster",
    "Edward Chen", "Fiona O'Brien", "George Harris", "Hannah Lee",
    "Ian Campbell", "Julia Roberts", "Kevin Nguyen", "Lily Park",
    "Marcus Allen", "Nina Patel", "Oscar Williams", "Penelope Cruz",
    "Quincy Adams", "Rachel Green", "Steven King", "Tara Singh",
]

FOOD_DESCRIPTIONS = [
    "Assorted vegetable curry with rice",
    "Fresh garden salad with dressing",
    "Bread rolls and pastries assortment",
    "Chicken stew with potatoes",
    "Pasta with tomato sauce",
    "Seasonal fruit basket",
    "Vegetable soup with crackers",
    "Rice and bean casserole",
    "Sandwich platter (mixed)",
    "Fresh milk and yogurt packs",
    "Assorted juice boxes",
    "Baked cookies and muffins",
    "Canned vegetable mix",
    "Lentil soup (ready to serve)",
    "Grilled vegetables with quinoa",
    "Cheese and cracker packs",
    "Oatmeal breakfast packs",
    "Egg salad sandwiches",
    "Fruit smoothie packs",
    "Vegetable stir-fry with noodles",
]

UNIT_OPTIONS = ["Kg", "Liters", "Pieces", "Boxes", "Packages"]

FOOD_DONATION_STATUSES = ["Draft", "Available", "Collected", "Expired"]

FOOD_REQUEST_STATUSES = ["Draft", "Submitted", "Approved", "Fulfilled", "Rejected"]

PICKUP_STATUSES = ["Pending", "In Progress", "Completed", "Cancelled"]

DELIVERY_STATUSES = ["Pending", "In Transit", "Delivered", "Failed"]

AVAILABILITY_OPTIONS = ["Full Time", "Part Time", "Weekends Only"]

PRIORITY_OPTIONS = ["Low", "Medium", "High", "Urgent"]

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────


def log(message, verbose=False):
    """Print a log message."""
    if verbose:
        print(message)


def safe_insert(doctype, data_dict, check_field=None, verbose=False):
    """Insert a document if it doesn't already exist."""
    if check_field:
        check_value = data_dict.get(check_field)
        if check_value and frappe.db.exists(doctype, {check_field: check_value}):
            log(f"  ⏭  {doctype} '{check_value}' already exists", verbose)
            return frappe.get_doc(doctype, check_value)

    try:
        doc = frappe.get_doc({"doctype": doctype, **data_dict})
        doc.insert(ignore_permissions=True, ignore_mandatory=False)
        log(f"  ✅ Created {doctype}: '{doc.name}'", verbose)
        return doc
    except Exception as e:
        log(f"  ❌ Failed to create {doctype} '{data_dict.get(check_field, '')}': {e}", verbose)
        frappe.log_error(
            message=f"Failed to create demo {doctype}: {frappe.get_traceback()}",
            title=f"FoodShare Hub Demo Data - {doctype}",
        )
        return None


def sanitize_email_localpart(name):
    """Convert a display name into a safe email local-part.

    Removes apostrophes, special chars, and consolidates dots/spaces.
    Example: "St. Mary's Shelter" -> "st.mary.shelter"
    """
    # Lowercase first
    local = name.lower()
    # Replace apostrophes and ampersands with nothing
    local = local.replace("'", "").replace("&", "and")
    # Replace any non-alphanumeric char (except dot) with a space
    local = re.sub(r"[^a-z0-9. ]", " ", local)
    # Replace spaces with dots
    local = local.replace(" ", ".")
    # Collapse consecutive dots into one
    local = re.sub(r"\.+", ".", local)
    # Strip leading/trailing dots
    local = local.strip(".")
    return local


def random_datetime(start_date=None, max_days_ago=30, max_days_ahead=7):
    """Return a random datetime string within range."""
    if start_date is None:
        start_date = datetime.now()
    delta_days = random.randint(-max_days_ago, max_days_ahead)
    delta_hours = random.randint(0, 23)
    delta_minutes = random.randint(0, 59)
    result = start_date + timedelta(days=delta_days, hours=delta_hours, minutes=delta_minutes)
    return result.strftime("%Y-%m-%d %H:%M:%S")


# ──────────────────────────────────────────────
# Master data creators
# ──────────────────────────────────────────────


def create_food_categories(verbose=False):
    """Create food categories."""
    created = 0
    for cat in FOOD_CATEGORIES:
        doc = safe_insert("Food Category", cat, check_field="category_name", verbose=verbose)
        if doc:
            created += 1
    log(f"\n📦 Food Categories: {created} created / {len(FOOD_CATEGORIES)} total", verbose)
    return created


def create_donor_organizations(verbose=False):
    """Create donor organizations."""
    created = 0
    for org in DONOR_ORGANIZATIONS:
        doc = safe_insert("Donor Organization", org, check_field="organization_name", verbose=verbose)
        if doc:
            created += 1
    log(f"\n📦 Donor Organizations: {created} created / {len(DONOR_ORGANIZATIONS)} total", verbose)
    return created


def create_ngo_partners(verbose=False):
    """Create NGO partners."""
    created = 0
    for ngo in NGO_PARTNERS:
        doc = safe_insert("NGO Partner", ngo, check_field="ngo_name", verbose=verbose)
        if doc:
            created += 1
    log(f"\n📦 NGO Partners: {created} created / {len(NGO_PARTNERS)} total", verbose)
    return created


def create_donors(verbose=False):
    """Create donor records linked to donor organizations."""
    org_names = [org["organization_name"] for org in DONOR_ORGANIZATIONS]
    created = 0

    for name in DONOR_NAMES:
        if frappe.db.exists("Donor", {"donor_name": name}):
            log(f"  ⏭  Donor '{name}' already exists", verbose)
            continue

        donor_data = {
            "donor_name": name,
            "email": f"{sanitize_email_localpart(name)}@email.com",
            "phone": f"+1-555-{random.randint(1000, 9999)}",
            "organization": random.choice(org_names),
            "address": f"{random.randint(100, 9999)} {random.choice(['Oak St', 'Elm Ave', 'Maple Dr', 'Pine Ln', 'Cedar Ct'])}, {random.choice(['Food City', 'Metro City', 'Green Valley', 'Downtown', 'Uptown'])}, {random.choice(['FC', 'MC', 'GV', 'DT', 'UP'])}{random.randint(10000, 99999)}",
            "status": "Active" if random.random() > 0.15 else "Inactive",
        }

        doc = safe_insert("Donor", donor_data, check_field="donor_name", verbose=verbose)
        if doc:
            created += 1

    log(f"\n📦 Donors: {created} created / {len(DONOR_NAMES)} total", verbose)
    return created


def create_receivers(verbose=False):
    """Create receiver records."""
    created = 0

    for name in RECEIVER_NAMES:
        if frappe.db.exists("Receiver", {"receiver_name": name}):
            log(f"  ⏭  Receiver '{name}' already exists", verbose)
            continue

        receiver_data = {
            "receiver_name": name,
            "email": f"{sanitize_email_localpart(name)}@receivermail.org",
            "phone": f"+1-555-{random.randint(1000, 9999)}",
            "address": f"{random.randint(100, 9999)} {random.choice(['Support St', 'Care Ave', 'Help Blvd', 'Hope Dr', 'Aid Ln'])}, {random.choice(['Care City', 'Help Town', 'Safe Haven', 'Harmony City', 'Justice City'])}, {random.choice(['CC', 'HT', 'SH', 'HC', 'JC'])}{random.randint(10000, 99999)}",
            "organization": random.choice(
                ["Community Services", "Social Welfare Dept", "Faith-based Network",
                 "Local Government", "Charity Foundation", "Food Security Alliance",
                 "Neighborhood Association", "Youth Services", "Senior Services"]
            ),
            "status": "Active" if random.random() > 0.1 else "Inactive",
        }

        doc = safe_insert("Receiver", receiver_data, check_field="receiver_name", verbose=verbose)
        if doc:
            created += 1

    log(f"\n📦 Receivers: {created} created / {len(RECEIVER_NAMES)} total", verbose)
    return created


def create_volunteers(verbose=False):
    """Create volunteer records."""
    created = 0

    for name in VOLUNTEER_NAMES:
        if frappe.db.exists("Volunteer", {"volunteer_name": name}):
            log(f"  ⏭  Volunteer '{name}' already exists", verbose)
            continue

        volunteer_data = {
            "volunteer_name": name,
            "email": f"{sanitize_email_localpart(name)}@volunteers.org",
            "phone": f"+1-555-{random.randint(1000, 9999)}",
            "address": f"{random.randint(100, 9999)} {random.choice(['Volunteer Ave', 'Service St', 'Helpful Ln', 'Giving Dr', 'Community Ct'])}, {random.choice(['Care City', 'Help Town', 'Food City', 'Green Valley', 'Harmony City'])}, {random.choice(['CC', 'HT', 'FC', 'GV', 'HC'])}{random.randint(10000, 99999)}",
            "availability": random.choice(AVAILABILITY_OPTIONS),
            "status": "Active" if random.random() > 0.15 else "Inactive",
        }

        doc = safe_insert("Volunteer", volunteer_data, check_field="volunteer_name", verbose=verbose)
        if doc:
            created += 1

    log(f"\n📦 Volunteers: {created} created / {len(VOLUNTEER_NAMES)} total", verbose)
    return created


# ──────────────────────────────────────────────
# Transaction data creators
# ──────────────────────────────────────────────


def get_all(doctype):
    """Get all record names for a DocType."""
    return [d.name for d in frappe.get_all(doctype)]


def create_food_donations(count=55, verbose=False):
    """Create food donation transactions."""
    donors = get_all("Donor")
    categories = get_all("Food Category")

    if not donors or not categories:
        log("  ⚠️  No donors or food categories found. Skipping Food Donations.", verbose)
        return 0

    created = 0
    existing_count = frappe.db.count("Food Donation")

    target = count
    needed = max(0, target - existing_count)

    if needed == 0:
        log(f"\n📦 Food Donations: already have {existing_count}, skipping", verbose)
        return 0

    for i in range(needed):
        donor = random.choice(donors)
        category = random.choice(categories)

        # Generate pickup datetime in the past (for most) or near future
        days_ago = random.randint(1, 45)
        pickup_dt = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 12))

        # Expiry is after pickup (1 hour to 7 days)
        expiry_dt = pickup_dt + timedelta(
            hours=random.randint(2, 48),
            minutes=random.choice([0, 15, 30, 45]),
        )

        quantity = round(random.uniform(1, 100), 1)

        # Determine status distribution:
        # ~20% Draft, ~40% Available, ~25% Collected, ~15% Expired
        status_roll = random.random()
        if status_roll < 0.20:
            desired_status = "Draft"
        elif status_roll < 0.60:
            desired_status = "Available"
        elif status_roll < 0.85:
            desired_status = "Collected"
        else:
            desired_status = "Expired"

        donation_data = {
            "donor": donor,
            "food_category": category,
            "food_description": random.choice(FOOD_DESCRIPTIONS),
            "quantity": quantity,
            "unit": random.choice(UNIT_OPTIONS),
            "pickup_datetime": pickup_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "expiry_datetime": expiry_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "pickup_address": f"{random.randint(100, 9999)} {random.choice(['Donor St', 'Give Ave', 'Share Blvd', 'Care Dr'])}, {random.choice(['Food City', 'Metro City', 'Green Valley'])}, {random.choice(['FC', 'MC', 'GV'])}{random.randint(10000, 99999)}",
            # Insert with Draft status to bypass workflow validation
            "status": "Draft",
        }

        try:
            doc = frappe.get_doc({"doctype": "Food Donation", **donation_data})
            doc.insert(ignore_permissions=True, ignore_mandatory=False)
            # Now set the desired status via db_set to bypass workflow validation
            if desired_status != "Draft":
                frappe.db.set_value("Food Donation", doc.name, "status", desired_status)
            created += 1
            if verbose and created % 10 == 0:
                log(f"  ✅ Created Food Donation {created}/{needed}", verbose)
        except Exception as e:
            log(f"  ❌ Failed to create Food Donation: {e}", verbose)
            frappe.log_error(
                message=f"Failed to create demo Food Donation: {frappe.get_traceback()}",
                title="FoodShare Hub Demo Data - Food Donation",
            )

    log(f"\n📦 Food Donations: {created} new / {frappe.db.count('Food Donation')} total", verbose)
    return created


def create_food_requests(count=45, verbose=False):
    """Create food request transactions."""
    receivers = get_all("Receiver")
    categories = get_all("Food Category")

    if not receivers or not categories:
        log("  ⚠️  No receivers or food categories found. Skipping Food Requests.", verbose)
        return 0

    created = 0
    existing_count = frappe.db.count("Food Request")
    needed = max(0, count - existing_count)

    if needed == 0:
        log(f"\n📦 Food Requests: already have {existing_count}, skipping", verbose)
        return 0

    for i in range(needed):
        receiver = random.choice(receivers)
        category = random.choice(categories)

        days_ago = random.randint(1, 30)
        request_date = getdate(add_days(None, -days_ago))

        # Delivery date: some have future dates, some past
        delivery_offset = random.randint(-5, 14)
        delivery_date = add_days(request_date, delivery_offset)
        if delivery_date < request_date:
            delivery_date = request_date

        quantity = round(random.uniform(5, 200), 1)

        # Status distribution
        status_roll = random.random()
        if status_roll < 0.20:
            desired_status = "Draft"
        elif status_roll < 0.40:
            desired_status = "Submitted"
        elif status_roll < 0.65:
            desired_status = "Approved"
        elif status_roll < 0.85:
            desired_status = "Fulfilled"
        else:
            desired_status = "Rejected"

        request_data = {
            "receiver": receiver,
            "food_category": category,
            "required_quantity": quantity,
            "unit": random.choice(UNIT_OPTIONS),
            "request_date": str(request_date),
            "delivery_date": str(delivery_date) if random.random() > 0.3 else "",
            "delivery_address": f"{random.randint(100, 9999)} {random.choice(['Receiver Rd', 'Aid Ave', 'Support St', 'Care Ln'])}, {random.choice(['Care City', 'Help Town', 'Safe Haven', 'Harmony City'])}, {random.choice(['CC', 'HT', 'SH', 'HC'])}{random.randint(10000, 99999)}",
            "priority": random.choice(PRIORITY_OPTIONS),
            # Insert with Draft status to bypass workflow validation
            "status": "Draft",
        }

        try:
            doc = frappe.get_doc({"doctype": "Food Request", **request_data})
            doc.insert(ignore_permissions=True, ignore_mandatory=False)
            # Now set the desired status via db_set to bypass workflow validation
            if desired_status != "Draft":
                frappe.db.set_value("Food Request", doc.name, "status", desired_status)
            created += 1
            if verbose and created % 10 == 0:
                log(f"  ✅ Created Food Request {created}/{needed}", verbose)
        except Exception as e:
            log(f"  ❌ Failed to create Food Request: {e}", verbose)
            frappe.log_error(
                message=f"Failed to create demo Food Request: {frappe.get_traceback()}",
                title="FoodShare Hub Demo Data - Food Request",
            )

    log(f"\n📦 Food Requests: {created} new / {frappe.db.count('Food Request')} total", verbose)
    return created


def create_pickup_assignments(count=35, verbose=False):
    """Create pickup assignment transactions.

    Constraints:
    - Food Donation must have status 'Available'
    - Volunteer must have status 'Active'
    - If pickup_status is 'Completed', donation is auto-set to 'Collected'
    """
    # Get donations that are currently "Available" (or could be set to Available)
    available_donations = frappe.get_all(
        "Food Donation",
        filters={"status": "Available"},
        pluck="name",
    )

    # Also get some "Draft" donations we can use
    draft_donations = frappe.get_all(
        "Food Donation",
        filters={"status": "Draft"},
        pluck="name",
    )

    volunteers = frappe.get_all(
        "Volunteer",
        filters={"status": "Active"},
        pluck="name",
    )

    if not available_donations or not volunteers:
        log("  ⚠️  Not enough available donations or active volunteers. Skipping Pickup Assignments.", verbose)
        return 0

    created = 0
    existing_count = frappe.db.count("Pickup Assignment")
    needed = max(0, count - existing_count)

    if needed == 0:
        log(f"\n📦 Pickup Assignments: already have {existing_count}, skipping", verbose)
        return 0

    # We need donations set to Available. If we don't have enough,
    # change some Draft donations to Available
    all_potential_donations = list(available_donations)

    if len(all_potential_donations) < needed:
        # Supplement with Draft donations; update them to Available
        needed_from_draft = min(needed - len(all_potential_donations), len(draft_donations))
        for dn in draft_donations[:needed_from_draft]:
            frappe.db.set_value("Food Donation", dn, "status", "Available")
            all_potential_donations.append(dn)

    for i in range(min(needed, len(all_potential_donations))):
        donation = all_potential_donations[i]
        volunteer = random.choice(volunteers)

        # Pickup date around the donation's pickup_datetime
        donation_doc = frappe.get_doc("Food Donation", donation)
        pickup_dt = get_datetime(donation_doc.pickup_datetime)

        pickup_date = pickup_dt.strftime("%Y-%m-%d")
        pickup_time = pickup_dt.strftime("%H:%M:%S")

        # Status distribution: ~30% Pending, ~20% In Progress, ~40% Completed, ~10% Cancelled
        status_roll = random.random()
        if status_roll < 0.30:
            pickup_status = "Pending"
        elif status_roll < 0.50:
            pickup_status = "In Progress"
        elif status_roll < 0.90:
            pickup_status = "Completed"
        else:
            pickup_status = "Cancelled"

        assignment_data = {
            "food_donation": donation,
            "volunteer": volunteer,
            "pickup_date": pickup_date,
            "pickup_time": pickup_time,
            "pickup_status": pickup_status,
        }

        try:
            doc = frappe.get_doc({"doctype": "Pickup Assignment", **assignment_data})
            doc.insert(ignore_permissions=True, ignore_mandatory=False)
            created += 1
            if verbose and created % 10 == 0:
                log(f"  ✅ Created Pickup Assignment {created}/{needed}", verbose)
        except Exception as e:
            log(f"  ❌ Failed to create Pickup Assignment: {e}", verbose)
            frappe.log_error(
                message=f"Failed to create demo Pickup Assignment: {frappe.get_traceback()}",
                title="FoodShare Hub Demo Data - Pickup Assignment",
            )

    log(f"\n📦 Pickup Assignments: {created} new / {frappe.db.count('Pickup Assignment')} total", verbose)
    return created


def create_delivery_tracking(count=30, verbose=False):
    """Create delivery tracking transactions.

    Constraints:
    - Pickup Assignment must have pickup_status 'Completed'
    - Receiver must have status 'Active'
    """
    completed_pickups = frappe.get_all(
        "Pickup Assignment",
        filters={"pickup_status": "Completed"},
        pluck="name",
    )

    active_receivers = frappe.get_all(
        "Receiver",
        filters={"status": "Active"},
        pluck="name",
    )

    if not completed_pickups or not active_receivers:
        log("  ⚠️  Not enough completed pickups or active receivers. Skipping Delivery Tracking.", verbose)
        return 0

    created = 0
    existing_count = frappe.db.count("Delivery Tracking")
    needed = max(0, count - existing_count)

    if needed == 0:
        log(f"\n📦 Delivery Tracking: already have {existing_count}, skipping", verbose)
        return 0

    for i in range(min(needed, len(completed_pickups))):
        pickup = completed_pickups[i]
        receiver = random.choice(active_receivers)

        # Get the Food Donation from the pickup assignment
        pickup_doc = frappe.get_doc("Pickup Assignment", pickup)
        food_donation = pickup_doc.food_donation

        # Delivery date is a few days after pickup
        pickup_date = getdate(pickup_doc.pickup_date)
        delivery_offset = random.randint(0, 3)
        delivery_date = add_days(pickup_date, delivery_offset)

        # Get receiver's address or use a default
        receiver_doc = frappe.get_doc("Receiver", receiver)
        delivery_address = receiver_doc.address or f"{random.randint(100, 9999)} Delivery Ave, {random.choice(['Care City', 'Help Town', 'Safe Haven'])}, {random.choice(['CC', 'HT', 'SH'])}{random.randint(10000, 99999)}"

        # Status distribution: ~20% Pending, ~25% In Transit, ~45% Delivered, ~10% Failed
        status_roll = random.random()
        if status_roll < 0.20:
            delivery_status = "Pending"
        elif status_roll < 0.45:
            delivery_status = "In Transit"
        elif status_roll < 0.90:
            delivery_status = "Delivered"
        else:
            delivery_status = "Failed"

        delivery_data = {
            "pickup_assignment": pickup,
            "food_donation": food_donation,
            "receiver": receiver,
            "delivery_date": str(delivery_date),
            "delivery_time": f"{random.randint(8, 18):02d}:{random.choice(['00', '15', '30', '45'])}:00",
            "delivery_status": delivery_status,
            "delivery_address": delivery_address,
            "receiver_contact": receiver_doc.phone or f"+1-555-{random.randint(1000, 9999)}",
        }

        try:
            doc = frappe.get_doc({"doctype": "Delivery Tracking", **delivery_data})
            doc.insert(ignore_permissions=True, ignore_mandatory=False)
            created += 1
            if verbose and created % 10 == 0:
                log(f"  ✅ Created Delivery Tracking {created}/{needed}", verbose)
        except Exception as e:
            log(f"  ❌ Failed to create Delivery Tracking: {e}", verbose)
            frappe.log_error(
                message=f"Failed to create demo Delivery Tracking: {frappe.get_traceback()}",
                title="FoodShare Hub Demo Data - Delivery Tracking",
            )

    log(f"\n📦 Delivery Tracking: {created} new / {frappe.db.count('Delivery Tracking')} total", verbose)
    return created


# ──────────────────────────────────────────────
# Main entry point
# ──────────────────────────────────────────────


def create_demo_data(verbose=True):
    """Create comprehensive demo data for FoodShare Hub.

    Creates all master data and transaction records with realistic,
    interconnected data. Safe to run multiple times — skips existing records.

    Args:
        verbose (bool): If True, prints progress messages. Defaults to True.

    Usage:
        bench --site yoursite.local execute foodshare_hub.demo_data.create_demo_data
        bench --site yoursite.local execute foodshare_hub.demo_data.create_demo_data --kwargs '{"verbose": false}'
    """
    print("\n" + "=" * 60)
    print("  🍽️  FoodShare Hub — Demo Data Generator")
    print("=" * 60)

    # Step 1: Master data (no dependencies)
    print("\n" + "─" * 40)
    print("  STEP 1: Creating Master Data")
    print("─" * 40)

    try:
        create_food_categories(verbose=verbose)
    except Exception as e:
        frappe.log_error(f"Food Categories failed: {e}", "FoodShare Hub Demo Data")
        print(f"  ⚠️  Food Categories error: {e}")

    frappe.db.commit()

    try:
        create_donor_organizations(verbose=verbose)
    except Exception as e:
        frappe.log_error(f"Donor Organizations failed: {e}", "FoodShare Hub Demo Data")
        print(f"  ⚠️  Donor Organizations error: {e}")

    frappe.db.commit()

    try:
        create_ngo_partners(verbose=verbose)
    except Exception as e:
        frappe.log_error(f"NGO Partners failed: {e}", "FoodShare Hub Demo Data")
        print(f"  ⚠️  NGO Partners error: {e}")

    frappe.db.commit()

    try:
        create_donors(verbose=verbose)
    except Exception as e:
        frappe.log_error(f"Donors failed: {e}", "FoodShare Hub Demo Data")
        print(f"  ⚠️  Donors error: {e}")

    frappe.db.commit()

    try:
        create_receivers(verbose=verbose)
    except Exception as e:
        frappe.log_error(f"Receivers failed: {e}", "FoodShare Hub Demo Data")
        print(f"  ⚠️  Receivers error: {e}")

    frappe.db.commit()

    try:
        create_volunteers(verbose=verbose)
    except Exception as e:
        frappe.log_error(f"Volunteers failed: {e}", "FoodShare Hub Demo Data")
        print(f"  ⚠️  Volunteers error: {e}")

    frappe.db.commit()

    # Step 2: Transaction data (depends on master data)
    print("\n" + "─" * 40)
    print("  STEP 2: Creating Transaction Data")
    print("─" * 40)

    try:
        create_food_donations(count=55, verbose=verbose)
    except Exception as e:
        frappe.log_error(f"Food Donations failed: {e}", "FoodShare Hub Demo Data")
        print(f"  ⚠️  Food Donations error: {e}")

    frappe.db.commit()

    try:
        create_food_requests(count=45, verbose=verbose)
    except Exception as e:
        frappe.log_error(f"Food Requests failed: {e}", "FoodShare Hub Demo Data")
        print(f"  ⚠️  Food Requests error: {e}")

    frappe.db.commit()

    try:
        create_pickup_assignments(count=35, verbose=verbose)
    except Exception as e:
        frappe.log_error(f"Pickup Assignments failed: {e}", "FoodShare Hub Demo Data")
        print(f"  ⚠️  Pickup Assignments error: {e}")

    frappe.db.commit()

    try:
        create_delivery_tracking(count=30, verbose=verbose)
    except Exception as e:
        frappe.log_error(f"Delivery Tracking failed: {e}", "FoodShare Hub Demo Data")
        print(f"  ⚠️  Delivery Tracking error: {e}")

    frappe.db.commit()

    # Step 3: Summary
    print("\n" + "─" * 40)
    print("  DEMO DATA GENERATION COMPLETE")
    print("─" * 40)
    print(f"\n  📊 Record Counts:")
    print(f"     Food Categories:     {frappe.db.count('Food Category'):>4}")
    print(f"     Donor Organizations: {frappe.db.count('Donor Organization'):>4}")
    print(f"     NGO Partners:        {frappe.db.count('NGO Partner'):>4}")
    print(f"     Donors:              {frappe.db.count('Donor'):>4}")
    print(f"     Receivers:           {frappe.db.count('Receiver'):>4}")
    print(f"     Volunteers:          {frappe.db.count('Volunteer'):>4}")
    print(f"     Food Donations:      {frappe.db.count('Food Donation'):>4}")
    print(f"     Food Requests:       {frappe.db.count('Food Request'):>4}")
    print(f"     Pickup Assignments:  {frappe.db.count('Pickup Assignment'):>4}")
    print(f"     Delivery Tracking:   {frappe.db.count('Delivery Tracking'):>4}")

    print("\n  ✅ Demo data created successfully!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    create_demo_data()
