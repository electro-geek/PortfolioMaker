# Analytics Dashboard

This is a standalone-ish dashboard app for tracking users and visitors.

## Features
- **User Tracking**: See total registered users and how many have generated portfolios.
- **Visitor Tracking**: Track unique IP addresses, page views, and recent activity.
- **Real-time Insights**: View top visited pages and recent visit logs.

## Setup
The dashboard is already integrated into the Django project.

1. **Access**: Navigate to `/dashboard/` on your site.
2. **Security**: Only staff members (admins) can access the dashboard.
3. **Tracking**: Tracking is handled automatically via `VisitorTrackingMiddleware`.

## Files
- `views.py`: Logic for aggregating stats.
- `models.py`: Uses `Visitor` model from `core` (or could be moved here).
- `templates/dashboard/home.html`: The premium UI for the dashboard.
