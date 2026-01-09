import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import re

# Загружаем переменные окружения из .env файла
load_dotenv()

# Создаем бота с префиксом команды
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Список триггерных слов/сочетаний
TRIGGER_WORDS = ["сво", "зов", "svo", "zov"]

# Список никнеймов для смены
NICKNAMES = [
    "СВООООООООО",
    "ПОБЕДА ЗА НАМИ",
    "СВО СВО СВО СВО",
    "ГОООООООООЛ",
    "СВОБОДА",
    "ЗОВ ПОБЕДЫ",
    "СВОЙ ЧЕМПИОН",
    "ПОБЕДНЫЙ СВО",
    "СВО СИЛА",
    "ЗОВ СВОБОДЫ",
]

# Список реакций для добавления
REACTIONS = [
    "⚽",  # футбольный мяч
    "🎯",  # попадание в цель
    "🔥",  # огонь
    "🚀",  # ракета
    "👏",  # аплодисменты
    "🎉",  # праздник
    "💥",  # взрыв
    "⭐",  # звезда
    "🏆",  # трофей
    "👍",  # палец вверх
    "❤️",  # сердце
    "🇷🇺",  # флаг России
    "🥅",  # футбольные ворота
    "👑",  # корона
]

# Реакции для питбайков - ВСЕ реакции сразу
PITBIKE_POSITIVE_REACTIONS = [
    "💯",
    "👍",
    "🔥",
    "🏍️",
    "🚀",
    "⭐",
    "🎯",
]  # все позитивные реакции
PITBIKE_NEGATIVE_REACTIONS = [
    "👎",
    "🖕",
    "💩",
    "😠",
    "🤮",
    "💔",
]  # все негативные реакции

# Оскорбительные слова для питбайков
NEGATIVE_WORDS = [
    "хуйня",
    "херня",
    "фигня",
    "фу",
    "гадость",
    "дерьмо",
    "отстой",
    "плохо",
    "ужасно",
    "кошмар",
    "беспонтово",
    "неочень",
    "таксебе",
    "говно",
    "мусор",
    "лажа",
    "шлак",
    "чепуха",
    "ерунда",
    "вранье",
]


@bot.event
async def on_ready():
    print(f"Бот {bot.user} успешно запущен!")
    print(f"ID бота: {bot.user.id}")
    print("------")


def find_trigger_words_in_message(message_content):
    """Находит слова с триггерными паттернами в сообщении"""
    found_words = []

    for pattern in WORD_PATTERNS:
        matches = re.findall(pattern, message_content, re.IGNORECASE)
        for match in matches:
            # Заменяем найденную часть на "СВО" с сохранением регистра
            if "сов" in match.lower():
                new_word = match.lower().replace("сов", "СВО")
            elif "осв" in match.lower():
                new_word = match.lower().replace("осв", "СВО")
            elif "сво" in match.lower():
                new_word = match.lower().replace("сво", "СВО")
            else:
                new_word = match

            # Сохраняем оригинальный регистр первой буквы
            if match[0].isupper():
                new_word = new_word[0].upper() + new_word[1:]

            found_words.append((match, new_word))

    return found_words


async def add_reactions(message, reactions_list=None):
    """Добавляет реакции к сообщению"""
    try:
        if reactions_list:
            # Используем конкретный список реакций - ВСЕ реакции сразу
            selected_reactions = reactions_list
        else:
            # Выбираем случайные реакции из общего списка
            num_reactions = random.randint(2, 4)
            selected_reactions = random.sample(REACTIONS, num_reactions)

        # Добавляем ВСЕ реакции с небольшой задержкой для натуральности
        for reaction in selected_reactions:
            try:
                await message.add_reaction(reaction)
                await asyncio.sleep(
                    0.3
                )  # Уменьшил задержку для быстрого добавления всех реакций
            except Exception as e:
                print(f"❌ Ошибка при добавлении реакции {reaction}: {e}")

    except Exception as e:
        print(f"❌ Общая ошибка при добавлении реакций: {e}")


async def handle_pitbike_message(message):
    """Обрабатывает сообщения с упоминанием питбайков"""
    message_lower = message.content.lower()

    # Проверяем есть ли оскорбительные слова
    has_negative_words = any(neg_word in message_lower for neg_word in NEGATIVE_WORDS)

    if has_negative_words:
        # ВСЕ негативные реакции за оскорбление питбайков
        await add_reactions(message, PITBIKE_NEGATIVE_REACTIONS)
        print(
            f"🚫 Питбайк оскорблен! Поставлены все негативные реакции. Сообщение: {message.content}"
        )
    else:
        # ВСЕ позитивные реакции за упоминание питбайков
        await add_reactions(message, PITBIKE_POSITIVE_REACTIONS)
        print(
            f"✅ Питбайк упомянут позитивно! Поставлены все позитивные реакции. Сообщение: {message.content}"
        )


