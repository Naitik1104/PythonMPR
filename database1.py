import mysql.connector
from mysql.connector import Error
from datetime import datetime

class Database:
    def __init__(self, host, user, password, database, port=3306):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
        except Error as e:
            print(f"Error: {e}")
            self.connection = None  # Ensure connection is None if there's an error

    def check_mobile_exists(self, aadhar):
        if self.connection is None:
            return False
        
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM users WHERE aadhar = %s", (aadhar,))
            count = cursor.fetchone()[0]
            return count > 0
        finally:
            cursor.close()

    def insert_user(self, name, password, aadhar, age, gender):
        if self.connection is None:
            print("No connection to the database. Cannot insert user.")
            return False
        
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (name, password, aadhar, age, gender)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, password, aadhar, age, gender))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error inserting user: {e}")
            return False
        finally:
            cursor.close()

    def insert_interest(self, user_id, interest):
        if self.connection is None:
            print("No connection to the database. Cannot insert interest.")
            return
        
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO profiles (user_id, Interests)
            VALUES (%s, %s)
        """, (user_id, interest))
        self.connection.commit()
        cursor.close()

    def get_user(self, username):
        if self.connection is None:
            print("No connection to the database. Cannot retrieve user.")
            return None
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE name = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        return user

    def update_user_profile(self, name, age, gender, location):
        if self.connection is None:
            print("No connection to the database. Cannot update profile.")
            return
        
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                UPDATE users 
                SET age = %s, gender = %s, location = %s
                WHERE name = %s
            """, (age, gender, location, name))
            self.connection.commit()
        finally:
            cursor.close()

    def update_user_interests(self, name, interests):
        if self.connection is None:
            print("No connection to the database. Cannot update interests.")
            return
        
        cursor = self.connection.cursor()
        try:
            # First get the user_id from users table
            cursor.execute("SELECT id FROM users WHERE name = %s", (name,))
            user = cursor.fetchone()
            if not user:
                print("User not found")
                return
            
            user_id = user[0]
            
            # Check if profile exists
            cursor.execute("SELECT id FROM profiles WHERE user_id = %s", (user_id,))
            profile = cursor.fetchone()
            
            if profile:
                cursor.execute("""
                    UPDATE profiles 
                    SET Interests = %s
                    WHERE user_id = %s
                """, (interests, user_id))
            else:
                cursor.execute("""
                    INSERT INTO profiles (user_id, Interests)
                    VALUES (%s, %s)
                """, (user_id, interests))
            
            self.connection.commit()
        finally:
            cursor.close()

    def update_profile_picture(self, name, profile_picture_data):
        if self.connection is None:
            print("No connection to the database. Cannot update profile picture.")
            return
        
        cursor = self.connection.cursor()
        try:
            # First get the user_id from users table
            cursor.execute("SELECT id FROM users WHERE name = %s", (name,))
            user = cursor.fetchone()
            if not user:
                print("User not found")
                return
            
            user_id = user[0]
            
            # Check if profile exists
            cursor.execute("SELECT id FROM profiles WHERE user_id = %s", (user_id,))
            profile = cursor.fetchone()
            
            if profile:
                cursor.execute("""
                    UPDATE profiles 
                    SET profile_picture = %s
                    WHERE user_id = %s
                """, (profile_picture_data, user_id))
            else:
                cursor.execute("""
                    INSERT INTO profiles (user_id, profile_picture)
                    VALUES (%s, %s)
                """, (user_id, profile_picture_data))
            
            self.connection.commit()
        finally:
            cursor.close()

    def get_profile_picture(self, name):
        if self.connection is None:
            print("No connection to the database. Cannot get profile picture.")
            return None
        
        cursor = self.connection.cursor()
        try:
            # Get user_id
            cursor.execute("SELECT id FROM users WHERE name = %s", (name,))
            user = cursor.fetchone()
            if not user:
                print("User not found")
                return None
            
            user_id = user[0]
            
            # Get profile picture
            cursor.execute("SELECT profile_picture FROM profiles WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            if result and result[0]:
                return result[0]  # Return binary data directly
            return None
        finally:
            cursor.close()

    def update_user_bio(self, name, bio):
        if self.connection is None:
            print("No connection to the database. Cannot update bio.")
            return
        
        cursor = self.connection.cursor()
        try:
            # First get the user_id from users table
            cursor.execute("SELECT id FROM users WHERE name = %s", (name,))
            user = cursor.fetchone()
            if not user:
                print("User not found")
                return
            
            user_id = user[0]
            
            # Check if profile exists
            cursor.execute("SELECT id FROM profiles WHERE user_id = %s", (user_id,))
            profile = cursor.fetchone()
            
            if profile:
                cursor.execute("""
                    UPDATE profiles 
                    SET Bio = %s
                    WHERE user_id = %s
                """, (bio, user_id))
            else:
                cursor.execute("""
                    INSERT INTO profiles (user_id, Bio)
                    VALUES (%s, %s)
                """, (user_id, bio))
            
            self.connection.commit()
        finally:
            cursor.close()

    def save_user_photos(self, name, photo_data_list):
        if self.connection is None:
            print("No connection to the database. Cannot save photos.")
            return
        
        cursor = self.connection.cursor()
        try:
            # Get user_id
            cursor.execute("SELECT id FROM users WHERE name = %s", (name,))
            user = cursor.fetchone()
            if not user:
                print("User not found")
                return
            
            user_id = user[0]
            
            # Delete existing photos for this user
            cursor.execute("DELETE FROM photos WHERE user_id = %s", (user_id,))
            
            # Insert new photos with current timestamp
            current_time = datetime.now()
            
            # Insert new photos
            for photo_data in photo_data_list:
                if photo_data:  # Only insert if photo data exists
                    cursor.execute("""
                        INSERT INTO photos (user_id, photo, upload_date)
                        VALUES (%s, %s, %s)
                    """, (user_id, photo_data, current_time))
            
            self.connection.commit()
        finally:
            cursor.close()

    def get_user_photos(self, username):
        if self.connection is None:
            print("No connection to the database.")
            return []

        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id FROM users WHERE name = %s", (username,))
            user_id = cursor.fetchone()
            
            if user_id is None:
                print("User not found.")
                return []

            user_id = user_id[0]  # Extract the user_id from the tuple

            # Fetch photos for the user
            cursor.execute("SELECT photo FROM photos WHERE user_id = %s", (user_id,))
            photos = [row[0] for row in cursor.fetchall()]  # Fetch all photos for the user
            return photos
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()