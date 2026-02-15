import aiosqlite

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._db = None

    async def get_db(self):
        """Returns a persistent connection"""
        if self._db is None:
            self._db = await aiosqlite.connect(self.db_path)
            self._db.row_factory = aiosqlite.Row
        return self._db

    async def setup(self):
        db = await self.get_db()
        
        #{name: type_definition}
        columns = {
            "guild_id": "INTEGER PRIMARY KEY",
            "sv_ip": "TEXT",
            "sv_port": "INTEGER DEFAULT 8080",
            "token": "TEXT",
            "verified": "INTEGER DEFAULT 0",
        }

        await db.execute("CREATE TABLE IF NOT EXISTS server_data (guild_id INTEGER PRIMARY KEY)")
        
        for col_name, col_type in columns.items():
            if col_name == "guild_id": 
                continue
                
            try:
                await db.execute(f"ALTER TABLE server_data ADD COLUMN {col_name} {col_type}")
            except aiosqlite.OperationalError:
                # OperationalError means the column already exists
                pass
                
        await db.commit()
        print(f"Database schema synced. Current columns: {', '.join(columns.keys())}")

    async def update_guild_data(self, guild_id: int, **kwargs):
        """Updates any number of columns at once"""
        if not kwargs:
            return

        db = await self.get_db()
        cols = ", ".join(kwargs.keys())
        placeholders = ", ".join(["?"] * len(kwargs))
        update_str = ", ".join([f"{col} = excluded.{col}" for col in kwargs.keys()])

        query = f'''
            INSERT INTO server_data (guild_id, {cols}) 
            VALUES (?, {placeholders})
            ON CONFLICT(guild_id) DO UPDATE SET {update_str}
        '''
        
        values = [guild_id] + list(kwargs.values())
        await db.execute(query, values)
        await db.commit()

    async def get_guild_settings(self, guild_id: int):
        """Retrieves the config of a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row 
            
            async with db.execute(
                "SELECT sv_ip, sv_port, token FROM server_data WHERE guild_id = ?", 
                (guild_id,)
            ) as cursor:
                return await cursor.fetchone()
            
    async def close(self):
        """clean shutdown"""
        if self._db:
            await self._db.close()