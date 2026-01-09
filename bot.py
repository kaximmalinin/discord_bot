import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Создаем бота с префиксом команды
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Список триггерных слов/сочетаний
TRIGGER_WORDS = ['сво', 'зов', 'svo', 'zov']

@bot.event
async def on_ready():
    print(f'Бот {bot.user} успешно запущен!')
    print(f'ID бота: {bot.user.id}')
    print('------')

@bot.event
async def on_message(message):
    # Игнорируем сообщения от самого бота
    if message.author == bot.user:
        return
    
    # Проверяем содержимое сообщения на наличие триггерных слов
    message_content = message.content.lower()
    
    # Считаем сколько раз встречаются триггерные слова
    found_triggers = []
    for word in TRIGGER_WORDS:
        count = message_content.count(word)
        if count > 0:
            found_triggers.append((word, count))
    
    # Проверяем есть ли слово "андрей"
    has_andrey = 'андрей' in message_content
    
    # Если нашли триггерные слова
    if found_triggers:
        total_triggers = sum(count for word, count in found_triggers)
        
        # Если есть слово "андрей", создаем ветку
        if has_andrey:
            try:
                # Создаем ветку с названием на основе автора сообщения
                thread_name = f"Обсуждение от {message.author.display_name}"
                thread = await message.create_thread(name=thread_name, auto_archive_duration=60)
                
                # Отправляем "ГООООЛ" за каждое упоминание в созданной ветке
                for i in range(total_triggers):
                    await thread.send('ГООООЛ ⚽ (в ветке!)')
                
                # Также отправляем основное сообщение в оригинальный канал
                await message.channel.send('🎉 Создана ветка для обсуждения!')
                
            except discord.Forbidden:
                await message.channel.send("❌ У меня нет прав для создания веток!")
            except Exception as e:
                await message.channel.send(f"❌ Ошибка при создании ветки: {e}")
        
        else:
            # Если нет слова "андрей", отправляем в обычный канал
            for i in range(total_triggers):
                await message.channel.send('ГООООЛ ⚽')
    
    # Обрабатываем команды
    await bot.process_commands(message)

# Запуск бота
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("Ошибка: Токен не найден. Убедитесь, что файл .env существует и содержит DISCORD_TOKEN")