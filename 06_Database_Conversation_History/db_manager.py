import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self, db_path='chat_history.db'):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    identifier TEXT,
                    timestamp TEXT,
                    full_chat TEXT
                )
            ''')
            conn.commit()

    def add_history(self, first_message, full_chat):
        identifier = f"{first_message[:20]} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO history (identifier, timestamp, full_chat)
                VALUES (?, ?, ?)
            ''', (identifier, timestamp, full_chat))
            conn.commit()

    def get_all_history(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, identifier, timestamp FROM history ORDER BY timestamp DESC')
            return cursor.fetchall()

    def get_history_by_id(self, record_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT full_chat FROM history WHERE id = ?', (record_id,))
            return cursor.fetchone()[0]
