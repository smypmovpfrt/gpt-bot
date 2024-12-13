import sqlite3
db_path = 'data/gpt_free_db.db'


class Bot_db():
    def __init__(self):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def get_users_count(self):
        self.cursor.execute("SELECT `userchatid` FROM `users`")
        result = self.cursor.fetchall()
        return str(len(result))

    def has_unlimited_access(self, user_id):
        if self.user_exists(user_id):
            self.cursor.execute("SELECT unlimit FROM users WHERE user_id = ?", (user_id,))
            result = self.cursor.fetchone()
            return result[0] == 1 if result and result[0] is not None else False
        else:
            print(f"User with ID {user_id} does not exist.")
            return False    
        
    def set_unlimited_access(self, user_id, access):
        if self.user_exists(user_id):
            self.cursor.execute("UPDATE users SET unlimit = ? WHERE user_id = ?", (access, user_id))
            self.conn.commit()
        else:
            print(f"User with ID {user_id} does not exist.")   

    
    def get_user_balance(self, user_id):
        self.cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
        
    def update_user_balance(self, user_id, new_balance):
        self.cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
        return self.conn.commit()    

    def not_active(self, user_id, active = 0):
        if self.user_exists(user_id):
            self.cursor.execute("UPDATE users SET is_active = ? WHERE user_id = ?", (active, user_id))
            self.conn.commit()
        else:
            print(f"User with ID {user_id} does not exist.")
    
    def is_active(self, user_id):
        self.cursor.execute("SELECT is_active FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def close(self):
        self.conn.close()    