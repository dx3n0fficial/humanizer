"""
Dx3n Text Humanizer - Achievement System
Created by Huzaifah Tahir (Dx3n)

This module handles the achievement and gamification system for the Dx3n Text Humanizer.
It tracks user progress, awards achievements, and stores achievement data.
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Union

# Achievement categories
CATEGORIES = {
    "beginner": "🌱 Beginner",
    "intermediate": "🔥 Intermediate",
    "advanced": "⭐ Advanced",
    "expert": "🏆 Expert",
    "secret": "🔒 Secret"
}

# Default achievements list
DEFAULT_ACHIEVEMENTS = [
    {
        "id": "first_humanize",
        "name": "First Transformation",
        "description": "Humanize your first AI-generated text",
        "category": "beginner",
        "icon": "🚀",
        "points": 10,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 1
    },
    {
        "id": "five_humanizations",
        "name": "Getting Started",
        "description": "Humanize 5 different texts",
        "category": "beginner",
        "icon": "📝",
        "points": 20,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 5
    },
    {
        "id": "try_all_levels",
        "name": "Level Explorer",
        "description": "Try all 5 humanization levels",
        "category": "beginner",
        "icon": "🔍",
        "points": 30,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 5,
        "progress_detail": {
            "levels_used": []
        }
    },
    {
        "id": "save_text",
        "name": "Collector",
        "description": "Save your first humanized text",
        "category": "beginner",
        "icon": "💾",
        "points": 15,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 1
    },
    {
        "id": "scholarship",
        "name": "Academic Writer",
        "description": "Humanize 3 texts using Level 5 (Scholarly)",
        "category": "intermediate",
        "icon": "🎓",
        "points": 30,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 3
    },
    {
        "id": "word_master",
        "name": "Word Master",
        "description": "Humanize over 5,000 words in total",
        "category": "intermediate",
        "icon": "📚",
        "points": 40,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 5000
    },
    {
        "id": "power_user",
        "name": "Power User",
        "description": "Save 10 different texts",
        "category": "intermediate",
        "icon": "⚡",
        "points": 35,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 10
    },
    {
        "id": "variety",
        "name": "Versatile Writer",
        "description": "Use each humanization level at least 3 times",
        "category": "advanced",
        "icon": "🌈",
        "points": 50,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 15,
        "progress_detail": {
            "level_count": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        }
    },
    {
        "id": "consistency",
        "name": "Consistent Creator",
        "description": "Use the humanizer on 5 different days",
        "category": "advanced",
        "icon": "📆",
        "points": 45,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 5,
        "progress_detail": {
            "days_used": []
        }
    },
    {
        "id": "upload_text",
        "name": "File Master",
        "description": "Upload a text file for humanization",
        "category": "beginner",
        "icon": "📄",
        "points": 15,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 1
    },
    {
        "id": "essay_complete",
        "name": "Essay Completer",
        "description": "Humanize a text with more than 1,000 words",
        "category": "intermediate",
        "icon": "📰",
        "points": 35,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 1
    },
    {
        "id": "detector_buster",
        "name": "Detector Buster",
        "description": "Humanize 10 texts with Level 4 or higher",
        "category": "advanced",
        "icon": "🛡️",
        "points": 55,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 10
    },
    {
        "id": "text_search",
        "name": "Archivist",
        "description": "Use the search function to find saved texts",
        "category": "beginner",
        "icon": "🔎",
        "points": 20,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 1
    },
    {
        "id": "word_champion",
        "name": "Word Champion",
        "description": "Humanize over 25,000 words in total",
        "category": "expert",
        "icon": "🌟",
        "points": 100,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 25000
    },
    {
        "id": "transformation_master",
        "name": "Transformation Master",
        "description": "Complete 50 humanizations",
        "category": "expert",
        "icon": "👑",
        "points": 150,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 50
    },
    {
        "id": "night_owl",
        "name": "Night Owl",
        "description": "Humanize a text between midnight and 5 AM",
        "category": "secret",
        "icon": "🦉",
        "points": 25,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 1
    },
    {
        "id": "easter_egg",
        "name": "Easter Egg Hunter",
        "description": "Discover a hidden feature of the humanizer",
        "category": "secret",
        "icon": "🥚",
        "points": 30,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 1
    },
    {
        "id": "perfect_score",
        "name": "Perfect Score",
        "description": "Earn all other achievements",
        "category": "expert",
        "icon": "💯",
        "points": 200,
        "unlocked": False,
        "date_unlocked": None,
        "progress": 0,
        "progress_max": 17  # One less than total achievements (itself excluded)
    }
]


class AchievementSystem:
    """
    A class to manage user achievements for the Dx3n Text Humanizer.
    """
    
    def __init__(self, achievements_file: str = "user_achievements.json"):
        """Initialize the achievement system with default achievements."""
        self.achievements_file = achievements_file
        self.achievements = self._load_achievements()
        self.tracked_days = set()
        self._initialize_stats()
        
    def _initialize_stats(self):
        """Initialize achievement statistics."""
        self.stats = {
            "total_points": 0,
            "achievements_unlocked": 0,
            "level": "Beginner",
            "next_level_points": 100,
            "achievement_categories": {
                "beginner": {"total": 0, "unlocked": 0},
                "intermediate": {"total": 0, "unlocked": 0},
                "advanced": {"total": 0, "unlocked": 0},
                "expert": {"total": 0, "unlocked": 0},
                "secret": {"total": 0, "unlocked": 0}
            }
        }
        
        # Count total achievements in each category
        for achievement in self.achievements:
            category = achievement["category"]
            self.stats["achievement_categories"][category]["total"] += 1
            
            # Count unlocked achievements and total points
            if achievement["unlocked"]:
                self.stats["achievements_unlocked"] += 1
                self.stats["total_points"] += achievement["points"]
                self.stats["achievement_categories"][category]["unlocked"] += 1
        
        # Calculate user level based on points
        self._calculate_level()
                
    def _calculate_level(self):
        """Calculate user level based on points."""
        points = self.stats["total_points"]
        
        if points < 100:
            self.stats["level"] = "Novice Humanizer"
            self.stats["next_level_points"] = 100
        elif points < 250:
            self.stats["level"] = "Apprentice Humanizer"
            self.stats["next_level_points"] = 250
        elif points < 500:
            self.stats["level"] = "Skilled Humanizer"
            self.stats["next_level_points"] = 500
        elif points < 750:
            self.stats["level"] = "Expert Humanizer"
            self.stats["next_level_points"] = 750
        else:
            self.stats["level"] = "Master Humanizer"
            self.stats["next_level_points"] = None
    
    def _load_achievements(self) -> List[Dict]:
        """Load achievements from file or use defaults if file doesn't exist."""
        if os.path.exists(self.achievements_file):
            try:
                with open(self.achievements_file, 'r') as f:
                    achievements = json.load(f)
                return achievements
            except json.JSONDecodeError:
                # If file is corrupt, use defaults
                return DEFAULT_ACHIEVEMENTS.copy()
        else:
            # File doesn't exist, use defaults
            return DEFAULT_ACHIEVEMENTS.copy()
    
    def _save_achievements(self):
        """Save achievements to file."""
        with open(self.achievements_file, 'w') as f:
            json.dump(self.achievements, f, indent=2)
    
    def get_achievement(self, achievement_id: str) -> Optional[Dict]:
        """Get an achievement by ID."""
        for achievement in self.achievements:
            if achievement["id"] == achievement_id:
                return achievement
        return None
    
    def get_all_achievements(self) -> List[Dict]:
        """Get all achievements, including locked ones."""
        return self.achievements
    
    def get_unlocked_achievements(self) -> List[Dict]:
        """Get only unlocked achievements."""
        return [ach for ach in self.achievements if ach["unlocked"]]
    
    def get_achievements_by_category(self, category: str) -> List[Dict]:
        """Get achievements in a specific category."""
        return [ach for ach in self.achievements if ach["category"] == category]
    
    def get_locked_achievements(self) -> List[Dict]:
        """Get locked achievements."""
        return [ach for ach in self.achievements if not ach["unlocked"]]
    
    def get_achievement_progress(self, achievement_id: str) -> Dict:
        """Get progress on a specific achievement."""
        achievement = self.get_achievement(achievement_id)
        if not achievement:
            return {"error": "Achievement not found"}
        
        return {
            "id": achievement["id"],
            "name": achievement["name"],
            "progress": achievement["progress"],
            "progress_max": achievement["progress_max"],
            "percent": (achievement["progress"] / achievement["progress_max"]) * 100 if achievement["progress_max"] > 0 else 0,
            "unlocked": achievement["unlocked"]
        }
    
    def unlock_achievement(self, achievement_id: str) -> Dict:
        """Manually unlock an achievement."""
        achievement = self.get_achievement(achievement_id)
        if not achievement:
            return {"error": "Achievement not found"}
        
        if achievement["unlocked"]:
            return {"status": "already_unlocked", "achievement": achievement}
        
        # Set the achievement as unlocked
        achievement["unlocked"] = True
        achievement["date_unlocked"] = datetime.now().isoformat()
        achievement["progress"] = achievement["progress_max"]
        
        # Save changes
        self._save_achievements()
        self._initialize_stats()
        
        return {"status": "unlocked", "achievement": achievement}
    
    def update_achievement_progress(self, achievement_id: str, progress_increment: int = 1, 
                                    additional_data: Optional[Dict] = None) -> Dict:
        """Update progress on an achievement."""
        achievement = self.get_achievement(achievement_id)
        if not achievement:
            return {"error": "Achievement not found"}
        
        if achievement["unlocked"]:
            return {"status": "already_unlocked", "achievement": achievement}
        
        # Update progress
        old_progress = achievement["progress"]
        achievement["progress"] = min(achievement["progress"] + progress_increment, achievement["progress_max"])
        
        # Update additional tracking data if provided
        if additional_data and "progress_detail" in achievement:
            for key, value in additional_data.items():
                if key in achievement["progress_detail"]:
                    achievement["progress_detail"][key] = value
        
        # Check if achievement should be unlocked
        newly_unlocked = False
        if achievement["progress"] >= achievement["progress_max"] and not achievement["unlocked"]:
            achievement["unlocked"] = True
            achievement["date_unlocked"] = datetime.now().isoformat()
            newly_unlocked = True
        
        # Save changes
        self._save_achievements()
        self._initialize_stats()
        
        # Check if the "Perfect Score" achievement should be updated
        if achievement_id != "perfect_score":
            self._check_perfect_score()
        
        return {
            "status": "unlocked" if newly_unlocked else "progress_updated",
            "achievement": achievement,
            "old_progress": old_progress,
            "new_progress": achievement["progress"]
        }
    
    def _check_perfect_score(self):
        """Check if the 'Perfect Score' achievement should be updated."""
        perfect_score = self.get_achievement("perfect_score")
        if perfect_score and not perfect_score["unlocked"]:
            # Count unlocked achievements excluding "perfect_score"
            unlocked_count = sum(1 for a in self.achievements if a["unlocked"] and a["id"] != "perfect_score")
            
            # Update progress
            self.update_achievement_progress("perfect_score", unlocked_count - perfect_score["progress"])
    
    def track_humanization(self, text: str, humanize_level: int) -> List[Dict]:
        """
        Track a humanization event and update relevant achievements.
        Returns a list of newly unlocked achievements.
        """
        word_count = len(text.split())
        newly_unlocked = []
        
        # Track current day
        today = datetime.now().strftime("%Y-%m-%d")
        is_night_time = 0 <= datetime.now().hour < 5
        
        # Record level used
        level_str = str(humanize_level)
        
        # Each achievement that might be updated by a humanization
        achievements_to_check = [
            # First humanization
            {"id": "first_humanize", "increment": 1},
            
            # Count total humanizations
            {"id": "five_humanizations", "increment": 1},
            {"id": "transformation_master", "increment": 1},
            
            # Track words processed
            {"id": "word_master", "increment": word_count},
            {"id": "word_champion", "increment": word_count},
            
            # Check for large texts
            {"id": "essay_complete", "increment": 1 if word_count >= 1000 else 0},
            
            # Track level usage
            {"id": "detector_buster", "increment": 1 if humanize_level >= 4 else 0},
            {"id": "scholarship", "increment": 1 if humanize_level == 5 else 0},
        ]
        
        # Try all levels achievement
        try_all_levels = self.get_achievement("try_all_levels")
        if try_all_levels and not try_all_levels["unlocked"]:
            levels_used = try_all_levels["progress_detail"]["levels_used"]
            if humanize_level not in levels_used:
                levels_used.append(humanize_level)
                achievements_to_check.append({
                    "id": "try_all_levels", 
                    "increment": 1,
                    "additional_data": {"levels_used": levels_used}
                })
        
        # Versatile writer achievement
        variety = self.get_achievement("variety")
        if variety and not variety["unlocked"]:
            level_count = variety["progress_detail"]["level_count"]
            level_count[level_str] = min(level_count.get(level_str, 0) + 1, 3)
            total_progress = sum(min(count, 3) for count in level_count.values())
            
            achievements_to_check.append({
                "id": "variety", 
                "increment": total_progress - variety["progress"],
                "additional_data": {"level_count": level_count}
            })
        
        # Consistency achievement
        consistency = self.get_achievement("consistency")
        if consistency and not consistency["unlocked"]:
            days_used = consistency["progress_detail"]["days_used"]
            if today not in days_used:
                days_used.append(today)
                achievements_to_check.append({
                    "id": "consistency", 
                    "increment": 1,
                    "additional_data": {"days_used": days_used}
                })
        
        # Night owl achievement
        if is_night_time:
            achievements_to_check.append({"id": "night_owl", "increment": 1})
            
        # Update each achievement's progress
        for check in achievements_to_check:
            achievement_id = check["id"]
            increment = check["increment"]
            additional_data = check.get("additional_data")
            
            if increment <= 0:
                continue
                
            result = self.update_achievement_progress(
                achievement_id, 
                increment,
                additional_data
            )
            
            if result.get("status") == "unlocked":
                newly_unlocked.append(result["achievement"])
        
        return newly_unlocked
    
    def track_text_save(self) -> List[Dict]:
        """Track when a user saves text and update relevant achievements."""
        newly_unlocked = []
        
        # Track first save
        save_result = self.update_achievement_progress("save_text", 1)
        if save_result.get("status") == "unlocked":
            newly_unlocked.append(save_result["achievement"])
        
        # Track multiple saves
        power_result = self.update_achievement_progress("power_user", 1)
        if power_result.get("status") == "unlocked":
            newly_unlocked.append(power_result["achievement"])
            
        return newly_unlocked
    
    def track_text_search(self) -> List[Dict]:
        """Track when a user searches for saved text."""
        newly_unlocked = []
        
        search_result = self.update_achievement_progress("text_search", 1)
        if search_result.get("status") == "unlocked":
            newly_unlocked.append(search_result["achievement"])
            
        return newly_unlocked
    
    def track_file_upload(self) -> List[Dict]:
        """Track when a user uploads a file for humanization."""
        newly_unlocked = []
        
        upload_result = self.update_achievement_progress("upload_text", 1)
        if upload_result.get("status") == "unlocked":
            newly_unlocked.append(upload_result["achievement"])
            
        return newly_unlocked
    
    def get_stats(self) -> Dict:
        """Get achievement system statistics."""
        return self.stats
    
    def get_level_progress(self) -> Dict:
        """Get user's current level and progress to next level."""
        if self.stats["next_level_points"] is None:
            # User is at max level
            return {
                "current_level": self.stats["level"],
                "progress_percent": 100,
                "next_level": None,
                "points_needed": 0
            }
        
        current_points = self.stats["total_points"]
        next_level_points = self.stats["next_level_points"]
        
        # Calculate previous level threshold
        if self.stats["level"] == "Novice Humanizer":
            prev_threshold = 0
        elif self.stats["level"] == "Apprentice Humanizer":
            prev_threshold = 100
        elif self.stats["level"] == "Skilled Humanizer":
            prev_threshold = 250
        elif self.stats["level"] == "Expert Humanizer":
            prev_threshold = 500
        else:
            prev_threshold = 750
        
        # Calculate progress percentage
        level_range = next_level_points - prev_threshold
        progress_in_level = current_points - prev_threshold
        progress_percent = (progress_in_level / level_range) * 100
        
        return {
            "current_level": self.stats["level"],
            "progress_percent": progress_percent,
            "next_level": self._get_next_level_name(),
            "points_needed": next_level_points - current_points
        }
    
    def _get_next_level_name(self) -> Optional[str]:
        """Get the name of the next level based on current level."""
        current = self.stats["level"]
        
        if current == "Novice Humanizer":
            return "Apprentice Humanizer"
        elif current == "Apprentice Humanizer":
            return "Skilled Humanizer"
        elif current == "Skilled Humanizer":
            return "Expert Humanizer"
        elif current == "Expert Humanizer":
            return "Master Humanizer"
        else:
            return None
    
    def track_easter_egg(self) -> Dict:
        """Track when a user discovers an easter egg."""
        return self.update_achievement_progress("easter_egg", 1)
    
    def reset_achievements(self):
        """Reset all achievements to default state."""
        self.achievements = DEFAULT_ACHIEVEMENTS.copy()
        self._save_achievements()
        self._initialize_stats()
        return {"status": "reset_complete"}


# For testing
if __name__ == "__main__":
    # Create an instance of the achievement system
    achievement_system = AchievementSystem()
    
    # Simulate some user actions
    print("Simulating user actions...")
    
    # First humanization
    newly_unlocked = achievement_system.track_humanization("This is a sample text for testing.", 3)
    print(f"Newly unlocked: {[a['name'] for a in newly_unlocked]}")
    
    # Save a text
    newly_unlocked = achievement_system.track_text_save()
    print(f"Newly unlocked: {[a['name'] for a in newly_unlocked]}")
    
    # Get user stats
    stats = achievement_system.get_stats()
    print(f"User level: {stats['level']}")
    print(f"Total points: {stats['total_points']}")
    print(f"Achievements unlocked: {stats['achievements_unlocked']}")