import json
import os
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

class TextDatabase:
    """
    A simple file-based database for storing humanized text entries.
    """
    
    def __init__(self, db_file: str = "text_database.json"):
        """Initialize the database with the specified file."""
        self.db_file = db_file
        self.data = self._load_data()
        
    def _load_data(self) -> Dict:
        """Load data from the database file."""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # Return default structure if file is corrupt or can't be read
                return {"texts": [], "metadata": {"version": "1.0", "created": datetime.now().isoformat()}}
        else:
            # Create new database with default structure
            data = {
                "texts": [],
                "metadata": {
                    "version": "1.0",
                    "created": datetime.now().isoformat()
                }
            }
            self._save_data(data)
            return data
    
    def _save_data(self, data: Optional[Dict] = None) -> None:
        """Save data to the database file."""
        if data is None:
            data = self.data
        
        try:
            with open(self.db_file, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving database: {e}")
    
    def save_text(self, original_text: str, humanized_text: str, 
                 humanize_level: int, metadata: Optional[Dict] = None) -> str:
        """
        Save a humanized text entry to the database.
        
        Args:
            original_text: The original AI-generated text
            humanized_text: The humanized version of the text
            humanize_level: The humanization level used (1-5)
            metadata: Additional metadata about the text
            
        Returns:
            The ID of the newly created text entry
        """
        entry_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        if metadata is None:
            metadata = {}
        
        entry = {
            "id": entry_id,
            "original_text": original_text,
            "humanized_text": humanized_text,
            "humanize_level": humanize_level,
            "created_at": timestamp,
            "metadata": {
                **metadata,
                "word_count_original": len(original_text.split()),
                "word_count_humanized": len(humanized_text.split()),
            }
        }
        
        self.data["texts"].append(entry)
        self._save_data()
        
        return entry_id
    
    def get_text(self, entry_id: str) -> Optional[Dict]:
        """Retrieve a specific text entry by ID."""
        for entry in self.data["texts"]:
            if entry["id"] == entry_id:
                return entry
        return None
    
    def get_all_texts(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        Retrieve all text entries, with pagination.
        
        Args:
            limit: Maximum number of entries to return
            offset: Number of entries to skip
            
        Returns:
            A list of text entries
        """
        texts = self.data["texts"]
        # Sort by creation date (newest first)
        texts = sorted(texts, key=lambda x: x["created_at"], reverse=True)
        
        return texts[offset:offset+limit]
    
    def search_texts(self, query: str) -> List[Dict]:
        """
        Search for text entries containing the query string.
        
        Args:
            query: The search term to look for in original or humanized text
            
        Returns:
            A list of matching text entries
        """
        query = query.lower()
        results = []
        
        for entry in self.data["texts"]:
            if (query in entry["original_text"].lower() or 
                query in entry["humanized_text"].lower()):
                results.append(entry)
                
        return results
    
    def delete_text(self, entry_id: str) -> bool:
        """
        Delete a text entry by ID.
        
        Args:
            entry_id: The ID of the entry to delete
            
        Returns:
            True if the entry was deleted, False otherwise
        """
        for i, entry in enumerate(self.data["texts"]):
            if entry["id"] == entry_id:
                self.data["texts"].pop(i)
                self._save_data()
                return True
        return False
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the database.
        
        Returns:
            A dictionary with database statistics
        """
        texts = self.data["texts"]
        
        total_entries = len(texts)
        if total_entries == 0:
            return {
                "total_entries": 0,
                "avg_humanize_level": 0,
                "most_recent": None,
                "total_words_processed": 0
            }
            
        total_level = sum(entry["humanize_level"] for entry in texts)
        avg_level = total_level / total_entries if total_entries > 0 else 0
        
        total_words = sum(entry["metadata"].get("word_count_original", 0) for entry in texts)
        
        # Get most recent entry
        most_recent = sorted(texts, key=lambda x: x["created_at"], reverse=True)[0]
        
        return {
            "total_entries": total_entries,
            "avg_humanize_level": round(avg_level, 1),
            "most_recent": most_recent["created_at"],
            "total_words_processed": total_words
        }
    
    def clear_database(self) -> None:
        """Clear all entries from the database."""
        self.data["texts"] = []
        self._save_data()


# Example usage
if __name__ == "__main__":
    db = TextDatabase()
    
    # Example: Save a text entry
    entry_id = db.save_text(
        original_text="The implementation of machine learning algorithms in healthcare settings has demonstrated significant potential for improving diagnostic accuracy.",
        humanized_text="Machine learning in healthcare has shown great promise for making diagnoses more accurate.",
        humanize_level=3,
        metadata={"source": "example"}
    )
    
    # Example: Retrieve the entry
    entry = db.get_text(entry_id)
    if entry:
        print(f"Retrieved entry: {entry['humanized_text']}")
    else:
        print("Entry not found")
    
    # Example: Get all texts
    all_texts = db.get_all_texts()
    print(f"Total entries: {len(all_texts)}")