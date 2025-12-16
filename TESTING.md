# Testing Guide

## Testing Without a Resume

If you want to test the templates without uploading a resume or using the Gemini API, you can use the Django shell to create sample data.

### Create Sample Portfolio Data

1. Open the Django shell:
```bash
python3 manage.py shell
```

2. Run the following code:
```python
from core.models import PortfolioRequest

# Sample portfolio data
sample_data = {
    "name": "Alex Johnson",
    "tagline": "Full Stack Developer & AI Enthusiast",
    "bio": "Passionate software engineer with 5+ years of experience building scalable web applications and integrating AI/ML solutions. Specialized in modern web technologies and cloud infrastructure.",
    "contact": {
        "email": "alex.johnson@email.com",
        "phone": "+1 (555) 123-4567",
        "linkedin": "linkedin.com/in/alexjohnson",
        "github": "github.com/alexjohnson",
        "website": "alexjohnson.dev"
    },
    "skills": [
        "Python", "JavaScript", "React", "Django", "Node.js",
        "PostgreSQL", "Docker", "AWS", "Machine Learning", "REST APIs"
    ],
    "experience": [
        {
            "role": "Senior Full Stack Developer",
            "company": "Tech Innovations Inc.",
            "duration": "Jan 2021 - Present",
            "description": "Led development of microservices architecture serving 1M+ users. Implemented CI/CD pipelines reducing deployment time by 60%. Mentored junior developers and conducted code reviews.",
            "technologies": ["Python", "React", "AWS", "Docker", "PostgreSQL"]
        },
        {
            "role": "Software Developer",
            "company": "StartUp Labs",
            "duration": "Jun 2019 - Dec 2020",
            "description": "Developed RESTful APIs and responsive web applications. Integrated third-party services and payment gateways. Optimized database queries improving performance by 40%.",
            "technologies": ["JavaScript", "Node.js", "MongoDB", "Express"]
        }
    ],
    "projects": [
        {
            "name": "AI-Powered Portfolio Generator",
            "duration": "2024",
            "description": "Built an intelligent system that converts PDF resumes into beautiful portfolio websites using Google Gemini AI. Features three unique template designs and automatic data extraction.",
            "technologies": ["Python", "Django", "Gemini AI", "JavaScript"],
            "link": "github.com/alexjohnson/portfolio-generator"
        },
        {
            "name": "E-Commerce Platform",
            "duration": "2023",
            "description": "Developed a full-featured e-commerce platform with payment integration, inventory management, and real-time analytics. Handled 10K+ daily transactions.",
            "technologies": ["React", "Node.js", "Stripe", "Redis"],
            "link": "ecommerce-demo.com"
        }
    ],
    "education": [
        {
            "degree": "Bachelor of Science in Computer Science",
            "institution": "State University",
            "duration": "2015 - 2019",
            "details": "GPA: 3.8/4.0, Dean's List, Computer Science Society President"
        }
    ]
}

# Create a portfolio request with sample data
request = PortfolioRequest.objects.create(extracted_data=sample_data)
print(f"Created sample portfolio request with ID: {request.id}")
print("Store this ID in your session or use it directly in URLs")
```

3. Note the ID that's printed, then you can access the template selection page for this sample data.

## Manual Testing Workflow

### Test Template Rendering

Create a simple Python script to test template rendering:

```python
# test_templates.py
from django.template import Template, Context
import json

# Load sample data
sample_data = {
    "name": "Test User",
    "tagline": "Software Developer",
    # ... add more fields
}

# Load and render a template
with open('core/templates/portfolios/terminal/index.html', 'r') as f:
    template_content = f.read()

template = Template(template_content)
rendered = template.render(Context(sample_data))

# Save to test file
with open('test_output.html', 'w') as f:
    f.write(rendered)

print("Template rendered! Open test_output.html in your browser")
```

## Testing Individual Components

### Test PDF Extraction
```python
from core.utils import extract_text_from_pdf

text = extract_text_from_pdf('/path/to/your/resume.pdf')
print(text)
```

### Test Gemini Integration
```python
from core.utils import get_portfolio_data

sample_text = """
John Doe
Software Engineer
john@email.com | linkedin.com/in/johndoe

EXPERIENCE
Senior Developer at Tech Corp
2020-Present
- Developed web applications
- Led team of 5 developers

SKILLS
Python, JavaScript, React, Django
"""

data = get_portfolio_data(sample_text)
print(json.dumps(data, indent=2))
```

## Common Issues

### Issue: "GEMINI_API_KEY not found"
- Make sure `.env` file exists in project root
- Verify the API key is correctly set: `GEMINI_API_KEY=your_actual_key`
- Restart the Django server after adding the key

### Issue: PDF extraction returns empty text
- Some PDFs are image-based (scanned documents)
- Try extracting text manually first to verify
- Consider using OCR for image-based PDFs

### Issue: Gemini API quota exceeded
- Google Gemini has free tier limits
- Check your API usage at [Google AI Studio](https://makersuite.google.com/)
- Consider implementing caching for development

## Performance Testing

### Load Testing
```bash
# Install locust for load testing
pip install locust

# Create locustfile.py with test scenarios
# Run load test
locust -f locustfile.py
```

### Test File Upload Limits
Create test PDFs of various sizes to verify 10MB limit:
```bash
# Create a 5MB test file
dd if=/dev/zero of=test_5mb.pdf bs=1M count=5
```

## Browser Testing

Test the application in multiple browsers:
- Chrome/Chromium
- Firefox
- Safari
- Edge

Test responsive design at different screen sizes:
- Mobile (375px)
- Tablet (768px)
- Desktop (1024px+)

## Template Quality Checks

For each template, verify:
- [ ] All data fields display correctly
- [ ] Responsive design works on mobile
- [ ] Links are clickable and functional
- [ ] Print-friendly layout
- [ ] No JavaScript errors in console
- [ ] Proper semantic HTML
- [ ] Accessibility (ARIA labels, alt text)
