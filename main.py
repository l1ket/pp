import asyncio
import logging
import aiosqlite
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import docx.document

from dannie import TOKEN
from handlers import common
from funcs import generate_token, update_token


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    db = await aiosqlite.connect('token_db')
    con = await db.cursor()
    await con.execute(
        '''CREATE TABLE IF NOT EXISTS my_table(
        token TEXT
        )
        ''')
    await db.commit()
    await db.close()

    db = await aiosqlite.connect('status_db')
    con = await db.cursor()
    await con.execute(
        '''CREATE TABLE IF NOT EXISTS bot_status(
        active_status TEXT
        )
        ''')
    await db.commit()
    await db.close()

    dp = Dispatcher(storage=MemoryStorage())
    os.environ["TOKEN"] = TOKEN
    bot = Bot(token=TOKEN)

    dp.include_router(common.router)

    await bot.delete_webhook(
        drop_pending_updates=True
        )  # Скипает все новые сообщения
    await dp.start_polling(bot)


async def test():
    # Список критериев
    criteria = [
        "заключение",
        "список использованных источников",
        "приложения",
        "оценка современного состояния решаемой научно-технической проблемы",
        "основание и исходные данные для разработки темы",
        "обоснование необходимости проведения НИР",
        "сведения о планируемом научно-техническом уровне разработки, о патентных исследованиях и выводы из них",
        "актуальность темы",
        "новизна темы",
        "связь данной работы с другими научно-исследовательскими работами",
        "цель и задачи исследования",
        "объект и предмет",
        "краткие выводы по результатам работы или отдельных ее этапов",
        "оценка полноты решений поставленных задач",
        "разработка рекомендаций и исходных данных по конкретному использованию результатов НИР",
        "результаты оценки технико-экономической эффективности внедрения",
        "результаты оценки научно-технического уровня выполненной НИР в сравнении с лучшими достижениями в этой области",
        "Заключение базируется на цели и задачах, выдвинутых во введении",
        "Список литературы",
        "Соблюдение ГОСТ",
        "Неверное оформление интернет источников (1,7)",
        "Неверное оформление учебника (25)"
    ]
    plus_and = ['+', '-']

    import docx
    doc = docx.Document()
    table = doc.add_table(rows=1, cols=1)
    row = table.add_row('qwe','qweqw')




if __name__ == '__main__':
    # x = asyncio.run(main())
    asyncio.run(test())