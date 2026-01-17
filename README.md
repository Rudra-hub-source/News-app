# 📰 News Management App

A modern, interactive news management system built with Flask featuring dual database support (SQLite for development, PostgreSQL for production), sleek dark theme with gradient animations and comprehensive CRUD operations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-orange.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.0+-blue.svg)

## ✨ Features

- 📝 **Full CRUD Operations** - Create, read, update, and delete articles
- 🗄️ **Dual Database Support** - SQLite for development, PostgreSQL for production
- 🎨 **Modern Interactive UI** - Gradient backgrounds, animations, and hover effects
- 🖼️ **Image Management** - Upload and manage article images
- 🔍 **Search Functionality** - Search articles by title and content
- 📱 **Responsive Design** - Works seamlessly on all devices
- 🕐 **IST Timezone Support** - Displays correct Indian Standard Time
- 🏷️ **Category System** - Organize articles by categories
- 📊 **Article Statistics** - View counts and performance metrics

## 🚀 Quick Start

### 1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run the application (uses SQLite by default):

```bash
python app.py
```

### 4. Open your browser:

```
http://127.0.0.1:5000
```

### 5. Initialize with sample data:

```
http://127.0.0.1:5000/initdb
```

## 🐘 PostgreSQL Setup (Optional for Local Development)

### For PostgreSQL in development:

```bash
# Install PostgreSQL and create database
createdb news_app

# Set environment variable
export DATABASE_URL="postgresql://postgres:password@localhost:5432/news_app"

# Run the application
python app.py
```

## 📁 Project Structure

```
News-app/
├── 📄 README.md                           # Project documentation
├── 📄 requirements.txt                    # Python dependencies
├── 📄 app.py                             # Main Flask application entry point
├── 📄 .gitignore                         # Git ignore file
├── 📄 .env                               # Environment variables (optional)
│
├── 📁 backend/                           # 🐍 PYTHON BACKEND
│   ├── 📄 __init__.py                    # Package initialization
│   ├── 📄 state.py                       # Database configuration & Flask app setup
│   ├── 📄 router.py                      # Main router configuration
│   │
│   ├── 📁 controllers/                   # 🎮 Route handlers (Flask blueprints)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 article_controller.py      # Article CRUD operations
│   │   ├── 📄 home_controller.py         # Home page routes
│   │   ├── 📄 category_controller.py     # Category-based routes
│   │   └── 📄 media_controller.py        # Image upload/management
│   │
│   ├── 📁 models/                        # 🗄️ Database models (SQLAlchemy)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 article.py                 # Article model with IST timezone
│   │   └── 📄 media.py                   # Media/Image model
│   │
│   └── 📁 services/                      # ⚙️ Business logic layer
│       ├── 📄 __init__.py
│       ├── 📄 article_service.py         # Article business operations
│       └── 📄 media_service.py           # Media handling services
│
├── 📁 frontend/                          # 🎨 FRONTEND ASSETS
│   │
│   ├── 📁 templates/                     # 📋 Jinja2 HTML templates
│   │   ├── 📄 layout.html                # Base template with navigation
│   │   ├── 📄 home.html                  # Homepage template
│   │   ├── 📄 articles.html              # My Articles page (enhanced)
│   │   ├── 📄 article_create.html        # Create article form (streamlined)
│   │   ├── 📄 article_detail.html        # Article view page (animated)
│   │   ├── 📄 article_edit.html          # Edit article page (enhanced)
│   │   ├── 📄 category.html              # Category-based articles
│   │   ├── 📄 trending_articles.html     # Trending articles page
│   │   ├── 📄 latest_articles.html       # Latest articles page
│   │   ├── 📄 media_library.html         # Media management
│   │   ├── 📄 media_library_simple.html  # Simple media view
│   │   ├── 📄 media_upload.html          # Media upload interface
│   │   └── 📄 media_upload_simple.html   # Simple upload form
│   │
│   └── 📁 static/                        # 🎯 Static assets
│       │
│       ├── 📁 css/                      # 🎨 Stylesheets
│       │   ├── 📄 main.css               # Main stylesheet
│       │   ├── 📄 components.css         # Component-specific styles
│       │   ├── 📄 animations.css         # Animation definitions
│       │   └── 📄 responsive.css         # Responsive design rules
│       │
│       ├── 📁 js/                       # ⚡ JavaScript files
│       │   ├── 📄 main.js                # Main JavaScript functionality
│       │   ├── 📄 article.js             # Article-specific JS
│       │   ├── 📄 components.js          # Reusable components
│       │   ├── 📄 animations.js          # Animation controllers
│       │   └── 📄 utils.js               # Utility functions
│       │
│       ├── 📁 images/                   # 🖼️ Static images
│       │   ├── 📄 logo.png               # App logo
│       │   ├── 📄 favicon.ico            # Favicon
│       │   ├── 📄 hero-bg.jpg            # Hero background
│       │   └── 📁 icons/                 # SVG icons
│       │       ├── 📄 article.svg
│       │       ├── 📄 edit.svg
│       │       └── 📄 delete.svg
│       │
│       └── 📁 uploads/                  # 📤 User uploaded files
│           └── 📄 .gitkeep               # Keep directory in git
│
├── 📁 database/                          # 🗃️ DATABASE & STORAGE
│   ├── 📁 instance/                     # Instance-specific files
│   │   └── 📁 uploads/                  # Uploaded media files
│   │       └── 📄 .gitkeep
│   │
│   └── 📁 migrations/                   # Database migrations (optional)
│       ├── 📄 __init__.py
│       └── 📁 versions/
│           └── 📄 001_initial_migration.py
│
├── 📁 config/                            # ⚙️ CONFIGURATION
│   ├── 📄 development.py                # Development settings
│   ├── 📄 production.py                 # Production settings
│   └── 📄 testing.py                    # Testing configuration
│
├── 📁 tests/                            # 🧪 TESTING
│   ├── 📄 __init__.py
│   ├── 📄 test_articles.py               # Article tests
│   ├── 📄 test_media.py                  # Media tests
│   └── 📄 test_routes.py                 # Route tests
│
└── 📁 docs/                             # 📚 DOCUMENTATION
    ├── 📄 API.md                         # API documentation
    ├── 📄 DEPLOYMENT.md                  # Deployment guide
    └── 📄 CONTRIBUTING.md                # Contribution guidelines
```

