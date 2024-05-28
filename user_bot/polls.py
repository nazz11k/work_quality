import telebot

from datetime import datetime, timezone

from api import *
from markups import *
from services import *


def to_main_menu(massage, bot):
    bot.send_message(massage.chat.id, 'Головне меню', reply_markup=poll_main())


class PersonalData:
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message
        self.region = None
        self.results = {
            'telegram_id': message.chat.id,
            'first_name': None,
            'last_name': None,
            'gender': None,
            'age': None,
            'email': None,
            'phone': None,
            'city': None
        }

    def start(self):
        self.question_1()
        return self.results

    def question_1(self):
        user_id = self.message.chat.id
        self.bot.send_message(user_id, 'Введіть своє ім\'я:')
        self.bot.register_next_step_handler(self.message, self.question_2)

    def question_2(self, message):
        user_id = self.message.chat.id
        self.results['first_name'] = message.text
        self.bot.send_message(user_id, 'Введіть своє прізвище:', reply_markup=types.ReplyKeyboardRemove())
        self.bot.register_next_step_handler(message, self.question_3)

    def question_3(self, message):
        user_id = self.message.chat.id
        self.results['last_name'] = message.text
        self.bot.send_message(user_id, 'Вкажіть свою стать:', reply_markup=gender_markup())
        self.bot.register_next_step_handler(message, self.question3_validation)

    def question3_validation(self, message):
        user_id = self.message.chat.id
        if message.text not in ['Чоловік', 'Жінка', 'Інше', 'Не хочу вказувати']:
            self.bot.send_message(user_id, 'Некоректно введені дані.\nВведіть стать знову:', reply_markup=gender_markup())
            self.bot.register_next_step_handler(message, self.question3_validation)
        else:
            self.question_4(message)

    def question_4(self, message):
        user_id = self.message.chat.id
        self.results['gender'] = message.text
        self.bot.send_message(user_id, 'Введіть ваш вік:', reply_markup=types.ReplyKeyboardRemove())
        self.bot.register_next_step_handler(message, self.question_4validation)

    def question_4validation(self, message):
        user_id = self.message.chat.id
        if not message.text.isdigit():
            self.bot.send_message(user_id, 'Некоректно введені дані.\nВведіть вік знову:', reply_markup=types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(message, self.question_4validation)
        else:
            self.question_5(message)

    def question_5(self, message):
        user_id = self.message.chat.id
        self.results['age'] = message.text
        self.bot.send_message(user_id, 'Введіть вашу електронну пошту:', reply_markup=types.ReplyKeyboardRemove())
        self.bot.register_next_step_handler(message, self.question_5validation)

    def question_5validation(self, message):
        user_id = self.message.chat.id
        if not is_mail_correct(message.text):
            self.bot.send_message(user_id, 'Некоректно введені дані.\nВведіть електронну пошту знову:', reply_markup=types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(message, self.question_5validation)
        else:
            self.question_6(message)

    def question_6(self, message):
        user_id = self.message.chat.id
        self.results['email'] = message.text
        self.bot.send_message(user_id, 'Вкажіть номер свого телефону:\n(формат: 0951070626)', reply_markup=types.ReplyKeyboardRemove())
        self.bot.register_next_step_handler(message, self.question_6validation)

    def question_6validation(self, message):
        user_id = self.message.chat.id
        if not is_phone_correct(message.text):
            self.bot.send_message(user_id, 'Некоректно введені дані.\nВведіть номер телефону знову:', reply_markup=types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(message, self.question_6validation)
        else:
            self.question_7(message)

    def question_7(self, message):
        user_id = self.message.chat.id
        self.results['phone'] = message.text
        regions = get_regions_list()
        self.bot.send_message(user_id, 'Вкажіть область в якій проживаєте:', reply_markup=regions_markup(regions))
        self.bot.register_next_step_handler(message, self.question7_validation)

    def question7_validation(self, message):
        user_id = self.message.chat.id
        regions = get_regions_list()
        if message.text not in regions:
            self.bot.send_message(user_id, 'Некоректно введені дані.\nВведіть область знову:', reply_markup=regions_markup(regions))
            self.bot.register_next_step_handler(message, self.question7_validation)
        else:
            self.region = get_region_id(message.text)
            self.question_8(message)

    def question_8(self, message):
        user_id = self.message.chat.id
        cities = get_cities_list(self.region)
        self.bot.send_message(user_id, 'Вкажіть район в якому проживаєте:', reply_markup=cities_markup(cities))
        self.bot.register_next_step_handler(message, self.question8_validation)

    def question8_validation(self, message):
        user_id = self.message.chat.id
        cities = get_cities_list(self.region)
        if message.text not in cities:
            self.bot.send_message(user_id, 'Некоректно введені дані.\nВведіть район знову:', reply_markup=cities_markup(cities))
            self.bot.register_next_step_handler(message, self.question8_validation)
        else:
            self.results['city'] = get_city_id(message.text)
            self.result_processing(message)


    def result_processing(self, message):
        user_id = self.message.chat.id
        if is_client_exists(user_id):
            response = update_client_data(user_id, self.results)
            print(response.status_code)
            if response.status_code == 200:
                data = response.json()
                self.bot.send_message(user_id, f'Дані успішно змінені \n {personal_data_to_text(data)}', reply_markup=types.ReplyKeyboardRemove())
                to_main_menu(message, self.bot)
            else:
                self.bot.send_message(user_id, 'Помилка зміни даних, спробуйте ще раз', reply_markup=types.ReplyKeyboardRemove())
                to_main_menu(message, self.bot)
        else:
            response = post_client_data(self.results)
            if response.status_code == 201:
                data = response.json()
                self.bot.send_message(user_id, f'Дані успішно збережені \n {personal_data_to_text(data)}', reply_markup=types.ReplyKeyboardRemove())
                to_main_menu(message, self.bot)
            else:
                self.bot.send_message(user_id, 'Помилка збереження даних, cпробуйте ще раз', reply_markup=types.ReplyKeyboardRemove())
                self.start()


class FirstPoll:
    def __init__(self, bot, telegram_id):
        self.bot = bot
        self.telegram_id = telegram_id
        self.results = {
            'telegram_id': telegram_id,
            'datetime_started': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z'),
        }

    def start(self):
        self.poll_acception()

    def poll_acception(self):
        name = get_user_name(self.telegram_id)
        message = self.bot.send_message(self.telegram_id, f'{name}, у нас є коротке опитування про те як ви дізналися про наш бренд', reply_markup=poll_accept())
        self.bot.register_next_step_handler(message, self.poll_acception_processing)

    def poll_acception_processing(self, message):
        if message.text == 'Пройти':
            self.question_1()
        else:
            self.bot.send_message(self.telegram_id, 'Дякуємо за увагу', reply_markup=types.ReplyKeyboardRemove())
            to_main_menu(message, self.bot)

    def question_1(self):
        message = self.bot.send_message(self.telegram_id, 'Як ви дізналися про наш бренд?', reply_markup=poll_social())
        self.bot.register_next_step_handler(message, self.poll_result_processing)

    def poll_result_processing(self, message):
        if message.text == 'Інше':
            self.results['source'] = 'Інше'
            self.bot.send_message(self.telegram_id, 'Введіть як ви дізналися про наш бренд', reply_markup=types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(message, self.other_result_processing)
        else:
            self.results['source'] = message.text
            print(self.results)
            response = post_FirsClientCheck(self.results)
            if response.status_code == 201:
                self.bot.send_message(self.telegram_id, 'Дякуємо за відповідь', reply_markup=types.ReplyKeyboardRemove())
                to_main_menu(message, self.bot)
            else:
                self.bot.send_message(self.telegram_id, 'Помилка відправлення відповіді, пройдіть опитування ще раз')
                self.poll_acception()

    def other_result_processing(self, message):
        self.results['comment'] = message.text
        response = post_FirsClientCheck(self.results)
        if response.status_code == 201:
            self.bot.send_message(self.telegram_id, 'Дякуємо за відповідь')
            to_main_menu(message, self.bot)
        else:
            self.bot.send_message(self.telegram_id, 'Помилка відправлення відповіді, пройдіть опитування ще раз')
            self.poll_acception()


class MonthlyPoll:
    def __init__(self, bot, telegram_id):
        self.bot = bot
        self.telegram_id = telegram_id
        self.results = {
            'telegram_id': self.telegram_id,
            'answer1': None,
            'answer2': None,
            'answer3': None,
            'datetime_sended': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z'),
        }

    def start(self):
        self.poll_acception()

    def poll_acception(self):
        name = get_user_name(self.telegram_id)
        message = self.bot.send_message(self.telegram_id, f'{name}, ми маємо коротке опитування для вас', reply_markup=poll_accept())
        self.bot.register_next_step_handler(message, self.poll_acception_processing)

    def poll_acception_processing(self, message):
        if message.text == 'Пройти':
            self.results['datetime_started'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z')
            self.question_1()
        else:
            self.bot.send_message(self.telegram_id, 'Дякуємо за увагу', reply_markup=types.ReplyKeyboardRemove())
            to_main_menu(message, self.bot)

    def question_1(self):
        message = self.bot.send_message(self.telegram_id, 'Яка вірогідність того, що ви порекомендуєте наші послуги своїм друзям та знайомим?', reply_markup=poll_up10())
        self.bot.register_next_step_handler(message, self.question_2)

    def question_2(self, message):
        self.results['answer1'] = message.text
        self.bot.send_message(self.telegram_id, 'Яка вірогідність того, що ви знову купите продукт у нас?', reply_markup=poll_up10())
        self.bot.register_next_step_handler(message, self.question_3)

    def question_3(self, message):
        self.results['answer2'] = message.text
        self.bot.send_message(self.telegram_id, 'Яка вірогідність того, що ви скористаєтеся іншими продуктами чи послугами нашої компанії?', reply_markup=poll_up10())
        self.bot.register_next_step_handler(message, self.poll_result_processing)

    def poll_result_processing(self, message):
        self.results['answer3'] = message.text
        print(self.results)
        response = post_CustomerLoyaltyIndex(self.results)
        if response.status_code == 201:
            self.bot.send_message(self.telegram_id, 'Дякую за участь у опитуванні!', reply_markup=types.ReplyKeyboardRemove())
            to_main_menu(message, self.bot)
        else:
            self.bot.send_message(self.telegram_id, 'Помилка відправлення відповіді, пройдіть опитування ще раз')
            self.poll_acception()


class ShopPoll:
    def __init__(self, bot, telegram_id, service_id):
        self.bot = bot
        self.telegram_id = telegram_id
        self.results = {
            'telegram_id': self.telegram_id,
            'service': service_id,
            'datetime_sended': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z'),
        }

    def start(self):
        self.poll_acception()

    def poll_acception(self):
        name = get_user_name(self.telegram_id)
        message = self.bot.send_message(self.telegram_id, f'{name}, у нас є коротке опитування про ваш останній візит до нашого магазину.', reply_markup=poll_accept())
        self.bot.register_next_step_handler(message, self.poll_acception_processing)

    def poll_acception_processing(self, message):
        if message.text == 'Пройти':
            self.question_1()
        else:
            self.bot.send_message(self.telegram_id, 'Дякуємо за увагу', reply_markup=types.ReplyKeyboardRemove())
            to_main_menu(message, self.bot)

    def question_1(self):
        message = self.bot.send_message(self.telegram_id, 'Як ви оцінюєте асортимент нашого магазину?', reply_markup=poll_up5_skip())
        self.bot.register_next_step_handler(message, self.question2)

    def question2(self, message):
        self.results['datetime_started'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z')
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer1'] = message.text
        self.bot.send_message(self.telegram_id, 'Як ви оцінюєте розташування нашого магазину?', reply_markup=poll_up5_skip())
        self.bot.register_next_step_handler(message, self.question3)

    def question3(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer2'] = message.text
        self.bot.send_message(self.telegram_id, 'Як ви оцінюєте чистоту та організацію простору в нашому магазині?', reply_markup=poll_up5_skip())
        self.bot.register_next_step_handler(message, self.question4)

    def question4(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer3'] = message.text
        self.bot.send_message(self.telegram_id, 'Як ви оцінюєте дизайн та атмосферу в нашому магазині?', reply_markup=poll_up5_skip())
        self.bot.register_next_step_handler(message, self.question5)

    def question5(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer4'] = message.text
        self.bot.send_message(self.telegram_id, 'Залиште коментар про наш магазин:', reply_markup=skip())
        self.bot.register_next_step_handler(message, self.question6)

    def question6(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer5'] = message.text
        self.bot.send_message(self.telegram_id, 'Як ви оцінюєте знання продуктів нашими продавцями?', reply_markup=poll_up5_skip())
        self.bot.register_next_step_handler(message, self.question7)

    def question7(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer6'] = message.text
        self.bot.send_message(self.telegram_id, 'Як ви оцінюєте комунікацйні навички наших продавців?', reply_markup=poll_up5_skip())
        self.bot.register_next_step_handler(message, self.question8)

    def question8(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer7'] = message.text
        self.bot.send_message(self.telegram_id, 'Як ви оцінюєте ввічливість та доброзичливість наших продавців?', reply_markup=poll_up5_skip())
        self.bot.register_next_step_handler(message, self.question9)

    def question9(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer8'] = message.text
        self.bot.send_message(self.telegram_id, 'Як ви оцінюєте швидкість обслуговування наших продавців?', reply_markup=poll_up5_skip())
        self.bot.register_next_step_handler(message, self.question10)

    def question10(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer9'] = message.text
        self.bot.send_message(self.telegram_id, 'Як ви оцінюєте чесність та прозорість наших продавців?', reply_markup=poll_up5_skip())
        self.bot.register_next_step_handler(message, self.question11)

    def question11(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer10'] = message.text
        self.bot.send_message(self.telegram_id, 'Залиште коментар про наш персонал:', reply_markup=skip())
        self.bot.register_next_step_handler(message, self.result_processing)

    def result_processing(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer11'] = message.text
        print(self.results)
        response = post_CustomerShopFeedback(self.results)
        if response.status_code == 201:
            self.bot.send_message(self.telegram_id, 'Дякуємо за участь у опитуванні!', reply_markup=types.ReplyKeyboardRemove())
            to_main_menu(message, self.bot)
        else:
            self.bot.send_message(self.telegram_id, 'Помилка відправлення відповіді, пройдіть опитування ще раз')
            self.poll_acception()


class ProductPoll:
    def __init__(self, bot, telegram_id, service_id):
        self.bot = bot
        self.telegram_id = telegram_id
        self.results = {
            'telegram_id': self.telegram_id,
            'service': service_id,
            'datetime_sended': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z'),
        }

    def start(self):
        self.poll_acception()

    def poll_acception(self):
        name = get_user_name(self.telegram_id)
        message = self.bot.send_message(self.telegram_id, f'{name}, нас є коротке опитування про вашу останню покупку.', reply_markup=poll_accept())
        self.bot.register_next_step_handler(message, self.poll_acception_processing)

    def poll_acception_processing(self, message):
        if message.text == 'Пройти':
            self.results['datetime_started'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z')
            self.question_1()
        else:
            self.bot.send_message(self.telegram_id, 'Дякуємо за увагу', reply_markup=types.ReplyKeyboardRemove())
            to_main_menu(message, self.bot)

    def question_1(self):
        message = self.bot.send_message(self.telegram_id, 'Наскільки легко вам було використовувати наш продукт?', reply_markup=poll_up5())
        self.bot.register_next_step_handler(message, self.question2)

    def question2(self, message):
        self.results['answer1'] = message.text
        self.bot.send_message(self.telegram_id, 'Залиште коментар про наш магазин', reply_markup=skip())
        self.bot.register_next_step_handler(message, self.result_processing)

    def result_processing(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer2'] = message.text
        print(self.results)
        response = post_ProductFeedback(self.results)
        if response.status_code == 201:
            self.bot.send_message(self.telegram_id, 'Дякуємо за участь у опитуванні!', reply_markup=types.ReplyKeyboardRemove())
            to_main_menu(message, self.bot)
        else:
            self.bot.send_message(self.telegram_id, 'Помилка відправлення відповіді, пройдіть опитування ще раз')
            self.poll_acception()


class RefundPoll:
    def __init__(self, bot, telegram_id, service_id):
        self.bot = bot
        self.telegram_id = telegram_id
        self.results = {
            'telegram_id': self.telegram_id,
            'service': service_id,
            'datetime_sended': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z'),
        }

    def start(self):
        self.poll_acception()

    def poll_acception(self):
        name = get_user_name(self.telegram_id)
        message = self.bot.send_message(self.telegram_id, f'{name}, нещодавно ви скористалися послугою повернення, у нас є коротку опитування про це', reply_markup=poll_accept())
        self.bot.register_next_step_handler(message, self.poll_acception_processing)

    def poll_acception_processing(self, message):
        if message.text == 'Пройти':
            self.results['datetime_started'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z')
            self.question_0()
        else:
            self.bot.send_message(self.telegram_id, 'Дякуємо за увагу', reply_markup=types.ReplyKeyboardRemove())
            to_main_menu(message, self.bot)

    def question_0(self):
        message = self.bot.send_message(self.telegram_id, 'Оцініть процес повернення товару:', reply_markup=poll_up5())
        self.bot.register_next_step_handler(message, self.question_1)

    def question_1(self, message):
        self.results['answer1'] = message.text
        message = self.bot.send_message(self.telegram_id, 'Яка причина повернення товару?', reply_markup=poll_refund())
        self.bot.register_next_step_handler(message, self.result_processing)

    def result_processing(self, message):
        self.results['answer2'] = message.text
        if message.text == 'Інше':
            self.bot.send_message(self.telegram_id, 'Введіть причину повернення товару', reply_markup=types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(message, self.other_result_processing)
        else:
            response = post_RefundFeedback(self.results)
            if response.status_code == 201:
                message = self.bot.send_message(self.telegram_id, 'Дякуємо за участь у опитуванні!', reply_markup=types.ReplyKeyboardRemove())
                to_main_menu(message, self.bot)
            else:
                self.bot.send_message(self.telegram_id, 'Помилка відправлення відповіді, пройдіть опитування ще раз')
                self.poll_acception()

    def other_result_processing(self, message):
        self.results['comment'] = message.text
        print(self.results)
        response = post_RefundFeedback(self.results)
        if response.status_code == 201:
            message = self.bot.send_message(self.telegram_id, 'Дякуємо за участь у опитуванні!', reply_markup=types.ReplyKeyboardRemove())
            to_main_menu(message, self.bot)
        else:
            self.bot.send_message(self.telegram_id, 'Помилка відправлення відповіді, пройдіть опитування ще раз')
            self.poll_acception()


class RepairPoll:
    def __init__(self, bot, telegram_id, service_id):
        self.bot = bot
        self.telegram_id = telegram_id
        self.results = {
            'telegram_id': self.telegram_id,
            'service': service_id,
            'datetime_sended': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z'),
        }

    def start(self):
        self.poll_acception()

    def poll_acception(self):
        name = get_user_name(self.telegram_id)
        message = self.bot.send_message(self.telegram_id, f'{name}, нещодавно ви користувалися послугами нашого сервісного центру, у нас є коротке опитування про це', reply_markup=poll_accept())
        self.bot.register_next_step_handler(message, self.poll_acception_processing)

    def poll_acception_processing(self, message):
        if message.text == 'Пройти':
            self.results['datetime_started'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z')
            self.question_1()
        else:
            self.bot.send_message(self.telegram_id, 'Дякуємо за увагу', reply_markup=types.ReplyKeyboardRemove())
            to_main_menu(message, self.bot)

    def question_1(self):
        message = self.bot.send_message(self.telegram_id, 'Як ви оцінюєте швидкість ремонту?', reply_markup=poll_up5_skip())
        self.bot.register_next_step_handler(message, self.question2)

    def question2(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer1'] = message.text
        self.bot.send_message(self.telegram_id, 'Як ви оцінюєте якість ремонту?', reply_markup=poll_up5_skip())
        self.bot.register_next_step_handler(message, self.question3)

    def question3(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer2'] = message.text
        self.bot.send_message(self.telegram_id, 'Як ви оцінюєте вартість ремонту?', reply_markup=poll_up5_skip())
        self.bot.register_next_step_handler(message, self.question4)

    def question4(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer3'] = message.text
        self.bot.send_message(self.telegram_id, 'Як ви оцінюєте якість обслуговування в сервісному центрі', reply_markup=poll_up5_skip())
        self.bot.register_next_step_handler(message, self.question5)

    def question5(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer4'] = message.text
        self.bot.send_message(self.telegram_id, 'Залиште коментар про сервісний центр:', reply_markup=skip())
        self.bot.register_next_step_handler(message, self.result_processing)

    def result_processing(self, message):
        if message.text == 'Пропустити':
            pass
        else:
            self.results['answer5'] = message.text
        print(self.results)
        response = post_RepairFeedback(self.results)
        if response.status_code == 201:
            message = self.bot.send_message(self.telegram_id, 'Дякуємо за участь у опитуванні!', reply_markup=types.ReplyKeyboardRemove())
            to_main_menu(message, self.bot)
        else:
            self.bot.send_message(self.telegram_id, 'Помилка відправлення відповіді, пройдіть опитування ще раз')
            self.poll_acception()

