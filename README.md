# CV Analyzer

A sophisticated CV analyzer that matches CVs against job opportunities using AI agents.

## 🚀 Features

- **PDF CV Processing**: Extract text from PDF CVs using multiple strategies
- **AI-Powered Analysis**: Uses Google Gemini (free tier) for intelligent CV parsing
- **Job Description Analysis**: Extract requirements from job postings
- **Smart Matching**: AI-powered compatibility scoring between CVs and jobs
- **Detailed Insights**: Comprehensive recommendations and interview tips
- **Clean Architecture**: Modular, testable, and maintainable codebase
- **RESTful API**: Easy integration with other systems

## 🏗️ Architecture

```
src/
├── domain/          # Core business logic (entities, repositories, services)
├── application/     # Use cases and application services
├── infrastructure/  # External dependencies (AI, PDF, database)
└── presentation/    # API endpoints and schemas
```

## 🛠️ Technology Stack

- **Backend**: Python 3.12, FastAPI
- **AI**: Google Gemini (free tier), Hugging Face (optional)
- **PDF Processing**: pdfplumber, PyPDF2
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Architecture**: Clean Architecture principles

## 📋 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd cv_analiser
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your Google API key
```

Get your **free** Google Gemini API key from: https://makersuite.google.com/app/apikey

### 3. Run the Application

```bash
python main.py
```

The API will be available at:
- **Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### CV Management
- `POST /api/v1/cv/upload` - Upload and analyze CV (PDF)
- `GET /api/v1/cv/` - List uploaded CVs

### Job Analysis
- `POST /api/v1/job/analyze` - Analyze job description
- `GET /api/v1/job/` - List analyzed jobs

### CV-Job Matching
- `POST /api/v1/match/analyze` - Create match analysis
- `GET /api/v1/match/{match_id}` - Get match results

## 🧪 Testing the API

### 1. Upload a CV

```bash
curl -X POST "http://localhost:8000/api/v1/cv/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/cv.pdf"
```

### 2. Analyze a Job Description

```bash
curl -X POST "http://localhost:8000/api/v1/job/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "company": "Tech Corp",
    "description": "We are looking for a senior Python developer with 5+ years of experience...",
    "location": "San Francisco, CA"
  }'
```

### 3. Check Health

```bash
curl http://localhost:8000/health
```

## 🎯 Example Response

### CV Upload Response
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "filename": "john_doe_cv.pdf",
  "message": "CV uploaded and analyzed successfully",
  "extracted_data": {
    "name": "John Doe",
    "email": "john@example.com",
    "skills": [
      {"name": "Python", "level": "advanced"},
      {"name": "FastAPI", "level": "intermediate"}
    ],
    "experience_years": 5.2,
    "education": [
      {"degree": "Bachelor of Computer Science", "institution": "Tech University"}
    ],
    "certifications": ["AWS Certified Developer"]
  }
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key (required) | "" |
| `DEBUG` | Enable debug mode | false |
| `MAX_FILE_SIZE_MB` | Max PDF file size | 10 |
| `LOG_LEVEL` | Logging level | INFO |

### Free Tier Limits

- **Google Gemini**: 15 requests/minute, 1,500 requests/day (very generous!)
- **File Upload**: 10MB max PDF size
- **Processing**: ~5-30 seconds per CV depending on complexity

## 🎨 Key Features Explained

### 1. **Smart CV Parsing**
- Extracts personal info, skills, experience, education
- Handles various CV formats and layouts
- Categorizes skills (programming, soft skills, tools)
- Calculates total experience in years

### 2. **Job Requirement Analysis**
- Identifies required vs preferred skills
- Extracts experience requirements
- Categorizes mandatory vs nice-to-have qualifications
- Determines skill importance weights

### 3. **Intelligent Matching**
- Multi-dimensional scoring (skills, experience, education)
- Gap analysis with specific recommendations
- Interview preparation tips
- Recommendation levels (Highly Recommended, Recommended, etc.)

## 🚀 Next Steps (Future Development)

1. **Database Integration**: PostgreSQL with SQLAlchemy
2. **User Authentication**: JWT-based user management
3. **Batch Processing**: Analyze multiple CVs against multiple jobs
4. **Advanced Matching**: Machine learning-based scoring
5. **Export Features**: PDF reports, Excel exports
6. **Dashboard**: Web interface for HR managers
7. **Integration**: ATS systems, job boards

## 🛠️ Development Setup

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality:

```bash
# Install pre-commit (included in requirements.txt)
pip install pre-commit

# Install the git hooks
pre-commit install

# Run on all files manually
pre-commit run --all-files
```

**What the hooks do:**
- **Black**: Auto-formats Python code (79 char line length)
- **isort**: Sorts and organizes imports
- **flake8**: Lints code for style and errors
- **General**: Trims whitespace, fixes file endings, checks YAML/JSON

The hooks run automatically on `git commit` and only process changed files, keeping your commits clean and consistent!

### Code Style

- **Line Length**: 79 characters (configured in `pyproject.toml`)
- **Formatter**: Black with isort for imports
- **Linter**: flake8 with custom rules
- **Architecture**: Clean Architecture principles

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

For support, please:
1. Check the API documentation at `/docs`
2. Review the health endpoint at `/health`
3. Check the logs for detailed error information
4. Open an issue on GitHub

---

**Built with ❤️ using Clean Architecture and Google Gemini AI**
