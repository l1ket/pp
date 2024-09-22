import asyncio
import uuid
import aiosqlite
import json
import re

from aiohttp import ClientSession
from docx import Document


async def generate_token() -> str:
    myuuid = uuid.uuid4()

    async with ClientSession() as session:
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        payload = "scope=GIGACHAT_API_PERS"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(myuuid),
            'Authorization': 'Basic MjhiNTE5OTctMTIyNi00NzFkLWExNTktNWJiM2ZmNjE4ZjdlOjlmOTMxYTY3LWMzOTYtNGUzYy05ZDE0LTdiNjQ0NmIxZTRkMg=='
                    }

        async with session.post(url=url, headers=headers, data=payload, ssl=False) as response:
            # print(response.status) #### check response

            if response.status == 200:
                resp_js = await response.json()
                token: str = resp_js['access_token']
                return token
                # time_exp = resp_js['expires_at']   # int

                # if len(str(time_exp)) > 10:
                #     time_exp = time_exp / 1000

                # expires_date = datetime.datetime.fromtimestamp(time_exp).strftime('%Y-%m-%d %H:%M:%S')
                # print(token) ##### check token
            else:
                print("failed request")
                print(response.status)
                print(await response.text())


async def check_tokens(text):
    token = await generate_token()

    async with ClientSession() as session:
        url = "https://gigachat.devices.sberbank.ru/api/v1/tokens/count"
        
        payload = json.dumps({
        "model": "GigaChat",
        "input": [
            f"{text}"
        ]
        })
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
        }


        async with session.post(url=url, headers=headers, data=payload, ssl=False) as response:
            # print(response.status) #### check responsex``
            # print(await response.text())
            ...


async def request2(text):
    token = await generate_token()

    async with ClientSession() as session:
        url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
        payload = json.dumps({  
            "model": "GigaChat",
            "messages": [
                {
                "role": "system",
                "content": "Вы выступаете в роли преподавателя в институте. Пожалуйста, проверьте данный текст на соответствие по ГОСТу РФ 2024. В своем ответе предоставьте отчет, в котором укажите все несоответствия стандартам ГОСТа вот он:Таблица 2 - Отчет о научно-исследовательской работеПункт	ТребованиеПроверка разделов	Наличие структурных разделов	Наличие в работе разделов согласно ГОСТ 7.32 (раздел 4)Проверка ВведенияСоответствие текста Введения стандартам ГОСТ	При несоответствии Введения требованиям ГОСТ 7.32 (раздел 5.7) вывести комментарий, что необходимо исправить/добавить.Генерация моделью предполагаемого варианта верного исправления.Проверка Заключения	Соответствие текста Заключения стандартам ГОСТ	При несоответствии Заключения требованиям ГОСТ 7.32 (раздел 5.9) вывести комментарий, что необходимо исправить/добавить.Генерация моделью предполагаемого варианта верного исправления.Пересечение Введения и Заключения по смыслу	Заключение должно опираться на поставленные цели и задачи по Введении.Список литературыПроверка списка литературы на соответствие ГОСТ	Вывести комментарий о верности/неверности списка литературы + рекомендации (ГОСТ Р 7.0.100– 2018)Проверка соответствия указанных в тексте источников и списка литературы.Проверка наличия всех источников литературы в тексте работыПроверка следования индексации от наименьшего к наибольшемуПояснения к таблице 21.        Проверка разделовНаличие разделов в соответствии с разделом 4 ГОСТ 7.32Структурными элементами отчета о НИР являются:- титульный лист; - список исполнителей;- реферат; содержание;- термины и определения;- перечень сокращений и обозначений;- введение;- заключение;- список использованных источников; - приложения.2.        Проверка ВведенияТребования ГОСТ:оценка современногосостояния решаемой научно-технической проблемы основание и исходные данные для разработки темы обоснование необходимости проведения НИРсведения о планируемом научно-техническом уровне разработки, о патентных исследованиях и выводы из них актуальность и новизна темысвязь данной работы с другими научно-исследовательскими работами.цель и задачи исследования Генерация текстаГенерация моделью предполагаемого варианта верного исправления. (Пример: не сформулирована Актуальность работы, генерируется вариант формулировки актуальности)Пересечение Введения и Заключения. Цель и задачи выдвинутые во Введении соответствуют выводам сделанным в Заключении3.        Проверка ЗаключенияСоответствие текста Заключения разделу 5.9 ГОСТ 7.32Требования ГОСТ:- краткие выводы по результатам работы или отдельных ее этапов;- оценка полноты решений поставленных задач;- разработка рекомендаций и исходных данных по конкретному использованию результатов НИР;- результаты оценки технико-экономической эффективности внедрения;- результаты оценки научно-технического уровня выполненной НИР в сравнении с лучшими достижениями в этой области.Генерация текстаГенерация моделью предполагаемого варианта верного исправления. (Пример: не сформулирована Актуальность работы, генерируется вариант формулировки актуальности)Ответ, сгенерированный ИИ, должен быть точным, понятным, соответствовать контексту запроса и не отличаться от ответа, сгенерированного человеком.        Список литературыроверка списка литературы на соответствие ГОСТ Р 7.0.100– 2018 (раздел 6.16)Проверка наличия всех источников литературы в тексте работыПроверка следования индексации от наименьшего к наибольшемуОбщая схема библиографического описания:Заголовок (фамилия, инициалы автора) Основное заглавие : Дополнительные сведения (тип издания) / Сведения об ответственности (И. О. Фамилия автора, редакторы, переводчики, коллективы).  Сведения об издании.  Место издания : Издательство, Год издания.  Количество страниц.	При описании электронной книги необходимо добавить сведения об адресе ресурса в интернете и дату обращения к нему. Если автор один (до трех) в издании, то указывается один автор в заголовке, один автор (два или три соответственно) за косой чертой в поле ответственности. При четырех авторах заголовок не прописывается, после косой черты в поле ответственности перечисляются все авторы. При пяти и более авторов в издании – заголовок не прописывается и описание начинается с основного заглавия, указываются три первых автора и сокращение [и др.] за косой чертой в поле ответственности.. Если такие несоответствия есть,то напишите, в чем они заключаются, и предложите способы исправления,все свои исправления поясните. Если ошибок нет, ответьте одним словом: 'НЕТ'. При описании каждой ошибки пиши с новой строки."
                },
                {
                "role": "user",
                "content": f"{text}"
                }
            ],
            "n": 1,
            "stream": False,
            "update_interval": 0
            })
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
            }
        async with session.post(url=url, headers=headers, data=payload, ssl=False) as response:
                    # print(response.status) #### check responsex``
                    # print(await response.text())
                    return await response.json()
        

