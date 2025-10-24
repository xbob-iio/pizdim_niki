from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os

# 🔐 Твои данные
api_id =   # <-- API ID
api_hash = ''  # <-- API HASH
session_name = 'my_session'

client = TelegramClient(session_name, api_id, api_hash)

async def main():
    await client.start()
    print("✅ Авторизация прошла")

    # Получаем список диалогов (чаты, группы и т.д.)
    dialogs = await client.get_dialogs()

    print("\n📋 Список чатов:")
    group_dialogs = [d for d in dialogs if d.is_group]

    for i, chat in enumerate(group_dialogs):
        print(f"{i + 1}. {chat.name} (ID: {chat.id})")

    # Спрашиваем пользователя, в какую группу зайти
    index = int(input("\n🔢 Введите номер группы: ")) - 1
    if index < 0 or index >= len(group_dialogs):
        print("❌ Неверный номер.")
        return

    target_group = group_dialogs[index]

    print(f"\n📨 Собираем сообщения из: {target_group.name}")

    users = set()

    async for msg in client.iter_messages(target_group, limit=1000):
        if msg.sender_id:
            try:
                sender = await client.get_entity(msg.sender_id)
                name = f"{sender.first_name or ''} {sender.last_name or ''}".strip()
                username = f"@{sender.username}" if sender.username else f"(ID: {sender.id})"
                users.add((name, username))
            except:
                continue

    with open("users.txt", "w", encoding="utf-8") as f:
        for name, username in users:
            f.write(f"{name} | {username}\n")

    print(f"\n✅ Готово! Сохранено {len(users)} пользователей в users.txt")

with client:
    client.loop.run_until_complete(main())

