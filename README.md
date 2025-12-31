# Portfolio Maker

Transform your resume into a stunning, professional portfolio website in seconds using the power of Google Gemini AI.

## ✨ Features

- 🤖 **AI-Powered Extraction**: Google Gemini intelligently parses your resume and extracts structured data
- 🎨 **Three Unique Templates**: Choose from Terminal (hacker-style), Renaissance (classical art), or Newspaper (vintage print) designs
- 👀 **Live Preview**: See your portfolio before downloading
- 📦 **One-Click Download**: Get a complete, ready-to-deploy website as a ZIP file
- 🚀 **No Coding Required**: Upload PDF → Select Template → Download Website

## 🎯 Project Overview

Portfolio Maker is a web application that allows users to upload their PDF resume, select from beautifully crafted portfolio design templates, and receive a fully generated, downloadable personal portfolio website. The application leverages Google Gemini AI to intelligently parse resumes, infer missing data contextually (such as generating an "About Me" section or expanding on skills), and seamlessly map the information to the chosen template's structure.

## 🚀 Quick Start

1. **Set up your Gemini API key**:
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

## 📸 Available Templates

### 1. Terminal Template
Retro hacker-style design with green monospace text, scanline effects, and command-line interface aesthetics. Perfect for developers and tech professionals who want to showcase their coding prowess.

### 2. Renaissance Template
Classical art-inspired design with ornate typography, parchment textures, and decorative flourishes. Ideal for creative professionals, designers, and artists.

### 3. Newspaper Template
Vintage newspaper layout with multi-column design, bold headlines, and print journalism aesthetic. Great for writers, journalists, and content creators.

## 🛠 Tech Stack

* **Backend:** Python, Django
* **AI/LLM:** Google Gemini API (`google-generativeai`)
* **PDF Processing:** `pypdf`
* **Frontend:** HTML5, Tailwind CSS, JavaScript
* **Database:** PostgreSQL (Production), SQLite (Development)

## 🔄 How It Works

1. **Upload Resume**: Users upload their resume in PDF format through a simple, intuitive interface
2. **AI Processing**: Google Gemini AI extracts and structures the resume data, intelligently filling in gaps and enhancing descriptions
3. **Choose Template**: Browse and select from three distinct, professionally designed portfolio templates
4. **Preview**: View a live preview of your generated portfolio website
5. **Download**: Download a complete, ready-to-deploy website package as a ZIP file

## 📁 Project Structure

The application follows Django's best practices with a modular architecture:

- **Core App**: Handles portfolio generation, template rendering, and file management
- **Dashboard App**: Provides analytics and user management features
- **Templates**: Three unique, standalone HTML/CSS/JS bundles for different design aesthetics
- **AI Integration**: Intelligent resume parsing and data enhancement using Google Gemini

## 🌟 Key Highlights

- **Zero Coding Required**: Anyone can create a professional portfolio website without any technical knowledge
- **Smart AI Enhancement**: Missing information is intelligently inferred from context
- **Professional Templates**: Carefully crafted designs that stand out
- **Instant Deployment**: Downloaded portfolios are ready to host on any static site platform
- **Fully Customizable Output**: Generated websites use standard HTML/CSS/JS for easy modification

---

Built with ❤️ using Django and Google Gemini AI
