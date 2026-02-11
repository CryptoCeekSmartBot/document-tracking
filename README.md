# Document Tracking System

## Production-Ready Django Application

### Features
✅ Unlimited Document Types (User-Managed)
✅ Custom Checkpoint Workflows
✅ Role-Based Access (Admin/Staff/Viewer)
✅ Auto-Generated Tracking IDs
✅ Progress Tracking
✅ Search & Filter
✅ Dashboard with Statistics
✅ PostgreSQL Database
✅ Ready for Railway Deployment

### Quick Start

#### 1. Local Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (optional)
python manage.py loaddata initial_data.json

# Run development server
python manage.py runserver
```

Access at: http://localhost:8000
Admin panel: http://localhost:8000/admin

#### 2. Railway Deployment

**Step 1: Create PostgreSQL Database**
- Go to Railway dashboard
- Click "New" → "Database" → "PostgreSQL"
- Copy connection details

**Step 2: Set Environment Variables**
In Railway project settings, add:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app
DB_NAME=railway
DB_USER=postgres
DB_PASSWORD=(from Railway PostgreSQL)
DB_HOST=(from Railway PostgreSQL)
DB_PORT=5432
```

**Step 3: Deploy**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up
```

**Step 4: Run Migrations**
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

### Database Models

**1. User (Custom)**
- username, password, email
- department, role (admin/staff/viewer)
- phone

**2. DocumentType** (UNLIMITED)
- type_name (user-defined)
- description
- is_active
- created_by

**3. CheckpointTemplate**
- document_type (FK)
- checkpoint_name
- sequence_order

**4. Route**
- route_name (Route A, B, C, etc.)
- description

**5. Document**
- tracking_id (auto-generated: DTS-YYYYMMDD-XXXX)
- document_type (FK)
- route (FK)
- document_date, exam_date
- current_status (pending/in_progress/finalized)
- notes

**6. DocumentCheckpoint**
- document (FK)
- checkpoint_name
- is_completed
- completed_by, completed_at
- receiver_name, remarks

### Default Admin Features

**Document Type Management:**
- Add unlimited document types
- Define checkpoints for each type
- Set checkpoint order
- Activate/deactivate types

**Document Tracking:**
- Create new documents
- Auto-load checkpoints based on type
- Mark checkpoints complete
- Track progress
- View history

**User Management:**
- Add users with roles
- Assign departments
- Manage permissions

### API Endpoints (For Future)
- GET /api/documents/ - List all documents
- POST /api/documents/ - Create document
- GET /api/documents/{id}/ - Get document details
- PATCH /api/checkpoints/{id}/ - Update checkpoint

### Tech Stack
- **Backend:** Django 6.0
- **Database:** PostgreSQL
- **Frontend:** HTML + Bootstrap 5 + JavaScript
- **Hosting:** Railway.app
- **Static Files:** WhiteNoise

### Project Structure
```
document-tracking-system/
├── config/              # Django settings
├── accounts/            # User management
├── documents/           # Core functionality
├── templates/           # HTML templates
├── static/             # CSS, JS, images
├── staticfiles/        # Collected static files
├── media/              # User uploads
├── manage.py
├── requirements.txt
├── .env.example
├── README.md
└── Procfile           # For Railway
```

### Security Checklist
✅ DEBUG=False in production
✅ Strong SECRET_KEY
✅ ALLOWED_HOSTS configured
✅ Database password secure
✅ HTTPS enabled (Railway auto)
✅ CSRF protection enabled
✅ Password validators active

### Support
For issues or questions:
1. Check Django admin panel logs
2. Review Railway deployment logs
3. Verify environment variables

### License
Proprietary - Internal Office Use Only
