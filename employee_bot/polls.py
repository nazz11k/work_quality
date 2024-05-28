import telebot

from api import *
from services import *
from markups import *


class PersonalData:
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message
        self.region = None
        self.city = None
        self.regions = None
        self.cities = None
        self.workplaces = None
        self.results = {
            'telegram_id': message.chat.id,
            'first_name': None,
            'last_name': None,
            'email': None,
            'phone': None,
            'workplace': None,
        }

    def start(self):
        self.first_name()

    def region_list(self):
        return [region['name'] for region in self.regions]

    def region_id(self, region_name):
        for region in self.regions:
            if region['name'] == region_name:
                return region['id']
        return None

    def city_id(self, city_name):
        for city in self.cities:
            if city['name'] == city_name:
                return city['id']

    def workplace_id(self, workplace_name):
        for workplace in self.workplaces:
            if workplace['name'] == workplace_name:
                return workplace['id']

    def first_name(self):
        self.bot.send_message(self.message.chat.id, 'Введіть ім\'я')
        self.bot.register_next_step_handler(self.message, self.first_name_processing)

    def first_name_processing(self, message):
        self.results['first_name'] = message.text
        self.second_name()

    def second_name(self):
        self.bot.send_message(self.message.chat.id, 'Введіть прізвище')
        self.bot.register_next_step_handler(self.message, self.second_name_processing)

    def second_name_processing(self, message):
        self.results['last_name'] = message.text
        self.email()

    def email(self):
        self.bot.send_message(self.message.chat.id, 'Введіть електронну пошту')
        self.bot.register_next_step_handler(self.message, self.email_processing)

    def email_processing(self, message):
        if mail_is_correct(message.text):
            self.results['email'] = message.text
            self.phone()
        else:
            self.bot.send_message(self.message.chat.id, 'Некоректна електронна пошта')
            self.email()

    def phone(self):
        self.bot.send_message(self.message.chat.id, 'Введіть номер телефону')
        self.bot.register_next_step_handler(self.message, self.phone_processing)

    def phone_processing(self, message):
        if is_phone_correct(message.text):
            self.results['phone'] = message.text
            self.workplace_region()
        else:
            self.bot.send_message(self.message.chat.id, 'Некоректний номер телефону')
            self.phone()

    def workplace_region(self):
        response = get_regions_with_workplaces()
        if response.status_code == 200:
            self.regions = response.json()
            self.bot.send_message(self.message.chat.id, 'Оберіть ваш регіон', reply_markup=regions_markup(self.region_list()))
            self.bot.register_next_step_handler(self.message, self.workplace_region_processing)
        else:
            self.bot.send_message(self.message.chat.id, 'Помилка сервера')

    def workplace_region_processing(self, message):
        if message.text in self.region_list():
            self.region = self.region_id(message.text)
            self.workplace_city()
        else:
            self.bot.send_message(self.message.chat.id, 'Некоректний регіон')
            self.workplace_region()

    def workplace_city(self):
        response = get_cities_with_workplaces(self.region)
        if response.status_code == 200:
            self.cities = response.json()
            self.bot.send_message(self.message.chat.id, 'Оберіть ваше місто', reply_markup=cities_markup([city['name'] for city in self.cities]))
            self.bot.register_next_step_handler(self.message, self.workplace_city_processing)
        else:
            self.bot.send_message(self.message.chat.id, 'Помилка сервера')

    def workplace_city_processing(self, message):
        if message.text in [city['name'] for city in self.cities]:
            self.city = self.city_id(message.text)
            self.workplace()
        else:
            self.bot.send_message(self.message.chat.id, 'Некоректне місто')
            self.workplace_city()

    def workplace(self):
        response = get_workplaces_by_city(self.city)
        if response.status_code == 200:
            self.workplaces = response.json()
            self.bot.send_message(self.message.chat.id, 'Оберіть вашу робочу точку', reply_markup=workplaces_markup([workplace['name'] for workplace in self.workplaces]))
            self.bot.register_next_step_handler(self.message, self.workplace_processing)
        else:
            self.bot.send_message(self.message.chat.id, 'Помилка сервера')

    def workplace_processing(self, message):
        if message.text in [workplace['name'] for workplace in self.workplaces]:
            self.results['workplace'] = self.workplace_id(message.text)
            self.result_processing()
        else:
            self.bot.send_message(self.message.chat.id, 'Некоректна робоча точка')
            self.workplace()

    def result_processing(self):
        print(self.results)
        user_id = self.message.chat.id
        if is_employee_exists(user_id):
            response = update_employee(user_id, self.results)
            if response.status_code == 200:
                self.bot.send_message(self.message.chat.id, 'Дані успішно оновлено', reply_markup=types.ReplyKeyboardRemove())
            else:
                self.bot.send_message(self.message.chat.id, 'Помилка сервера, спробуйте ще раз')
                self.start()
        else:
            response = post_employee(self.results)
            if response.status_code == 201:
                self.bot.send_message(self.message.chat.id, 'Дані успішно збережено', reply_markup=types.ReplyKeyboardRemove())
            else:
                self.bot.send_message(self.message.chat.id, 'Помилка сервера, спробуйте ще раз')
                self.start()


