# AI Prompt Studio - Deployment Guide

## Local Development

### Prerequisites
- Python 3.10 or higher
- pip

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Streamlit Cloud Deployment

### Initial Setup
1. Push your code to a GitHub repository
2. Go to [Share.streamlit.io](https://share.streamlit.io)
3. Click "New app" → "Deploy an app"
4. Select your repository

### Configuration
- **Main file path**: `app.py`
- **Python version**: 3.10 or higher
- **Branch**: `main` (or your default branch)

### Environment Variables
No environment variables needed for v1 (in-memory storage).

### Post-Deployment
1. Test all routes:
   - Home: `/`
   - Categories: `/?view=category&cat=cat_prospection`
   - Admin: `/?view=admincoreteam50`

## Adding Real Data

The app starts with seeded data:
- 1 Metier: Sales
- 3 Categories: Prospection, Account Planning, Négociation
- 1 Author: MansourYoum

### To add more data:
1. Access admin panel: `/?view=admincoreteam50`
2. Navigate to "Pending" tab
3. Create submissions via "CREATE PROMPT"
4. Approve submissions to publish them

## Customization

### Logo
Replace `assets/logo.png` with your Arkema logo (PNG format).

### Branding
Edit `config.py`:
- `APP_NAME`: Application title
- `PRIMARY_COLOR`: Main theme color
- `FONT_FAMILY`: Font family name

### Theme
Edit `.streamlit/config.toml` to customize colors and styling.

## Upgrade to Persistent Storage

For production use beyond v1, swap `lib/data_store.py` to use:
- SharePoint Lists API
- Azure SQL Database
- PostgreSQL
- MongoDB

The API interface remains the same, making the swap straightforward.

## Troubleshooting

### ModuleNotFoundError
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

### CSS not loading
Check browser console for Google Fonts CORS issues (usually resolves automatically).