async def request3(text):
    token = await generate_token()
    await check_tokens(text=text)

    async with ClientSession() as session:
        url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
        payload = json.dumps({  
            "model": "GigaChat",
            "messages": [
                {
                "role": "system",
                "content": "Проанализируйте предоставленный текст на наличие ошибок по заданным критериям. Ответьте в формате: «Критерий: (да/нет)». Критерии: заключение,список использованных источников,приложения,оценка современного состояния решаемой научно-технической проблемы,основание и исходные данные для разработки темы,обоснование необходимости проведения НИР,сведения о планируемом научно-техническом уровне разработки, о патентных исследованиях и выводы из них,актуальность темы,новизна темы,связь данной работы с другими научно-исследовательскими работами.,цель и задачи исследования,объект и предмет,краткие выводы по результатам работы или отдельных ее этапов,оценка полноты решений поставленных задач,разработка рекомендаций и исходных данных по конкретному использованию результатов НИР,результаты оценки технико-экономической эффективности внедрения,результаты оценки научно-технического уровня выполненной НИР в сравнении с лучшими достижениями в этой области,Заключение базируется на цели и задачах, выдвинутых во введении,Список литературы,Соблюдение ГОСТ,Неверное оформление интернет источников (1,7),Неверное оформление учебника (25),Для каждого критерия отметьте «да», если он есть, и «нет», если он отсутствует"
                },
                {
                "role": "user",
                "content": f"{text}"
                }
            ],
            "n": 1,
            "stream": False,
            "update_interval": 0
            })
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
            }
        async with session.post(url=url, headers=headers, data=payload, ssl=False) as response:
            # print(response.status) #### check responsex``
            # print(await response.text())
            # print(await response.text())
            # print(await response.text())
            return await response.json()


async def asd(path):

    def read_word_document(file_path):
        # Чтение документа Word
        doc = Document(file_path)
        full_text = []
        
        # Сбор всего текста из параграфов
        for para in doc.paragraphs:
            full_text.append(para.text)
        
        # Объединяем все параграфы в одну строку
        text = ' '.join(full_text)

        cleaned_text = re.sub(r'\s+', ' ', text).strip()
        
        # Удаляем все лишние символы, оставляем только буквы, цифры, пробелы и базовые знаки препинания
        cleaned_text = re.sub(r'[^a-zA-Z0-9А-Яа-я.,!?;:\-\(\)\[\]\'\" ]', '', cleaned_text)

        # print(cleaned_text)
        return(cleaned_text)


    async def split_text_by_words(text, word_limit=150):
        words = text.split()
        chunks = []
        total_text = ''
        # Разделяем текст на блоки по word_limit слов
        for i in range(0, len(words), word_limit):
            chunk = ' '.join(words[i:i + word_limit])
            chunks.append(chunk)
            # await check_tokens(chunk)
            responce = await request2(chunk)
            # print(responce)
            reason = responce['choices'][0]['finish_reason']
            # print(reason)
            if reason == 'blacklist':
                # print(responce)
                # print('stop')
                continue
            else:
                content = responce['choices'][0]['message']['content']
                if content == 'НЕТ':
                    # print('NO')
                    continue
                else:
                    total_text += f'{content}\n'
                    # print(content)
        return total_text

    async def process_word_document(file_path: str):
        # Чтение полного текста документа
        full_text = read_word_document(file_path)
        
        # Разделение текста на блоки по 2000 слов
        return await split_text_by_words(full_text)

    return await process_word_document(path)


async def update_token():
    db = await aiosqlite.connect('token_db')
    con = await db.cursor()
    await con.execute('SELECT token from my_table')
    rows = await con.fetchall()
    if rows == []:
        token = await generate_token()
        await con.execute('INSERT INTO my_table(token) VALUES(?)', (token,))
        await db.commit()
        await db.close()
    else:
        token = await generate_token()
        await con.execute('UPDATE my_table SET token = ?', (token,))
        await db.commit()
        await db.close()


# async def check_status():
#     db = await aiosqlite.connect('status_db')
#     con = await db.cursor()
#     await con.execute('SELECT active_status from bot_status')
#     rows = await con.fetchall()
#     print(rows)
#     await db.commit()
#     await db.close()


# async def set_true():
#     db = await aiosqlite.connect('status_db')
#     con = await db.cursor()
#     await con.execute('INSERT INTO bot_status(active_status) VALUES (?)', ('TRUE'))
#     await db.commit()
#     await db.close()


if __name__ == '__main__':
    # asyncio.run(set_true())
    # asyncio.run(check_status())
    ...
