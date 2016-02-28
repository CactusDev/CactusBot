
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

    def parse_event(self, result):
        if 'event' in result:
            event = result['event']

            if 'username' in result['data']['username']:
                pass
            elif 'user_name' in result['data']['username']:
                pass
            elif event == "UserJoin":
                print("SOMEONE IS HERE LOLHI")
            elif event == "UserLeave":
                print("Someone went bye-bye")
            elif event == "ChatMessage":
                print("message!")
