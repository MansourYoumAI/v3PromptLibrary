# AI Prompt Studio

A clean, professional internal app to manage and use high-quality prompts for Sales.

## Features

- **Prompt Management**: Create, view, and manage AI prompts with CRAFT structure
- **Category Organization**: Organize prompts by category (Prospection, Account Planning, Négociation)
- **Rating System**: Rate prompts and view average ratings
- **Bookmarking**: Save favorites for quick access
- **Admin Panel**: Hidden admin route for reviewing and approving prompts
- **Search**: Token-based AND search across all prompt fields

## Installation

```bash
pip install -r requirements.txt
```

## Running Locally

```bash
streamlit run app.py
```

## Deployment on Streamlit Cloud

1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Set Main file path: `app.py`
4. Deploy!

## Admin Access

Admin features are accessible via hidden route:
```
/?view=admincoreteam50
```

## Architecture

- **Framework**: Streamlit (Python 3.10+)
- **Storage**: In-memory (easily swappable for persistence layer)
- **Font**: Work Sans
- **Theme**: Light mode with primary color #188d6d

## Project Structure

```
/app.py                    # Router + global CSS/theme + sidebar
/config.py                 # Constants: branding, admin route, seeds
/requirements.txt          # streamlit, pandas, python-dateutil
/.streamlit/config.toml    # Theme configuration
/lib/
  /__init__.py
  /utils.py                # logging, normalization, helpers
  /data_store.py           # in-memory DB + CRUD + rating/bookmarks
/views/
  /__init__.py
  /home.py                 # Home grid + search
  /category.py           # Cards list + sorting + bookmark
  /prompt_detail.py       # CRAFT + Full views + copy/bookmark/rate
  /new_prompt.py          # Create prompt (CRAFT only)
  /my_saved.py            # Bookmarks of current user
  /my_submitted.py        # Submissions created by current user
  /admin.py               # Monitoring + Review/Edit + Import/Export
/assets/
  /logo.png               # Arkema logo
/logs/                    # CSV logs (runtime)
```

## Usage

### Creating a Prompt

1. Click "CREATE PROMPT"
2. Fill in name, description, category, and author
3. Complete all 5 CRAFT fields:
   - CONTEXT
   - ROLE
   - ACTION
   - FORMAT
   - TONE
4. Preview full text
5. Submit for review

### Viewing Prompts

- **Home**: Browse categories with top 3 prompts per category
- **Category**: View all prompts in a category, sorted by rating/usage
- **Detail**: Toggle between CRAFT and Full text views

### Admin Features

Access admin panel via `/?view=admincoreteam50`:
- Review pending submissions
- Approve/Reject prompts
- View published prompts
- Manage categories
- View logs

## Version

v1 - Sales only, in-memory storage

