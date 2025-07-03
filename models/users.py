import sqlite3


class User:
    def __init__(self, name, mail, password, isadm="client"):
        self.name = name
        self.mail = mail
        self.password = password
        self.isadm = isadm


class UserDAO:
    def __init__(
        self,
        db_path="database/system.db",
    ):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mail TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            isadm TEXT NOT NULL CHECK(isadm IN('adm', 'client'))
    )
    """
        )
        self.conn.commit()

    def register(self, user):
        try:
            self.cursor.execute(
                "INSERT INTO users (name, mail, password, isadm) VALUES (?, ?, ?, ?)",
                (user.name, user.mail, user.password, user.isadm),
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("EMAIL JA CADASTRADO.")

    def authenticate(self, mail, password):
        self.cursor.execute(
            "SELECT id, name, mail, isadm FROM users WHERE mail = ? AND password = ?",
            (mail, password),
        )
        return self.cursor.fetchone()
