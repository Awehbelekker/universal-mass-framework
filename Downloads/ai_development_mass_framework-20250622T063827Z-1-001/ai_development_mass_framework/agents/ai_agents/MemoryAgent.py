class MemoryAgent(Agent):
    def __init__(self, name, on_message, db_path=":memory:"):
        super().__init__(name, on_message)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT)")
        conn.commit()
        conn.close()

    async def on_message(self, sender, message):
        if message.get("type") == "store":
            key = message.get("key")
            value = message.get("value")
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))
            conn.commit()
            conn.close()
            logging.info(f"{self.name} stored {key}: {value}")
            await self.send(sender, "stored", {"key": key})
        elif message.get("type") == "retrieve":
            key = message.get("key")
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT value FROM memory WHERE key=?", (key,))
            row = c.fetchone()
            conn.close()
            value = row[0] if row else None
            logging.info(f"{self.name} retrieved {key}: {value}")
            await self.send(sender, "retrieved", {"key": key, "value": value})