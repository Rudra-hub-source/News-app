import sqlite3
import os

def migrate_database():
    db_path = 'instance/news.db'
    
    if not os.path.exists(db_path):
        print("Database doesn't exist yet. It will be created with the new schema.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if view_count column exists in article table
    cursor.execute("PRAGMA table_info(article)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'view_count' not in columns:
        print("Adding view_count column to article table...")
        cursor.execute("ALTER TABLE article ADD COLUMN view_count INTEGER DEFAULT 0")
        conn.commit()
        print("view_count column added successfully!")
    else:
        print("view_count column already exists.")
    
    # Check if media table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='media'")
    if not cursor.fetchone():
        print("Creating media table...")
        cursor.execute('''
            CREATE TABLE media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename VARCHAR(255) NOT NULL,
                original_filename VARCHAR(255) NOT NULL,
                file_path VARCHAR(500) NOT NULL,
                file_size INTEGER,
                mime_type VARCHAR(100),
                alt_text VARCHAR(255),
                description TEXT,
                article_id INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (article_id) REFERENCES article (id)
            )
        ''')
        conn.commit()
        print("Media table created successfully!")
    else:
        print("Media table already exists.")
        # Check if article_id column exists
        cursor.execute("PRAGMA table_info(media)")
        media_columns = [column[1] for column in cursor.fetchall()]
        if 'article_id' not in media_columns:
            print("Adding article_id column to media table...")
            cursor.execute("ALTER TABLE media ADD COLUMN article_id INTEGER")
            conn.commit()
            print("article_id column added successfully!")
    
    conn.close()
    print("Migration completed successfully!")

if __name__ == '__main__':
    migrate_database()