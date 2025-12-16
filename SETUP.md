# Setup and Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation Steps

### 1. Clone or Download the Project

```bash
cd /home/mritunjay/Desktop/PortfolioMaker
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Configuration File

Create a `config.properties` file in the project root:

```bash
cp config.properties.example config.properties
```

Then edit `config.properties` and add your Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

### 5. Run Database Migrations

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 6. Initialize Templates

```bash
python3 manage.py init_templates
```

### 7. Create a Superuser (Optional, for Admin Access)

```bash
python3 manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python3 manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## Usage

1. **Upload Resume**: Go to the home page and upload your PDF resume
2. **AI Processing**: The system will use Google Gemini AI to extract and enhance your resume data
3. **Select Template**: Choose from three unique designs:
   - **Terminal**: Hacker-style command-line interface
   - **Renaissance**: Classical art-inspired design
   - **Newspaper**: Vintage newspaper layout
4. **Preview**: Click "Preview" to see your portfolio in a new tab
5. **Download**: Click "Download" to get a ZIP file with your complete portfolio website

## Templates Overview

### Terminal Template
- Retro command-line interface aesthetic
- Green monospace text on dark background
- Scanline effects and blinking cursor
- Perfect for developers and tech professionals

### Renaissance Template
- Ornate classical typography
- Parchment-like textures
- Decorative flourishes and borders
- Ideal for creative professionals and artists

### Newspaper Template
- Classic print newspaper layout
- Multi-column responsive design
- Bold headlines and classified ad styling
- Great for journalists, writers, and traditional professionals

## Project Structure

```
PortfolioMaker/
├── portfolio_builder/        # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                     # Main application
│   ├── management/
│   │   └── commands/
│   │       └── init_templates.py
│   ├── templates/
│   │   ├── core/             # App templates
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   └── select_template.html
│   │   └── portfolios/       # Portfolio templates
│   │       ├── terminal/
│   │       ├── renaissance/
│   │       └── newspaper/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── media/                    # Uploaded files
├── config.properties         # Configuration file
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## Troubleshooting

### Issue: "Module not found" errors
**Solution**: Make sure you've activated your virtual environment and installed all dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "GEMINI_API_KEY not found"
**Solution**: Ensure you've created a `config.properties` file and added your API key:
```
GEMINI_API_KEY=your_key_here
```

### Issue: Template not showing up
**Solution**: Run the init_templates command:
```bash
python3 manage.py init_templates
```

### Issue: PDF extraction fails
**Solution**: Ensure your PDF is not password-protected and under 10MB

## Admin Panel

Access the Django admin panel at `http://127.0.0.1:8000/admin/` to:
- View all portfolio requests
- Manage templates
- Configure system settings

## Development

To modify templates:
1. Edit the HTML files in `core/templates/portfolios/`
2. Templates use Django template syntax with variables like `{{ name }}`, `{{ bio }}`, etc.
3. Test changes by uploading a resume and previewing

## Deployment

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Collect static files: `python manage.py collectstatic`
5. Use a production server like Gunicorn or uWSGI
6. Set up HTTPS

## License

See LICENSE file for details.

## Support

For issues or questions, please check the documentation or create an issue in the repository.
