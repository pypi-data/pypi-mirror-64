import sqlite3
from typing import *
from filterlib import Filter


class Setting:
    columns = ["text_id TEXT PRIMARY KEY",
               "readable_name TEXT",
               "description TEXT",
               "value"]

    def __init__(self,
                 database_name: str = ":memory:"):
        self.database_name = database_name
        self.database = sqlite3.connect(database_name)
        self.switch_database(database_name)

    def __getitem__(self,
                    item) -> str:
        cmd = f"SELECT value FROM user_settings WHERE text_id='{item}'".replace("''", "")
        result = [x for x in self.database.execute(cmd)][0][0]
        return result

    def __setitem__(self,
                    key,
                    value) -> None:
        self.database.execute(f"UPDATE user_settings SET value={value} WHERE text_id='{key}'")
        self.database.commit()

    def __contains__(self,
                     item) -> bool:
        return item in [x for x in self.database.execute("SELECT text_id FROM user_settings")]

    def add_setting(self,
                    text_id: str,
                    readable_name: str,
                    description: str,
                    value):
        cols = [x.split()[0] for x in self.columns]
        values = [text_id,
                  readable_name,
                  description,
                  value]
        c = ', '.join(cols)
        v = ', '.join(["'" + str(v).replace("'", "\'") + "'" for v in values])
        cmd = f"INSERT INTO user_settings({c}) VALUES({v})".replace("''", "")
        self.database.execute(cmd)
        self.database.commit()

    def update_setting(self,
                       text_id: str,
                       readable_name: Optional[str] = None,
                       description: Optional[str] = None,
                       value: Optional[Any] = None):
        f = Filter(text_id__eq__=text_id)
        command = "UPDATE user_settings SET"  # …
        if readable_name:
            cmd = f"{command} readable_name='{readable_name.strip()}' WHERE {f}"
            self.database.execute(cmd)
        if description:
            cmd = f"{command} description='{description.strip()}' WHERE {f}"
            self.database.execute(cmd)
        if value:
            cmd = f"{command} value='{str(value).strip().replace(' ', '_')}' WHERE {f}"
            self.database.execute(cmd)
        self.database.commit()

    def delete_setting(self,
                       text_id):
        f = Filter(text_id__eq__=text_id)
        cmd = f"DELETE FROM user_settings WHERE {f}"
        self.database.execute(cmd)
        self.database.commit()

    def switch_database(self,
                        new_db_name: str,
                        commit_to_old: bool = True) -> None:
        self.database_name = new_db_name
        if commit_to_old:
            try:
                self.database.commit()
            except AttributeError:
                pass
        self.database.close()
        self.database = sqlite3.connect(self.database_name)
        cols = [str(x) for x in self.columns]
        cmd = f"CREATE TABLE IF NOT EXISTS user_settings({', '.join(cols)})"
        self.database.execute(cmd)
        self.database.commit()

    def get_setting(self,
                    text_id: str,
                    detail: Optional[str] = "*") -> List[List]:
        cmd = f"SELECT {detail} FROM user_settings WHERE text_id='{text_id}'"
        return [x for x in self.database.execute(cmd)][0]

    def __iter__(self, f: Filter = None) -> List[List]:
        for a in [e for e in self.database.execute("SELECT * FROM user_settings" + (" WHERE " + str(f) if f else ""))]:
            yield a


if __name__ == "__main__":
    pass
