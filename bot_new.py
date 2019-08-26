#
# 21 String by string refactoring of the code (data names and etc)
# +1 add one list with schedule data
# 20 add buttons
# +2 make swithcer for 1 or 2 groups (typing)
# +4 add links to teachers
# +3 encode token
# +5 clean heroku and update pass
# _18 update schedule
# _17 deploy from null
# _19 Do tests
#

import requests
import datetime
import math
import time
from time import sleep
from cryptography.fernet import Fernet

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.telegram.org/bot{}/'.format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = False

        return last_update

def getWeekDay(wd):
    if wd == 'понедельник':
        return 'Monday'
    elif wd == 'вторник':
        return 'Tuesday'
    elif wd == 'среда':
        return 'Wednesday'
    elif wd == 'четверг':
        return 'Thursday'
    elif wd == 'пятница':
        return 'Friday'
    elif wd == 'суббота':
        return 'Saturday'
    else:
        return 'Sunday'

def output(group_schedule, requested_weekday, last_chat_id, greet_bot):
    amount = len(group_schedule[requested_weekday])
    greet_bot.send_message(
            last_chat_id,
            '''
                {}\n\n
                9:00-10:20: {}\n\n
                10:30-11:50: {}\n\n
                12:00-13:20: {}\n\n
                13:30-14:50: {}\n\n
                15:00-16:20: {}\n\n
                16:30-17:50: {}\n\n
                17:50-19:20: {}\n
            '''.format(
                    requested_weekday,
                    group_schedule[requested_weekday][0] if amount > 0 else '',
                    group_schedule[requested_weekday][1] if amount > 1 else '',
                    group_schedule[requested_weekday][2] if amount > 2 else '',
                    group_schedule[requested_weekday][3] if amount > 3 else '',
                    group_schedule[requested_weekday][4] if amount > 4 else '',
                    group_schedule[requested_weekday][5] if amount > 5 else '',
                    group_schedule[requested_weekday][6] if amount > 6 else '',
                ).replace('    ', '')
    )

### black box
key = 'W22QLeJifoX8i3847ZDGHh7DX_KyVj_kCXhTE7LClEM='
encrypted_data = 'gAAAAABdSzLJiXB2Hl3s1YUczG0VMDw7H6BdBoU7Sq1VRt20HO-e-AIK0Q2koi3JYKfcpIbaOStm7elSuxb9AA6Fe0kW1Vp8aA_uA-ZIWqqGv9CmHBgKknXMMDDCWg0mgol8UmX9bxju'
f = Fernet(key)

greet_bot = BotHandler(f.decrypt(encrypted_data.encode()).decode("utf-8"))
###

## is_week_even = True

# switcher parity
is_parity_switched = True

def main():
    new_offset = None
    is_week_even = False

    while True:

        is_week_even = is_parity_switched if (math.ceil((datetime.date.max.toordinal() + 1) / 7)  % 2) == 1 else not is_parity_switched # rewrite to the function

        greet_bot.get_updates(new_offset)
        last_update = greet_bot.get_last_update()

        if last_update == False:
            continue       

        last_update_id = last_update['update_id']
        last_chat_id = last_update['message']['chat']['id']

        ### Single group functional
        # requested_weekday = last_update['message']['text'].strip().lower() 
        ###

        ### Groups functional
        requested_weekday = last_update['message']['text'][:-1].strip().lower()
        group_number = last_update['message']['text'][-1]
        is_requested_first_group = (group_number == '1')
        ###

        requested_weekday = getWeekDay(requested_weekday)

        schedules = {
                                1: {  
                                    'Monday': [
                                            '', 
                                            'Пр. Алгебра 473' if is_week_even else '',
                                            'Лекц. Алгебра, Попов А.М., 260',
                                            'Обед',
                                            'Пр. Иностранный язык',
                                            'Пр. Иностранный язык' if is_week_even else 'ДПО "Модуль переводчика"',
                                            'ДПО "Модуль переводчика"'
                                            ],
                                    
                                    'Tuesday': [
                                                'Лекц. Компы, Аносова Н.П. 495а',
                                                'Лаб. Компы, ДК-3',
                                                'Обед',
                                                'Прикладная физическая культура, Мальченко А.Д., ФОК РУДН'
                                            ],

                                    'Wednesday': [
                                                    'Пр. Алгебра 104',
                                                    'Пр. Аналитическая геометрия 473',
                                                    'Лекц. Аналитическая геометрия, Гольдман М.Л., 260',
                                                    'Обед',
                                                    'Лекция Деловой Этикет Варламова И.Ю. 397' if is_week_even else 'Лекц. Алгебра 263',
                                                    'Пр. Деловой этикет 262' if is_week_even else ''
                                                ],
                                
                                    'Thursday': [
                                                    'Лекц./Пр. Проф. этика Лапшин И.Е. 104',
                                                    'Пр. История 258',
                                                    'Лекц. Матан 263',
                                                    'Пр. Матан 261',
                                                    'Обед',
                                                    ''
                                                ],

                                    'Friday': [
                                                'Лекц. Математический анализ, Марченко В.В., 261'
                                            ],

                                    'Saturday': [
                                                'Лекц. Политология 104' if is_week_even else 'Пр. Психология Зал 1',
                                                'Лекц. Политология 104' if is_week_even else 'Пр. Психология Зал 1'
                                                ],

                                    'Sunday': [
                                        'Проверь правописание',
                                        'Неправильно написан день недели'
                                    ]
                            },
                            2: {
                                    'Monday': [
                                            '', 
                                            '' if is_week_even else 'Пр. Алгебра 473',
                                            'Лекц. Алгебра, Попов А.М., 260',
                                            'Обед',
                                            'Пр. Иностранный язык',
                                            'Пр. Иностранный язык' if is_week_even else 'ДПО "Модуль переводчика"',
                                            'ДПО "Модуль переводчика"'
                                            ],
                                    
                                    'Tuesday': [
                                                'Лекц. Компы, Аносова Н.П. 495а',
                                                'Пр. Математический анализ 258',
                                                'Обед',
                                                'Прикладная физическая культура, Мальченко А.Д., ФОК РУДН'
                                            ],

                                    'Wednesday': [
                                                    'Пр. Аналитическая геометрия 264',
                                                    'Пр. Алгебра 471',
                                                    'Лекц. Аналитическая геометрия, Гольдман М.Л., 262',
                                                    'Обед',
                                                    'Лекция Деловой Этикет Варламова И.Ю. 397' if is_week_even else 'Лекц. Алгебра 263',
                                                    'Пр. Деловой этикет 262' if is_week_even else ''
                                                ],
                                
                                    'Thursday': [
                                                    'Лекц./Пр. Проф. этика Лапшин И.Е. 104',
                                                    'Пр. Матан 261',
                                                    'Лекц. Матан 263',
                                                    'Пр. История 264',
                                                    'Обед',
                                                    'Лаб. Компы'
                                                ],

                                    'Friday': [
                                                'Лекц. Математический анализ, Марченко В.В., 261'
                                            ],

                                    'Saturday': [
                                                'Лекц. Политология 104' if is_week_even else 'Пр. Психология Зал 1',
                                                'Лекц. Политология 104' if is_week_even else 'Пр. Психология Зал 1'
                                                ],

                                    'Sunday': [
                                        'Проверь правописание',
                                        'Неправильно написан день недели'
                                    ]
                        }
        }

        ### group functional
        #
        requested_schedule = schedules[1] if is_requested_first_group else schedules[2]
        ###
        ### single group functional
        # requested_schedule = schedules[1]
        ###


        output(requested_schedule, requested_weekday, last_chat_id, greet_bot)

        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
