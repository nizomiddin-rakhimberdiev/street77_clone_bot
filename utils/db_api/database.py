import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('street77.db')
        self.cursor = self.conn.cursor()


    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              user_id INTEGER NOT NULL UNIQUE,
                              language VARCHAR(2) NOT NULL,
                              city VARCHAR(20) NOT NULL,
                              user_role VARCHAR(255) NOT NULL DEFAULT 'customer')
                            ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name VARCHAR(255) NOT NULL UNIQUE)
                            ''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS filials
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name VARCHAR(255) NOT NULL,
                              address VARCHAR(255) NOT NULL,
                              latitude REAL NOT NULL,
                              longitude REAL NOT NULL)
                            ''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name VARCHAR(255) NOT NULL UNIQUE,
                              price REAL NOT NULL,
                              description TEXT,
                              image Text,
                              category_id INTEGER NOT NULL,
                              FOREIGN KEY (category_id) REFERENCES categories(id))
                            ''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              user_id INTEGER NOT NULL,
                              filial_id INTEGER NOT NULL,
                              product_id INTEGER NOT NULL,
                              order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                              status VARCHAR(255) NOT NULL DEFAULT 'pending',
                              order_type VARCHAR(255) NOT NULL,
                              order_address VARCHAR(255),                              
                              FOREIGN KEY (user_id) REFERENCES users(id),
                              FOREIGN KEY (filial_id) REFERENCES filials(id)
                              FOREIGN KEY (product_id) REFERENCES products(id)
                            )
                            ''')
        
        self.conn.commit()


    def add_filial(self, name, address, latitude, longitude):
        self.cursor.execute("INSERT INTO filials (name, address, latitude, longitude) VALUES (?,?,?,?)", (name, address, latitude, longitude))
        self.conn.commit()


    def get_filials(self):
        self.cursor.execute("SELECT * FROM filials")
        return self.cursor.fetchall()
    


    def add_category(self, name):
        self.cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        self.conn.commit()

    def get_categories(self):
        self.cursor.execute("SELECT * FROM categories")
        return self.cursor.fetchall()
    
    def get_products(self, category_id):
        self.cursor.execute("SELECT * FROM products WHERE category_id =?", (category_id,))
        return self.cursor.fetchall()
    

    def get_product(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE id =?", (product_id,))
        return self.cursor.fetchall()[0]

    def check_product(self, name):
        self.cursor.execute("SELECT name FROM products WHERE name =?", (name,))
        print(self.cursor.fetchone())
        return self.cursor.fetchone()
    
    def add_product(self, name, price, description, image, category_id):
        self.cursor.execute("INSERT INTO products (name, price, description, image, category_id) VALUES (?,?,?,?,?)", (name, price, description, image, category_id))
        self.conn.commit()
    
 

    def add_order(self, user_id, filial_id, product_id, order_type, order_address):
        self.cursor.execute('INSERT INTO (user_id, filial_id, product_id, order_type, order_address) VALUES (?, ?, ?, ?, ?)', (user_id, filial_id, product_id, order_type, order_address))


    def get_orders(self):
        self.cursor.execute("SELECT * FROM orders")
        return self.cursor.fetchall()

    def add_user(self, user_id, language, city):
        self.cursor.execute("INSERT INTO users (user_id, language, city) VALUES (?,?,?)", (user_id, language, city))
        self.conn.commit()

    def get_users_id(self):
        self.cursor.execute("SELECT user_id FROM users")
        return self.cursor.fetchall()
    

    def change_user_role(self, user_id):
        self.cursor.execute("UPDATE users SET user_role='admin' WHERE user_id=?", (user_id,))
        self.conn.commit()

    def get_filials(self):
        self.cursor.execute("SELECT name FROM filials")
        return self.cursor.fetchall()
    
    def add_filial(self, name, address, latitude, longitude):
        self.cursor.execute("INSERT INTO filials (name, address, latitude, longitude) VALUES (?,?,?,?)", (name, address, latitude, longitude))
        self.conn.commit()

    
    
    def create_products(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name VARCHAR(255) NOT NULL,
                              price REAL NOT NULL,
                              category VARCHAR(255) NOT NULL)
                            ''')
        self.conn.commit()

    def drop_table(self):
        self.cursor.execute('''Drop table products''')
        self.conn.commit()