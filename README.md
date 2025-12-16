# Project: AI-Powered Resume to Portfolio Generator

Transform your resume into a stunning, professional portfolio website in seconds using the power of Google Gemini AI.

## ✨ Features

- 🤖 **AI-Powered Extraction**: Google Gemini intelligently parses your resume and extracts structured data
- 🎨 **Three Unique Templates**: Choose from Terminal (hacker-style), Renaissance (classical art), or Newspaper (vintage print) designs
- 👀 **Live Preview**: See your portfolio before downloading
- 📦 **One-Click Download**: Get a complete, ready-to-deploy website as a ZIP file
- 🚀 **No Coding Required**: Upload PDF → Select Template → Download Website

## 🚀 Quick Start

1. **Set up your Gemini API key** (required):
   ```bash
   # Get your free API key from: https://makersuite.google.com/app/apikey
   # Edit config.properties file and add your key
   ```

2. **Run the server**:
   ```bash
   python3 manage.py runserver
   ```

3. **Open your browser** and visit: `http://127.0.0.1:8000/`

For detailed setup instructions, see [SETUP.md](SETUP.md)

## 📸 Templates Preview

### 1. Terminal Template
Retro hacker-style with green monospace text, scanline effects, and command-line interface aesthetics. Perfect for developers and tech professionals.

### 2. Renaissance Template
Classical art-inspired design with ornate typography, parchment textures, and decorative flourishes. Ideal for creative professionals.

### 3. Newspaper Template
Vintage newspaper layout with multi-column design, bold headlines, and print journalism aesthetic. Great for writers and journalists.

---

## 1. Project Overview

* **Objective:** Build a web application where users upload a PDF resume, select a portfolio design template, and receive a fully generated, downloadable, and navigable personal portfolio website.
* **Core Intelligence:** Use Google Gemini API to parse the resume, infer missing data contextually (e.g., writing an "About Me" if missing, or expanding on "Skills"), and map it to the chosen template's structure.

## 2. Tech Stack

* **Backend:** Python, Django (Core logic, routing, file handling).
* **AI/LLM:** Google Gemini API (`google-generativeai`) - For parsing PDF text and structured data generation.
* **PDF Processing:** `pypdf` or `pdfminer.six` (To extract raw text from PDF).
* **Frontend/Templates:**
  * *App UI:* HTML5, Tailwind CSS, JavaScript (for the dashboard).
  * *Portfolio Templates:* Standalone HTML/CSS/JS bundles (stored as static assets or Django templates) that are compatible with static site generation.
* **Database:** SQLite (for development) or PostgreSQL.
* **Utilities:** `zipfile` (Python stdlib) for bundling downloads.

## 3. System Architecture & Workflow

### Step 1: User Upload & PDF Extraction

1. User uploads `resume.pdf` via a Django form.
2. Backend saves the file temporarily.
3. **PDF Parsing:** Use `pypdf` to extract raw text strings from the document.

### Step 2: Gemini Intelligence Layer (The Core)

We will perform a two-step prompt strategy or a single structured prompt.

* **Prompt:** Send the raw PDF text + the target "Schema" of our portfolio templates to Gemini.
* **Instruction to Gemini:**
  > "Extract the following fields: Name, Title, About Me, Experience, Projects, Skills, Contact."
  > "If a field is missing (e.g., 'About Me'), generate a professional summary based on the experience listed."
  > "Format the output strictly as JSON."

### Step 3: Template Selection & Mapping

1. User browses template thumbnails (e.g., "Modern", "Minimalist", "Dev").
2. Each template corresponds to a folder containing `index.html` (with Jinja2-like placeholders) and an `assets/` folder.
3. User selects a template ID.

### Step 4: Generation & Preview

1. Django loads the selected template's HTML.
2. Django renders the HTML using the JSON data received from Gemini.
3. **Preview:** Display the rendered HTML in an `<iframe>` or a separate route so the user can navigate/click through it to verify.

