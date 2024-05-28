import re


def mail_is_correct(mail):
    return re.match(r"[^@]+@[^@]+\.[^@]+", mail) is not None


def is_phone_correct(phone):
    return phone.isdigit() and len(phone) == 10
