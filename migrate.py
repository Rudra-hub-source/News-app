import sqlite3
import os

def migrate_database():
    db_path = 'instance/news.db'
    
    if not os.path.exists(db_path):
        print("Database doesn't exist yet. It will be created with the new schema.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if view_count column exists
    cursor.execute("PRAGMA table_info(article)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'view_count' not in columns:
        print("Adding view_count column to article table...")
        cursor.execute("ALTER TABLE article ADD COLUMN view_count INTEGER DEFAULT 0")
        conn.commit()
        print("Migration completed successfully!")
    else:
        print("view_count column already exists.")
    
    conn.close()

if __name__ == '__main__':
    migrate_database()