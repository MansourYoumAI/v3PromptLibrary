# AI Prompt Studio - Quick Start Guide

## 🚀 Getting Started

### Install & Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

Access at: `http://localhost:8501`

## 📖 Navigation Guide

### Main Views
- **Home** (`/`): Browse categories with top prompts
- **Category** (`/?view=category&cat=<category_id>`): View all prompts in a category
- **Prompt Detail** (`/?view=prompt&id=<prompt_id>`): View and interact with a prompt
- **Create Prompt** (`/?view=new`): Submit a new prompt for review
- **My Saved** (`/?view=my_saved`): Your bookmarked prompts
- **My Submitted** (`/?view=my_submitted`): Your submitted prompts

### Admin Access
**Hidden Route**: `/?view=admincoreteam50`

Features:
- Review pending submissions
- Approve/Reject prompts
- View all published prompts
- Manage categories
- View logs

## ✨ Key Features

### For Users
1. **Browse by Category**: Click any category to see relevant prompts
2. **Search**: Use the search bar on the home page
3. **Bookmark**: Save favorite prompts
4. **Rate**: Rate prompts 1-5 stars
5. **View Modes**: Toggle between CRAFT (structured) and Full (raw text)
6. **Copy Prompt**: One-click copy to clipboard
7. **Submit New**: Create and submit prompts for review

### For Admins
1. **Review Queue**: See all pending submissions
2. **Approve/Reject**: With one click
3. **Publish**: Approved prompts become visible to all users
4. **Manage Categories**: Add new categories on the fly
5. **Export Data**: Download CSV files

## 📝 Creating a Prompt

1. Click **CREATE PROMPT**
2. Fill in basic info (name, description, category, author)
3. Complete the 5 CRAFT fields:
   - **CONTEXT**: Background information
   - **ROLE**: The AI's role
   - **ACTION**: What to do
   - **FORMAT**: How to structure the output
   - **TONE**: Writing style
4. Preview the full text
5. Submit for review

## 🎨 CRAFT Framework

All prompts use the CRAFT structure:
- **C**ontext: Set the scene
- **R**ole: Define the AI's role
- **A**ction: Specify the task
- **F**ormat: Structure the response
- **T**one: Set the writing style

Example:
```
CONTEXT: You are helping a sales team with account planning.
ROLE: Act as a strategic sales advisor
ACTION: Create a detailed account plan
FORMAT: Bullet points with sections
TONE: Professional and concise
```

## 🔍 Tips

- **Default sorting**: Highest rated first
- **Bookmarks**: Access your saved prompts anytime
- **Admin route**: Use `/?view=admincoreteam50` (no link in UI)
- **Search**: Uses token-based AND matching across all fields
- **Ratings**: Updates in real-time; affects sorting

## 📊 Data Model

### Current State (v1)
- **Storage**: In-memory (resets on restart)
- **User**: Single guest user
- **Metier**: Sales only
- **Categories**: Prospection, Account Planning, Négociation

### Future (v2+)
- Persistent storage (SharePoint/Azure SQL)
- Multiple users with profiles
- Multiple metiers
- Entra ID SSO
- Usage analytics

## 🛠️ Troubleshooting

### Navigation not working
Ensure you have the latest Streamlit version: `pip install --upgrade streamlit`

### CSS not loading
Clear browser cache or hard refresh (Ctrl+Shift+R)

### Can't see admin panel
Use exact URL: `/?view=admincoreteam50`

### Empty categories
Create prompts first, then categories will populate

## 📞 Support

For issues or questions, contact the development team.

