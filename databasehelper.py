from errors.database_errors import *

class DatabaseHelper:
    def __init__(self, db):
        self.db = db

    ######################################################## COMMON ################################################
    async def check_presence(self, id):
        check = await self.db.fetch("SELECT id FROM userinfo WHERE id = $1", id)
        if check:
            return

        else:
            await self.db.execute("INSERT INTO userinfo (id, status, rank, kakechips, owochips) VALUES ($1, $2, $3, $4, $5)", id, "", "Student", 100, 0)

    async def delete_from_database(self, id):
        await self.db.execute("DELETE FROM userinfo WHERE id = $1", id)
    
    async def get_info(self, id):
        info = await self.db.fetch("SELECT * FROM userinfo WHERE id = $1",  id)
        return info[0]["status"], info[0]["rank"], info[0]["kakechips"], info[0]["owochips"]

    async def get_complete_balance(self, id):
        bal = await self.db.fetch("SELECT kakechips, owochips FROM userinfo WHERE id = $1", id)
        return bal[0]["kakechips"], bal[0]["owochips"]
    
    async def get_balance(self, id, currency):
        bal = await self.db.fetch(f"SELECT {currency} FROM userinfo WHERE id = $1", id)
        return bal[0][currency]
        
    async def update_balance(self, id, new_bal, currency):
        await self.db.execute(f"UPDATE userinfo SET {currency} = $1 WHERE id = $2", new_bal, id)
    
    async def update_status(self, id, status):
        await self.db.execute("UPDATE userinfo SET status = $1 WHERE id = $2", status, id)

    # Owner only
    async def update_rank(self, id, rank):
        rank = rank.title()
        await self.db.execute("UPDATE userinfo SET rank = $1 WHERE id = $2", rank, id)
    
    async def get_leaderboard(self):
        lb = await self.db.fetch("SELECT * FROM userinfo order by kakechips desc limit 10")
        return lb
##################################################################################################################

    async def add_balance(self, id, bal_to_add, currency):
        old_bal = await self.get_balance(id, currency)
        new_bal = old_bal + bal_to_add
        await self.update_balance(id, new_bal, currency)

    async def subtract_balance(self, id, bal_to_subtract, currency):
        old_bal = await self.get_balance(id, currency)
        if old_bal < bal_to_subtract:
            raise InsufficientBalance
        new_bal = old_bal - bal_to_subtract
        await self.update_balance(id, new_bal, currency)

    ################################################################################################################

    async def give_money(self, giverid, takerid, amount, currency):
        await self.subtract_balance(giverid, amount, currency)
        await self.add_balance(takerid, amount, currency)


    # Not in use
    """async def restart_table(self):
        await self.db.execute("DROP TABLE userinfo")
        await self.db.execute("CREATE TABLE userinfo (id BIGINT PRIMARY KEY, status VARCHAR (128), rank VARCHAR (25), kakechips BIGINT, owochips BIGINT);")
        print("Table restarted")"""