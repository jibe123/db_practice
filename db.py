from models import TGUser, Note

if not TGUser.table_exists():
    TGUser.create_table()

if not Note.table_exists():
    Note.create_table()