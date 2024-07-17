import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('street77.db')
        self.cursor = self.conn.cursor()


    def create_users_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              user_id INTEGER NOT NULL UNIQUE,
                              language VARCHAR(2) NOT NULL,
                              city VARCHAR(20) NOT NULL,
                              user_role VARCHAR(255) NOT NULL DEFAULT 'customer')
                            ''')
        self.conn.commit()


    def add_user(self, user_id, language, city):
        self.cursor.execute("INSERT INTO users (user_id, language, city) VALUES (?,?,?)", (user_id, language, city))
        self.conn.commit()

    def get_users_id(self):
        self.cursor.execute("SELECT user_id FROM users")
        return self.cursor.fetchall()