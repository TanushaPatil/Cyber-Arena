import sqlite3

DATABASE = "database/ctf.db"

conn = sqlite3.connect(DATABASE)

conn.execute("""
    UPDATE challenges
    SET flag = ?
    WHERE title = ?
""", (
    "TECH{reverse_the_blackbox}",
    "What Does It Do?"
))

conn.commit()

print("BLACKBOX flag updated successfully!")

conn.close()