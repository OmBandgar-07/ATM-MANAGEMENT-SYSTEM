import sqlite3


db = sqlite3.connect("atm.db")
cur = db.cursor()


cur.execute("CREATE TABLE users (account TEXT, pin TEXT, balance INTEGER)")
cur.execute("INSERT INTO users VALUES ('1001','1233',10000)")


db.commit()
db.close()