class ServicePoll():
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message
        self.telegram_id = message.chat.id
        self.client_data = None
        self.services = None
        self.results = {
            'employee': self.telegram_id,
            'client': None,
            'serviceType': None,
            'warranty': None,
            'nomenclature': None,
            'time_gap1': 120,
            'time_gap2': 240,
        }

    def start(self):
        self.client()

    def client(self):
        self.bot.send_message(self.message.chat.id, 'Введіть номер телефону клієнта', reply_markup=types.ReplyKeyboardRemove())
        self.bot.register_next_step_handler(self.message, self.client_processing)

    def client_processing(self, message):
        response = get_client_by_number(message.text)
        if response.status_code == 200:
            self.client_data = response.json()[0]
            self.client_approval()
        else:
            self.bot.send_message(self.message.chat.id, 'Клієнт не знайдений', reply_markup=types.ReplyKeyboardRemove())
            self.client()

    def client_approval(self):
        self.bot.send_message(self.message.chat.id, f'Клієнт: {self.client_data["first_name"]} {self.client_data["last_name"]}\n Номер телефону: {self.client_data["phone"]}. Підтвердити?', reply_markup=yesno_markup())
        self.bot.register_next_step_handler(self.message, self.client_approval_processing)

    def client_approval_processing(self, message):
        if message.text == 'Так':
            self.results['client'] = self.client_data['telegram_id']
            self.service_type()
        elif message.text == 'Ні':
            self.bot.send_message(self.message.chat.id, 'Заповніть дані заново', reply_markup=types.ReplyKeyboardRemove())
            self.client()
        else:
            self.bot.send_message(self.message.chat.id, 'Некоректний ввід', reply_markup=yesno_markup())
            self.client_approval()

    def service_type(self):
        self.bot.send_message(self.message.chat.id, 'Введіть тип послуги', reply_markup=services_markup())
        self.bot.register_next_step_handler(self.message, self.service_type_processing)

    def service_type_processing(self, message):
        if message.text == "Покупка" or message.text == "Покупка(франшиза)":
            self.results['serviceType'] = message.text
            self.buy()
        elif message.text == "Повернення":
            self.results['serviceType'] = message.text
            self.nomenclature()
        elif message.text == "Ремонт":
            self.results['serviceType'] = message.text
            self.repair()
        else:
            self.bot.send_message(self.message.chat.id, 'Некоректний ввід', reply_markup=services_markup())
            self.service_type()

    def buy(self):
        self.bot.send_message(self.message.chat.id, 'Введіть спосіб оплати', reply_markup=payment_markup())
        self.bot.register_next_step_handler(self.message, self.buy_processing)

    def buy_processing(self, message):
        self.results['payment'] = message.text
        self.nomenclature()

    def time_gap2(self):
        self.bot.send_message(self.message.chat.id, 'Введіть час до відправлення опитування про використання пристрою?(в секундах)', reply_markup=types.ReplyKeyboardRemove())
        self.bot.register_next_step_handler(self.message, self.time_gap2_processing)

    def time_gap2_processing(self, message):
        if message.text.isdigit():
            self.results['time_gap2'] = message.text
            self.time_gap1()
        else:
            self.bot.send_message(self.message.chat.id, 'Некоректний ввід', reply_markup=types.ReplyKeyboardRemove())
            self.time_gap2()

    def repair(self):
        self.bot.send_message(self.message.chat.id, 'Оберіть чи був це гарантійний ремонт', reply_markup=yesno_markup())
        self.bot.register_next_step_handler(self.message, self.repair_processing)

    def repair_processing(self, message):
        if message.text == 'Так':
            self.results['warranty'] = True
            self.nomenclature()
        elif message.text == 'Ні':
            self.results['warranty'] = False
            self.repair_payment()
        else:
            self.bot.send_message(self.message.chat.id, 'Некоректний ввід', reply_markup=yesno_markup())
            self.repair()

    def repair_payment(self):
        self.bot.send_message(self.message.chat.id, 'Введіть спосіб оплати', reply_markup=payment_markup())
        self.bot.register_next_step_handler(self.message, self.repair_payment_processing)

    def repair_payment_processing(self, message):
        self.results['payment'] = message.text
        self.nomenclature()
    def time_gap1(self):
        self.bot.send_message(self.message.chat.id, 'Введіть час до відправлення опитування?(в секундах)', reply_markup=types.ReplyKeyboardRemove())
        self.bot.register_next_step_handler(self.message, self.time_gap1_processing)

    def time_gap1_processing(self, message):
        if message.text.isdigit():
            self.results['time_gap1'] = message.text
            self.nomenclature()
        else:
            self.bot.send_message(self.message.chat.id, 'Некоректний ввід', reply_markup=types.ReplyKeyboardRemove())
            self.time_gap1()

    def nomenclature(self):
        self.bot.send_message(self.message.chat.id, 'Введіть частину назви цільової номенклатури', reply_markup=types.ReplyKeyboardRemove())
        self.bot.register_next_step_handler(self.message, self.nomenclature_processing)

    def nomenclature_processing(self, message):
        response = get_nomenclature_by_name_part(message.text)
        if response.status_code == 200:
            nomenclatures = response.json()
            if len(nomenclatures) == 0:
                self.bot.send_message(self.message.chat.id, 'Номенклатура не знайдена, спробуйте ще раз')
                self.nomenclature()
            else:
                self.bot.send_message(self.message.chat.id, 'Оберіть номенклатуру', reply_markup=nomeclature_markup(nomenclatures))
                self.bot.register_next_step_handler(self.message, self.nomenclature_processing2)
        else:
            self.bot.send_message(self.message.chat.id, 'Помилка сервера, спробуйте ще раз')
            self.nomenclature()

    def nomenclature_processing2(self, message):
        self.results['nomenclature'] = message.text.split('.')[0]
        self.result_processing()

    def result_processing(self):
        print(self.results)
        response = post_service(self.results)
        if response.status_code == 201:
            self.bot.send_message(self.message.chat.id, 'Послуга успішно збережена', reply_markup=types.ReplyKeyboardRemove())
        else:
            self.bot.send_message(self.message.chat.id, 'Помилка сервера, спробуйте ще раз', reply_markup=types.ReplyKeyboardRemove())
            self.start()



