# FoodShare Hub

A Frappe v15 / ERPNext v15+ application for managing leftover food donations and distribution to those in need.

## Features

- **Food Donation Management**: Track and manage food donations from various donors
- **Food Request System**: Handle food requests from NGOs, shelters, and community organizations
- **Pickup Assignment**: Assign volunteers to collect donations
- **Delivery Tracking**: Track food deliveries to receivers
- **Role-based Access**: Different roles for Administrators, Donors, Receivers, and Volunteers
- **Workflow Automation**: Automated status transitions for donations and requests
- **Reports**: Generate donation and request reports
- **Website Integration**: Public website for browsing available donations

## Installation

### Prerequisites

- Frappe Framework v15 or higher
- ERPNext v15 or higher (optional)
- Python 3.10+
- Node.js 16+

### Install via Bench

```bash
# Get the app
bench get-app foodshare_hub <repository_url>

# Install on a site
bench --site <sitename> install-app foodshare_hub

# Migrate
bench --site <sitename> migrate

# Build assets
bench build
```

## Modules

### Masters
- Food Category
- Donor
- Donor Organization
- Receiver
- NGO Partner
- Volunteer

### Transactions
- Food Donation
- Food Request
- Pickup Assignment
- Delivery Tracking

### Reports
- Food Donation Report
- Food Request Report

## Roles

- **FoodShare Administrator**: Full access to all modules
- **Donor User**: Can create and manage food donations
- **Receiver User**: Can create and manage food requests
- **Volunteer User**: Can manage pickup assignments and deliveries

## Workflows

### Food Donation Workflow
```
Draft → Available → Collected
                 ↘ Expired
```

### Food Request Workflow
```
Draft → Submitted → Approved → Fulfilled
                   ↘ Rejected
```

## Website Routes

- `/`: Home page
- `/donate-food`: Donate food page
- `/request-food`: Request food page
- `/available-donations`: Browse available donations
- `/contact-us`: Contact information

## API Endpoints

### Donation APIs
- `api/method/foodshare_hub.api.donation.get_donation`
- `api/method/foodshare_hub.api.donation.get_donations_by_donor`
- `api/method/foodshare_hub.api.donation.update_donation_status`

### Request APIs
- `api/method/foodshare_hub.api.request.get_request`
- `api/method/foodshare_hub.api.request.get_requests_by_receiver`
- `api/method/foodshare_hub.api.request.update_request_status`

### Utility APIs
- `api/method/foodshare_hub.api.utils.get_available_donations`
- `api/method/foodshare_hub.api.utils.get_pending_requests`
- `api/method/foodshare_hub.api.utils.get_donation_stats`
- `api/method/foodshare_hub.api.utils.get_request_stats`

## License

MIT License

## Support

For support, please contact admin@foodsharehub.com