"""In-memory data store for AI Prompt Studio."""

import uuid
from typing import Optional, List, Dict
from datetime import datetime
import config


class DataStore:
    """In-memory database for the application."""
    
    def __init__(self):
        self.metiers: List[Dict] = []
        self.categories: List[Dict] = []
        self.authors: List[Dict] = []
        self.prompts: List[Dict] = []
        self.submissions: List[Dict] = []
        self.ratings: List[Dict] = []
        self.bookmarks: List[Dict] = []
        
        # Seed data
        self._seed_data()
    
    def _seed_data(self):
        """Initialize with seed data."""
        # Seed metiers
        for metier_data in config.SEED_METIERS:
            metier = metier_data.copy()
            metier.setdefault("id", f"metier_{metier_data['name'].lower()}")
            self.metiers.append(metier)
        
        # Seed categories
        for cat_data in config.SEED_CATEGORIES:
            category = {
                "id": f"cat_{cat_data['name'].lower().replace(' ', '_')}",
                "metier_id": cat_data["metier_id"],
                "name": cat_data["name"],
                "is_active": cat_data.get("is_active", True)
            }
            self.categories.append(category)
        
        # Seed authors
        for author_data in config.SEED_AUTHORS:
            author = author_data.copy()
            author.setdefault("normalized_key", f"auth_{author_data['display_name'].lower()}")
            self.authors.append(author)
    
    def list_metiers(self, active_only: bool = True) -> List[Dict]:
        """List all metiers."""
        result = self.metiers
        if active_only:
            result = [m for m in result if m.get("is_active", True)]
        return result
    
    def list_categories(self, metier_id: str, active_only: bool = True) -> List[Dict]:
        """List categories for a metier."""
        result = [c for c in self.categories if c.get("metier_id") == metier_id]
        if active_only:
            result = [c for c in result if c.get("is_active", True)]
        return result
    
    def get_category(self, category_id: str) -> Optional[Dict]:
        """Get a category by ID."""
        for cat in self.categories:
            if cat["id"] == category_id:
                return cat
        return None
    
    def get_or_create_category(self, metier_id: str, name: str) -> Dict:
        """Get or create a category."""
        # Normalize name for ID
        cat_id = f"cat_{name.lower().replace(' ', '_')}"
        
        # Check if exists
        for cat in self.categories:
            if cat["id"] == cat_id and cat["metier_id"] == metier_id:
                return cat
        
        # Create new
        new_cat = {
            "id": cat_id,
            "metier_id": metier_id,
            "name": name,
            "is_active": True
        }
        self.categories.append(new_cat)
        return new_cat
    
    def list_authors(self, active_only: bool = True) -> List[Dict]:
        """List all authors."""
        result = self.authors
        if active_only:
            result = [a for a in result if a.get("is_active", True)]
        return result
    
    def get_author(self, author_id: str) -> Optional[Dict]:
        """Get an author by ID."""
        for author in self.authors:
            if author["id"] == author_id:
                return author
        return None
    
    def get_or_create_author(self, display_name: str) -> Dict:
        """Get or create an author."""
        from lib.utils import normalize_key
        
        normalized = normalize_key(display_name)
        
        # Check if exists
        for author in self.authors:
            if author.get("normalized_key") == normalized:
                return author
        
        # Create new
        new_author = {
            "id": f"auth_{normalized}",
            "display_name": display_name,
            "normalized_key": normalized,
            "is_active": True
        }
        self.authors.append(new_author)
        return new_author
    
    def create_submission(self, payload: Dict) -> Dict:
        """Create a new submission."""
        sub_id = str(uuid.uuid4())
        submission = {
            "id": sub_id,
            "status": "pending",
            "created_by": payload.get("created_by", "guest"),
            "created_at": datetime.now().isoformat(),
            "title": payload.get("title"),
            "description": payload.get("description"),
            "metier_id": payload.get("metier_id"),
            "category_id": payload.get("category_id"),
            "category_name": payload.get("category_name"),
            "author_id": payload.get("author_id"),
            "author_display_name_snapshot": payload.get("author_display_name_snapshot"),
            "craft_context": payload.get("craft_context"),
            "craft_role": payload.get("craft_role"),
            "craft_action": payload.get("craft_action"),
            "craft_format": payload.get("craft_format"),
            "craft_tone": payload.get("craft_tone"),
            "full_text": payload.get("full_text"),
            "review_comment": "",
            "published_prompt_id": None
        }
        self.submissions.append(submission)
        return submission
    
    def list_submissions(self, status: Optional[str] = None) -> List[Dict]:
        """List submissions."""
        result = self.submissions
        if status:
            result = [s for s in result if s.get("status") == status]
        return result
    
    def get_submission(self, submission_id: str) -> Optional[Dict]:
        """Get a submission by ID."""
        for sub in self.submissions:
            if sub["id"] == submission_id:
                return sub
        return None
    
    def approve_submission(self, sub_id: str) -> Optional[Dict]:
        """Approve a submission and create a published prompt."""
        submission = self.get_submission(sub_id)
        if not submission:
            return None
        
        # Create prompt from submission
        prompt_id = str(uuid.uuid4())
        prompt = {
            "id": prompt_id,
            "title": submission["title"],
            "description": submission["description"],
            "metier_id": submission["metier_id"],
            "category_id": submission["category_id"],
            "category_name": submission["category_name"],
            "author_id": submission["author_id"],
            "author_display_name_snapshot": submission["author_display_name_snapshot"],
            "craft_context": submission["craft_context"],
            "craft_role": submission["craft_role"],
            "craft_action": submission["craft_action"],
            "craft_format": submission["craft_format"],
            "craft_tone": submission["craft_tone"],
            "full_text": submission["full_text"],
            "avg_rating": 0.0,
            "uses_total": 0,
            "status": "published",
            "version": "1.0",
            "created_at": datetime.now().isoformat()
        }
        self.prompts.append(prompt)
        
        # Update submission
        submission["status"] = "approved"
        submission["published_prompt_id"] = prompt_id
        
        return prompt
    
    def reject_submission(self, sub_id: str, comment: str = "") -> None:
        """Reject a submission."""
        submission = self.get_submission(sub_id)
        if submission:
            submission["status"] = "rejected"
            submission["review_comment"] = comment
    
    def list_prompts(self, metier_id: Optional[str] = None, category_id: Optional[str] = None) -> List[Dict]:
        """List published prompts."""
        result = [p for p in self.prompts if p.get("status") == "published"]
        
        if metier_id:
            result = [p for p in result if p.get("metier_id") == metier_id]
        
        if category_id:
            result = [p for p in result if p.get("category_id") == category_id]
        
        return result
    
    def get_prompt(self, prompt_id: str) -> Optional[Dict]:
        """Get a prompt by ID."""
        for prompt in self.prompts:
            if prompt["id"] == prompt_id:
                return prompt
        return None
    
    def _recompute_avg_rating(self, prompt_id: str) -> None:
        """Recompute average rating for a prompt."""
        prompt_ratings = [r for r in self.ratings if r.get("prompt_id") == prompt_id]
        if prompt_ratings:
            avg = sum(r["stars"] for r in prompt_ratings) / len(prompt_ratings)
            prompt = self.get_prompt(prompt_id)
            if prompt:
                prompt["avg_rating"] = avg
        else:
            prompt = self.get_prompt(prompt_id)
            if prompt:
                prompt["avg_rating"] = 0.0
    
    def rate_prompt(self, user_key: str, prompt_id: str, stars: int) -> None:
        """Rate a prompt."""
        # Remove existing rating
        self.ratings = [r for r in self.ratings 
                       if not (r.get("user_key") == user_key and r.get("prompt_id") == prompt_id)]
        
        # Add new rating
        rating = {
            "user_key": user_key,
            "prompt_id": prompt_id,
            "stars": stars,
            "created_at": datetime.now().isoformat()
        }
        self.ratings.append(rating)
        
        # Recompute average
        self._recompute_avg_rating(prompt_id)
    
    def toggle_bookmark(self, user_key: str, prompt_id: str) -> bool:
        """Toggle bookmark for a prompt.
        
        Returns:
            True if added, False if removed
        """
        # Check if exists
        for bm in self.bookmarks:
            if bm.get("user_key") == user_key and bm.get("prompt_id") == prompt_id:
                self.bookmarks.remove(bm)
                return False
        
        # Add new bookmark
        bookmark = {
            "user_key": user_key,
            "prompt_id": prompt_id,
            "created_at": datetime.now().isoformat()
        }
        self.bookmarks.append(bookmark)
        return True
    
    def is_bookmarked(self, user_key: str, prompt_id: str) -> bool:
        """Check if a prompt is bookmarked."""
        for bm in self.bookmarks:
            if bm.get("user_key") == user_key and bm.get("prompt_id") == prompt_id:
                return True
        return False
    
    def list_bookmarks(self, user_key: str) -> List[Dict]:
        """List bookmarked prompts for a user."""
        bookmark_prompt_ids = [bm["prompt_id"] for bm in self.bookmarks 
                             if bm.get("user_key") == user_key]
        return [self.get_prompt(pid) for pid in bookmark_prompt_ids if self.get_prompt(pid)]


# Global instance
_db = DataStore()


def get_db() -> DataStore:
    """Get the global database instance."""
    return _db


