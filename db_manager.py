import aiosqlite

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path

    async def setup(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS server_data (
                    guild_id INTEGER PRIMARY KEY,
                    sv_ip TEXT,
                    sv_port INTEGER DEFAULT 8080,
                    token TEXT,
                    verified INTEGER DEFAULT 0  -- 0 = False, 1 = True
                )
            ''')
            await db.commit()
        print(f"Database initialized at {self.db_path}")

    async def update_ip(self, guild_id: int, ip: str):
        """Updates or inserts the server IP of a given guild"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO server_data (guild_id, sv_ip) 
                VALUES (?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET sv_ip = excluded.sv_ip
            ''', (guild_id, ip))
            await db.commit()

    async def update_token(self, guild_id: int, token: str):
        """Updates or inserts the token of a given guild"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO server_data (guild_id, token) 
                VALUES (?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET token = excluded.token
            ''', (guild_id, token))
            await db.commit()
    
    async def update_port(self, guild_id: int, port: int):
        """Updates or inserts the port of a given guild"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO server_data (guild_id, sv_port) 
                VALUES (?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET sv_port = excluded.sv_port
            ''', (guild_id, port))
            await db.commit()

    async def update_verified(self, guild_id: int, verified: bool):
        """Updates or inserts the verified status of a given guild"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO server_data (guild_id, verified) 
                VALUES (?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET verified = excluded.verified
            ''', (guild_id, verified))
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