### Step 5: Download

1. The system writes the rendered HTML to an `index.html` file.
2. The system copies the template's specific CSS/JS/Images folders.
3. The system zips `index.html` and `assets/` into `portfolio.zip`.
4. User downloads the zip.

## 4. Implementation Steps for Cursor

### Phase 1: Setup & Models

1. **Initialize Django:** Start project `resume_portfolio` and app `generator`.
2. **Install Requirements:** `django`, `google-generativeai`, `pypdf`, `python-dotenv`.
3. **Create Models:**

```python
class PortfolioRequest(models.Model):
    resume_file = models.FileField(upload_to='resumes/')
    extracted_data = models.JSONField(null=True, blank=True) # Stores Gemini output
    created_at = models.DateTimeField(auto_now_add=True)

class PortfolioTemplate(models.Model):
    name = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    template_file_path = models.CharField(max_length=200) # Path to the HTML file
    slug = models.SlugField(unique=True)
```

### Phase 2: AI Service (`utils.py`)

Create a helper function to interface with Gemini.

* **Function:** `parse_resume_with_gemini(text_content)`
* **Prompt Engineering:**
  > "You are a professional career consultant, specific JSON schema: {name, tag line, bio, experiences: [], projects: [], skills: [], social links: {} }. Analyze the following resume text. If the bio is missing, synthesize one from the experience. If project descriptions are short, enhance them slightly for a portfolio context. Return ONLY valid JSON."

### Phase 3: Views & Logic

* **UploadView:** Handle PDF upload → Extract Text → Call Gemini → Save JSON to session or DB → Redirect to Template Select.
* **SelectTemplateView:** Display available templates.
* **PreviewView:**
  1. Fetch extracted JSON.
  2. Load the selected template HTML file.
  3. Render it using `django.template.engines['django'].from_string(template_code).render(context)`.
  4. Return the rendered HTML as a response (for the iframe).
* **DownloadView:**
  1. Perform the same rendering as Preview.
  2. Create an in-memory ZIP file.
  3. Write the rendered HTML as `index.html`.
  4. Walk through the template's static asset folder and add those files to the ZIP.
  5. Return `FileResponse` with `application/zip`.

### Phase 4: Frontend & Templates

* **Base UI:** Simple Dashboard using Tailwind to upload file and pick cards.
* **Portfolio Templates:** Create 2-3 distinct folders in your `static/portfolio_templates/` directory:
  * `minimal/` (index.html, style.css)
  * `creative/` (index.html, js/main.js, css/style.css)
  * *Note:* The `index.html` inside these must use Django template syntax (e.g., `<h1>{{ name }}</h1>`).

## 5. Specific Prompts for Cursor (Copy/Paste these)

### Prompt 1 (Setup)

> "Create a Django project named portfolio_builder with an app named core. Configure settings.py for media file uploads and static files. Set up a simple base.html with TailwindCSS via CDN."

### Prompt 2 (Models & AI)

> "Create a utils.py file. Implement a function extract_text_from_pdf(pdf_path). Then, implement get_portfolio_data(text) using google-generativeai. The Gemini prompt should ask for a JSON structure containing: name, title, about, contact (email, linkedin, github), skills (list), experience (list of objects), and projects (list of objects). Ensure it handles missing data by inferring it from context."

### Prompt 3 (Views)

> "Create a view that accepts a file upload. Process the PDF using the utils we created. Store the resulting JSON data in the user's session (or a temporary database model) so we can use it in the next step. Redirect to a 'choose template' page."

### Prompt 4 (Rendering & Download)

> "Create a view generate_portfolio that takes a template_id. It should read a standard HTML file from a 'templates/portfolios' directory, render it with the context data from the session, and return it as a downloadable ZIP file containing the rendered HTML and all associated assets."

---

## Next Steps

Would you like me to help you refine the **Gemini Prompt** in Phase 2 to ensure the JSON comes back perfectly clean for the HTML templates?