## 🏗️ Architecture Overview

### **📂 Folder Organization**

| Folder | Purpose | Technology |
|--------|---------|------------|
| `backend/` | 🐍 Server-side logic | Python + Flask |
| `frontend/` | 🎨 User interface | HTML + CSS + JS |
| `database/` | 🗃️ Data storage | SQLite/PostgreSQL |
| `config/` | ⚙️ App settings | Python configs |
| `tests/` | 🧪 Quality assurance | PyTest |
| `docs/` | 📚 Documentation | Markdown |

### **🔄 Data Flow**
```
User Request → Frontend (Templates) → Backend (Controllers) → Services → Models → Database
     ↓              ↑                    ↑                    ↑        ↑        ↑
  Browser ←── Static Assets ←──── Flask Routes ←──── Business Logic ←── SQLAlchemy
```

### **Backend (Python)**
- **Flask** - Lightweight web framework
- **SQLAlchemy** - ORM for database operations
- **Jinja2** - Template engine
- **Werkzeug** - WSGI utilities

### **Frontend**
- **HTML5** - Semantic structure
- **CSS3** - Modern styling with gradients & animations
- **JavaScript** - Interactive functionality
- **Tailwind CSS** - Utility-first CSS framework
- **SVG Icons** - Scalable vector graphics

### **Database**
- **Development:** SQLite - Lightweight, serverless database for local development
- **Production:** PostgreSQL - Robust, scalable relational database
- **Auto-Detection:** Uses `DATABASE_URL` environment variable to switch
- **IST Timezone:** Indian Standard Time support

## 🎨 UI Features

- **Dark Theme** - Modern dark interface with gradient accents
- **Interactive Animations** - Hover effects, scale transforms, and smooth transitions
- **Metallic Effects** - Gradient text and glowing shadows
- **Responsive Grid** - Adaptive layouts for all screen sizes
- **Reading Progress** - Visual progress bar for article reading
- **Card-based Design** - Clean, organized content presentation

## 📊 Key Functionality

### **Article Management**
- Create new articles with rich text content
- Edit existing articles with live preview
- Delete articles with confirmation dialogs
- Search articles by title and content
- View article statistics and metrics

### **Media Management**
- Upload images for articles
- Manage media library
- Image optimization and storage
- Gallery view with hover effects

### **Navigation & Categories**
- Category-based article organization
- Trending articles based on view count
- Latest articles chronologically sorted
- Breadcrumb navigation

## 🗄️ Database Configuration

### **Automatic Database Selection**
The app automatically chooses the appropriate database:

```python
# Local Development (no DATABASE_URL set)
SQLite: news.db

# Production (DATABASE_URL environment variable exists)
PostgreSQL: Managed by hosting platform
```

### **Environment Detection**
- **Local:** `sqlite:///news.db` (default fallback)
- **Production:** Uses `DATABASE_URL` from environment
- **Render/Heroku:** Automatically provides PostgreSQL connection

### **Benefits**
- ✅ **Zero Setup** - Works immediately with SQLite
- ✅ **Production Ready** - Scales with PostgreSQL
- ✅ **Platform Agnostic** - Works on any hosting service
- ✅ **Development Friendly** - No database server required locally sorted
- Breadcrumb navigation

## 🚀 Development

### **Architecture Pattern**
Follows **MVC (Model-View-Controller)** pattern:
- **Models** - Database entities and relationships
- **Views** - Jinja2 templates with modern UI
- **Controllers** - Flask blueprints handling routes
- **Services** - Business logic separation

### **Code Organization**
- Clean separation of concerns
- Modular blueprint structure
- Service layer for business logic
- Template inheritance for consistency

## 🌟 Recent Enhancements

- ✅ **Enhanced UI** - Modern animations and interactive effects
- ✅ **IST Timezone** - Correct Indian time display
- ✅ **Streamlined Forms** - Removed sidebar distractions
- ✅ **Reading Experience** - Progress bars and typography improvements
- ✅ **Image Management** - Enhanced upload and gallery features

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

Made with ❤️ by **Praveen Chandra Panda**

---

**Happy Coding! 🚀**