@bot.event
async def on_message(message):
    # Игнорируем сообщения от самого бота
    if message.author == bot.user:
        return

    message_content = message.content
    message_lower = message_content.lower()

    # Проверяем есть ли слово "питбайк"
    has_pitbike = "питбайк" in message_lower

    # Обрабатываем питбайк отдельно - ставим ВСЕ реакции сразу
    if has_pitbike:
        await handle_pitbike_message(message)
        # Не прерываем выполнение, чтобы остальная логика тоже работала

    # Ищем слова с паттернами "сов", "осв", "сво"
    distorted_words = find_trigger_words_in_message(message_content)

    # Проверяем есть ли в сообщении обычные триггерные слова
    has_trigger_words = any(word in message_lower for word in TRIGGER_WORDS)

    # Проверяем есть ли слово "андрей"
    has_andrey = "андрей" in message_lower

    # Если нашли слова для искажения ИЛИ обычные триггерные слова
    if distorted_words or has_trigger_words:
        # Добавляем реакции к оригинальному сообщению (если еще не добавили для питбайка)
        if not has_pitbike:
            await add_reactions(message)

        # Меняем никнейм бота
        try:
            new_nickname = random.choice(NICKNAMES)
            guild = message.guild
            bot_member = guild.get_member(bot.user.id)
            await bot_member.edit(nick=new_nickname)
            print(f"Никнейм изменен на: {new_nickname}")
        except Exception as e:
            print(f"❌ Ошибка при смене никнейма: {e}")

        # Если нашли слова для искажения, отправляем специальный ответ
        if distorted_words:
            response_parts = []

            for original_word, distorted_word in distorted_words:
                response_parts.append(
                    f"**{original_word}**??? а может **{distorted_word.upper()}**??????"
                )

            response = "\n".join(response_parts) + "\n**ГОООООООООООООООЛ** ⚽"
            sent_message = await message.channel.send(response)
            # Добавляем реакции к ответу бота
            await add_reactions(sent_message)

        # Считаем обычные триггерные слова для дополнительных ответов
        total_triggers = sum(message_lower.count(word) for word in TRIGGER_WORDS)

        # Если есть слово "андрей", создаем ветку
        if has_andrey:
            try:
                thread_name = f"Обсуждение от {message.author.display_name}"
                thread = await message.create_thread(
                    name=thread_name, auto_archive_duration=60
                )

                # Отправляем дополнительные "ГООООЛ" в ветку
                for i in range(total_triggers):
                    thread_message = await thread.send("ГООООЛ ⚽ (в ветке!)")
                    await add_reactions(thread_message)

                thread_notification = await message.channel.send(
                    f"🎉 Создана ветка для обсуждения! Мой новый ник: {new_nickname}"
                )
                await add_reactions(thread_notification)

            except Exception as e:
                # Если не удалось создать ветку, отправляем в обычный канал
                for i in range(total_triggers):
                    sent_message = await message.channel.send("ГООООЛ ⚽")
                    await add_reactions(sent_message)

        # Если нет искаженных слов, но есть обычные триггеры - отправляем обычные ответы
        elif not distorted_words and total_triggers > 0:
            for i in range(total_triggers):
                sent_message = await message.channel.send("ГООООЛ ⚽")
                await add_reactions(sent_message)

            nick_message = await message.channel.send(
                f"⚡ Мой новый ник: {new_nickname}"
            )
            await add_reactions(nick_message)

    # Обрабатываем команды
    await bot.process_commands(message)


# Команда для просмотра оскорбительных слов
@bot.command()
async def negative_words(ctx):
    """Показать список оскорбительных слов для питбайков"""
    word_list = "\n".join([f"• {word}" for word in NEGATIVE_WORDS])
    sent_message = await ctx.send(
        f"**Список оскорбительных слов для питбайков:**\n{word_list}"
    )
    await add_reactions(sent_message)


# Команда для тестирования питбайк реакций
@bot.command()
async def test_pitbike(ctx):
    """Протестировать реакции на питбайки"""
    # Тест позитивных реакций
    test_message1 = await ctx.send("Тестируем ПОЗИТИВНЫЕ питбайк реакции! 🏍️")
    await add_reactions(test_message1, PITBIKE_POSITIVE_REACTIONS)

    # Тест негативных реакций
    test_message2 = await ctx.send("Тестируем НЕГАТИВНЫЕ питбайк реакции! 💩")
    await add_reactions(test_message2, PITBIKE_NEGATIVE_REACTIONS)


# Команда для просмотра всех реакций питбайка
@bot.command()
async def pitbike_reacts(ctx):
    """Показать все реакции для питбайков"""
    positive_reacts = " ".join(PITBIKE_POSITIVE_REACTIONS)
    negative_reacts = " ".join(PITBIKE_NEGATIVE_REACTIONS)

    message = (
        f"**Позитивные реакции для питбайков:**\n"
        f"{positive_reacts}\n\n"
        f"**Негативные реакции для питбайков:**\n"
        f"{negative_reacts}"
    )
    sent_message = await ctx.send(message)
    await add_reactions(sent_message)


# Команда для сброса никнейма
@bot.command()
async def reset_nick(ctx):
    """Сбросить никнейм бота на стандартный"""
    try:
        await ctx.guild.get_member(bot.user.id).edit(nick=None)
        sent_message = await ctx.send("✅ Никнейм сброшен на стандартный!")
        await add_reactions(sent_message)
    except discord.Forbidden:
        sent_message = await ctx.send("❌ Нет прав для изменения никнейма")
        await add_reactions(sent_message)


# Команда для просмотра текущего списка никнеймов
@bot.command()
async def nicks(ctx):
    """Показать список всех возможных никнеймов"""
    nick_list = "\n".join([f"• {nick}" for nick in NICKNAMES])
    sent_message = await ctx.send(f"**Список возможных никнеймов:**\n{nick_list}")
    await add_reactions(sent_message)


# Паттерны для поиска слов с "сов", "осв", "сво" (добавляем в конец)
WORD_PATTERNS = [
    r"\b\w*сов\w*\b",  # слова с "сов"
    r"\b\w*осв\w*\b",  # слова с "осв"
    r"\b\w*сво\w*\b",  # слова с "сво"
]

# Запуск бота
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print(
            "Ошибка: Токен не найден. Убедитесь, что файл .env существует и содержит DISCORD_TOKEN"
        )
