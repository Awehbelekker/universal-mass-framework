class NotifierAgent(Agent):
    async def on_message(self, sender, message):
        if message.get("type") == "notify":
            recipient = message.get("recipient")
            content = message.get("content")
            # Simulate sending a notification (e.g., email, SMS, webhook)
            logging.info(f"{self.name} notifying {recipient}: {content}")
            await self.send(sender, "notification_sent", {"recipient": recipient})