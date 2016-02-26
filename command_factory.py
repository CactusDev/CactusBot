
import sqlite3 as sql


conn = sql.connect('data/bot.db')
c = conn.cursor()


class Command():

    def get_response(self, cmd):
        return c.execute('SELECT response FROM commands WHERE command={command};', command=cmd)

    def set_response(self, cmd, resp):
        access = self.get_access(cmd)

        self.remove_command(cmd)
        self.add_command(cmd, resp, access)

    def add_command(self, cmd, response, access):
        c.execute("INSERT INTO commands VALUES ({cmd}, {resp}, {access});".format(cmd=cmd, resp=response, access=access))

        conn.commit()
        conn.close()

    def remove_command(self, cmd):
        c.execute("DELETE FROM commands WHERE command={cmd};".format(cmd=cmd))

        conn.commit()
        conn.close()

    def change_command(self, cmd, resp, access):
        c.execute("DELETE FROM command WHERE command={cmd};".format(cmd=cmd))
        c.execute("INSERT INTO command VALUES ({cmd}, {resp}, {access});".format(cmd=cmd, resp=resp, access=access))

        conn.commit()
        conn.close()

    def get_access(self, cmd):
        c.execute("SELECT access FROM commands WHERE command={cmd};".format(cmd=cmd))
