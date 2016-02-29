
import sqlite3 as sql


class Chat():

    def contains_banned_word(self, message, is_mod):
        # Open the database
        conn = sql.connect("data/bot.db")
        cur = conn.cursor()

        # Get all the banned words in the db
        cur.execute('''SELECT * FROM bannedWords''')
        banned = cur.getchall()

        # Loop through banned words
        for word in banned:
            if word in message:
                if is_mod is True:
                    return False
                else:
                    return True
            else:
                return False
