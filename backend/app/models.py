from datetime import datetime

class UserPreferences:
    def __init__(self, db):
        self.collection = db.user_preferences

    def create_user_preferences(self, session_id, preferences):
        """Create new user preferences with debugging"""
        print(f"Received preferences for creation: {preferences}")  # Debug input
        
        user_data = {
            'session_id': session_id,
            'grades': preferences.get('grades', []),
            'subjects': preferences.get('subjects', []),
            'teacher_tech': preferences.get('teacher_tech', []),
            'student_devices': preferences.get('student_devices', []),
            'goals': preferences.get('goals', []),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        print(f"Prepared user_data for MongoDB: {user_data}")  # Debug prepared data
        
        result = self.collection.insert_one(user_data)
        success = result.acknowledged
        print(f"MongoDB insert success: {success}")  # Debug result
        
        return str(result.inserted_id)

    def update_user_preferences(self, session_id, preferences):
        """Update existing user preferences with debugging"""
        print(f"Updating preferences for session {session_id}")  # Debug
        print(f"Update data received: {preferences}")  # Debug
        
        # Add updated timestamp
        preferences['updated_at'] = datetime.utcnow()
        
        result = self.collection.update_one(
            {'session_id': session_id},
            {'$set': preferences}
        )
        
        success = result.modified_count > 0
        print(f"MongoDB update success: {success}")  # Debug
        
        return success

    def get_user_preferences(self, session_id):
        """Retrieve user preferences by session_id with debugging"""
        print(f"Fetching preferences for session: {session_id}")  # Debug
        
        result = self.collection.find_one({'session_id': session_id})
        print(f"Found preferences: {result}")  # Debug
        
        return result