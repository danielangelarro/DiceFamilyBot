from enum import IntEnum
from typing import Optional, List
import sqlite3


class DBManager:
    def __init__(self, db_path: str) -> None:
        self.db = sqlite3.connect(
            db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.execute(
            '''CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY,
            user TEXT,
            money MONEY,
            name TEXT)''')
        self.execute(
            '''CREATE TABLE IF NOT EXISTS transactions
            (id INTEGER PRIMARY KEY,
            numbers TEXT,
            money FLOAT,
            game TEXT,
            autorized BOOLEAN,
            time TIMESTAMP,
            user INTEGER  REFERENCES users(id))''')

    def execute(self, statement: str, args=()) -> sqlite3.Cursor:
        return self.db.execute(statement, args)

    def commit(self, statement: str, args=()) -> sqlite3.Cursor:
        with self.db:
            return self.db.execute(statement, args)
    
    def close(self) -> None:
        self.db.close()

    # ==== users =====

    def add_user(self, gid: int, user: str, money: float, name: str) -> None:
        self.commit('INSERT INTO users VALUES (?,?,?,?)',
                    (gid, user, money, name))
    
    def exist_user(self, gid: int) -> bool:
        user = self.get_user_by_id(gid)

        return user is not None

    def set_user(self, money: float, gid: int) -> None:
        self.commit('SET money=? FROM users WHERE id=?', (money, gid))

    def remove_user(self, gid: int) -> None:
        self.commit('DELETE FROM users WHERE id=?', (gid,))

    def get_user_by_id(self, id: int) -> Optional[sqlite3.Row]:
        return self.execute(
            'SELECT * FROM users WHERE id=?', (id,)).fetchone()
    
    def get_user_by_name(self, name: str) -> Optional[sqlite3.Row]:
        return self.execute(
            'SELECT * FROM users WHERE name=?', (name,)).fetchone()

    def get_users(self) -> List[sqlite3.Row]:
        return self.execute(
            'SELECT * FROM users').fetchall()

    
    # ==== transaction =====

    def add_transaction(self, gid: int, numbers: str, money: float, game: str, time, user: int) -> None:
        self.commit('INSERT INTO transactions VALUES (?,?,?,?,?,?,?)', (gid, numbers, money, game, False, time, user))
    
    def remove_transaction(self, gid: int) -> None:
        self.commit('DELETE FROM transactions WHERE id=?', (gid,))
        
    def remove_all_transaction(self) -> None:
        self.commit('DELETE FROM transactions')

    def set_transaction(self, gid: int) -> None:
        self.commit('UPDATE transactions SET autorized=? WHERE id=?', (True, gid))

    def get_transaction_by_id(self, id: str) -> Optional[sqlite3.Row]:
        return self.execute(
            'SELECT * FROM transactions WHERE id=?', (id,)).fetchone()

    def get_transactions(self, user: int, game: str) -> Optional[sqlite3.Row]:
        return self.execute(
            'SELECT * FROM transactions WHERE user=? AND game=?', (user, game)).fetchone()

    def get_transactions_by_user(self, user: int) -> List[sqlite3.Row]:
        return self.execute(
            'SELECT * FROM transactions WHERE user=?', (user,)).fetchall()

    def get_transactions(self) -> List[sqlite3.Row]:
        return self.execute(
            'SELECT * FROM transactions').fetchall()
