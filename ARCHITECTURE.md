# User Flow Diagram

## Complete Application Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    🏠 HOME PAGE (/)                             │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │                                                         │    │
│  │   📄 Drag & Drop PDF Resume Upload                     │    │
│  │   • Max 10MB                                            │    │
│  │   • PDF format only                                     │    │
│  │   • Visual file feedback                                │    │
│  │                                                         │    │
│  │   [Generate My Portfolio Button]                       │    │
│  │                                                         │    │
│  └───────────────────────────────────────────────────────┘    │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│            🤖 Backend Processing (views.upload_resume)          │
│                                                                 │
│  1. Save PDF to media/resumes/                                 │
│  2. Extract text with pypdf                                    │
│  3. Call Google Gemini API                                     │
│  4. Parse & structure data                                     │
│  5. Save to database                                           │
│  6. Store ID in session                                        │
│                                                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│           📋 TEMPLATE SELECTION (/select-template/)             │
│                                                                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │ Terminal   │  │Renaissance │  │ Newspaper  │               │
│  │ Template   │  │ Template   │  │ Template   │               │
│  │            │  │            │  │            │               │
│  │ [Preview]  │  │ [Preview]  │  │ [Preview]  │               │
│  │ [Download] │  │ [Download] │  │ [Download] │               │
│  └────────────┘  └────────────┘  └────────────┘               │
│                                                                 │
└────────────┬──────────────────────┬─────────────────────────────┘
             │                      │
             │ (Preview)            │ (Download)
             ▼                      ▼
┌──────────────────────┐  ┌──────────────────────────────────────┐
│                      │  │                                      │
│  🔍 PREVIEW WINDOW   │  │  📦 DOWNLOAD GENERATION              │
│ (/preview/template/) │  │  (/download/template/)               │
│                      │  │                                      │
│  • New tab/window    │  │  1. Load template HTML               │
│  • Fully interactive │  │  2. Render with user data            │
│  • Navigate sections │  │  3. Create ZIP file:                 │
│  • Live data         │  │     - index.html (rendered)          │
│                      │  │     - CSS files                      │
│                      │  │     - JS files (if any)              │
│                      │  │     - Images (if any)                │
│                      │  │  4. Send as download                 │
│                      │  │                                      │
└──────────────────────┘  └──────────────────┬───────────────────┘
                                             │
                                             ▼
                                   ┌─────────────────────┐
                                   │                     │
                                   │  💾 portfolio.zip   │
                                   │                     │
                                   │  Ready to deploy!   │
                                   │                     │
                                   └─────────────────────┘
```

## Data Flow

```
PDF Resume
    │
    ├──> Extract Text (pypdf)
    │        │
    │        └──> Raw Text String
    │
    ├──> Send to Gemini AI
    │        │
    │        └──> Structured JSON:
    │             {
    │               "name": "...",
    │               "tagline": "...",
    │               "bio": "...",
    │               "contact": {...},
    │               "skills": [...],
    │               "experience": [...],
    │               "projects": [...],
    │               "education": [...]
    │             }
    │
    ├──> Save to Database
    │        │
    │        └──> PortfolioRequest Model
    │
    └──> Render Templates
             │
             ├──> Terminal Style
             ├──> Renaissance Style
             └──> Newspaper Style
```

## Database Schema

```
PortfolioRequest
├── id (AutoField)
├── resume_file (FileField) → media/resumes/
├── extracted_data (JSONField) → Gemini output
├── created_at (DateTime)
└── updated_at (DateTime)

PortfolioTemplate
├── id (AutoField)
├── name (CharField) → "Terminal", "Renaissance", "Newspaper"
├── description (TextField)
├── thumbnail (ImageField) → media/thumbnails/
├── template_file_path (CharField) → Path to HTML
├── slug (SlugField) → "terminal", "renaissance", "newspaper"
├── is_active (BooleanField)
└── created_at (DateTime)
```

## Template Rendering Process

```
1. User selects template → GET request with slug

2. Fetch from database:
   - PortfolioRequest (from session ID)
   - PortfolioTemplate (from slug)

3. Load template file:
   core/templates/portfolios/{slug}/index.html

4. Django Template Engine:
   - Parse Django template syntax {{ variable }}
   - Replace with user data
   - Execute template logic {% for ... %}

5. Output:
   - Preview: Rendered HTML → HttpResponse
   - Download: Rendered HTML + Assets → ZIP file
```

## Session Management

```
┌──────────────────────────────────────────┐
│ User uploads resume                      │
├──────────────────────────────────────────┤
│ Server processes and saves:              │
│   portfolio_request_id = 123             │
├──────────────────────────────────────────┤
│ Store in session:                        │
│   request.session['portfolio_request_id']│
│   = 123                                  │
├──────────────────────────────────────────┤
│ User navigates to template selection     │
├──────────────────────────────────────────┤
│ Server retrieves:                        │
│   id = request.session.get(              │
│     'portfolio_request_id'               │
│   )                                      │
├──────────────────────────────────────────┤
│ Fetch data and display templates         │
└──────────────────────────────────────────┘
```

## Error Handling Flow

```
Upload Error
├── File too large (>10MB) → Form validation error
├── Not a PDF → Form validation error  
├── PDF extraction fails → Utils exception
├── Gemini API error → Utils exception
└── Display error message → Redirect to home

Template Selection Error
├── No session ID → Redirect to home with message
├── Invalid request ID → 404 error
└── No extracted data → Redirect to home

Download Error
├── Template not found → 404 error
├── Missing data → Redirect to home
└── ZIP creation fails → Server error
```

## API Integration Points

```
Google Gemini API

Request:
POST https://generativelanguage.googleapis.com/...
Headers:
  - API Key from environment variable
Body:
  - Prompt with resume text
  - Instructions for JSON structure

Response:
{
  "candidates": [{
    "content": {
      "parts": [{
        "text": "{...JSON data...}"
      }]
    }
  }]
}

Parse → Extract JSON → Validate → Save
```

## File Structure for Downloaded Portfolio

```
portfolio_{template_slug}.zip
│
├── index.html (rendered with user data)
│
└── assets/ (if template has additional files)
    ├── css/
    │   └── style.css
    ├── js/
    │   └── script.js
    └── images/
        └── (any template images)
```

Note: Currently, templates are self-contained in single HTML files with inline CSS and minimal JS.

## Environment Configuration

```
.env file:
├── GEMINI_API_KEY=your_key_here
│
Django settings.py reads:
├── os.getenv('GEMINI_API_KEY')
│
Used in:
└── core/utils.py → genai.configure(api_key=...)
```
