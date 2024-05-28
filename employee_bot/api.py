from requests import post, get, put

def base_url():
    return 'http://127.0.0.1:8000/api/'


def get_client_by_number(phone):
    url = f'{base_url()}clients/?phone={phone}'
    response = get(url)
    return response

def post_service(data):
    url = f'{base_url()}services/'
    response = post(url, data=data)
    return response

def is_employee_exists(telegram_id):
    url = f'{base_url()}employees/{telegram_id}/'
    response = get(url)
    return response.status_code == 200


def post_employee(data):
    url = f'{base_url()}employees/'
    response = post(url, data=data)
    return response

def update_employee(telegram_id, data):
    url = f'{base_url()}employees/{telegram_id}/'
    response = put(url, data=data)
    return response

def get_workplaces():
    url = f'{base_url()}workplaces/'
    response = get(url)
    return response


def get_regions_with_workplaces():
    url = f'{base_url()}regions_with_workplaces/'
    response = get(url)
    return response


def get_cities_with_workplaces(region):
    url = f'{base_url()}cities_with_workplaces/?region={region}'
    response = get(url)
    return response


def get_workplaces_by_city(city):
    url = f'{base_url()}workplaces/?city={city}'
    response = get(url)
    return response


def get_regions_list():
    url = f'{base_url()}regions/'
    response = get(url)
    if response.status_code == 200:
        data = response.json()
        cities = []
        for city in data:
            cities.append(city['name'])
        return cities
    return []


def get_cities_list(region_id):
    url = f'{base_url()}cities/?region={region_id}'
    response = get(url)
    if response.status_code == 200:
        data = response.json()
        cities = []
        for city in data:
            cities.append(city['name'])
        return cities
    return []


def get_city_id(city_name):
    url = f'{base_url()}cities_name/{city_name}'
    response = get(url)
    if response.status_code == 200:
        data = response.json()
        return data['id']
    return None


def get_region_id(region_name):
    url = f'{base_url()}regions_name/{region_name}'
    response = get(url)
    if response.status_code == 200:
        data = response.json()
        return data['id']
    return None


def get_city_name(city_id):
    url = f'{base_url()}cities/{city_id}'
    response = get(url)
    if response.status_code == 200:
        data = response.json()
        return data['name']
    return None


def get_region_name(region_id):
    url = f'{base_url()}regions/{region_id}'
    response = get(url)
    if response.status_code == 200:
        data = response.json()
        return data['name']
    return None


def create_monthly_poll():
    url = f'{base_url()}monthly_polls/'
    response = get(url)
    return response


def get_nomenclature_by_name_part(name_part):
    url = f'{base_url()}nomenclature/?name_part={name_part}'
    response = get(url)
    return response