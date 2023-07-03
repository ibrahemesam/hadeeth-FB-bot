import sqlite3, os
from threading import Lock

DATABASE_PATH = 'data/db.db'
DEFAULT_CONFIG = {}
STARTUP_CONFIG = {}
SET_TRUE_FALSE_NONE = {'True', 'False', 'None'}

class db:
    def __init__(self) -> None:
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        self._db = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self._db.row_factory = sqlite3.Row
        self._db.execute("create table if not exists config(name text, value object)")
        # write default config items
        for i in DEFAULT_CONFIG:
            if self.configRead(i) is None:
                self.configWrite(i, DEFAULT_CONFIG[i])
        # write startup config items
        for i in STARTUP_CONFIG:
            self.configWrite(i, STARTUP_CONFIG[i])

    def __del__(self):
        self._db.close()

    def config_write(self, name, value):
        if name in [cr[0] for cr in self._db.execute('select name from config')]:
            self._db.execute('UPDATE config SET value = ? WHERE name = ?;', (value, name))
        else:
            self._db.execute(f'insert into config(name, value) values(?, ?)', (name, value))
        self._db.commit();

    def config_read(self, name):
        try:
            _ = tuple(self._db.execute('select value from config where name=?', (name,)))[0]['value']
            if _ in SET_TRUE_FALSE_NONE: return eval(_)
            else: return _
        except: return None

