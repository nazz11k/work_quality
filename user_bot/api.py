from requests import post, get, put


def base_url():
    return 'http://127.0.0.1:8000/api/'


def get_client_data(telegam_id):
    url = f'{base_url()}clients/{telegam_id}/'
    response = get(url)
    return response


def is_client_exists(telegam_id):
    url = f'{base_url()}clients/{telegam_id}/'
    response = get(url)
    return response.status_code == 200


def post_client_data(data):
    url = f'{base_url()}clients/'
    response = post(url, data=data)
    return response


def update_client_data(telegam_id, data):
    url = f'{base_url()}clients/{telegam_id}/'
    response = put(url, data=data)
    return response


def post_FirsClientCheck(data):
    url = f'{base_url()}first_client_checks/'
    response = post(url, data=data)
    return response


def post_CustomerLoyaltyIndex(data):
    url = f'{base_url()}customer_loyalty_indices/'
    response = post(url, data=data)
    return response


def post_CustomerShopFeedback(data):
    url = f'{base_url()}customer_shop_feedbacks/'
    response = post(url, data=data)
    return response

def post_ProductFeedback(data):
    url = f'{base_url()}product_feedbacks/'
    response = post(url, data=data)
    return response

def post_RefundFeedback(data):
    url = f'{base_url()}refund_feedbacks/'
    response = post(url, data=data)
    return response

def post_RepairFeedback(data):
    url = f'{base_url()}repair_feedbacks/'
    response = post(url, data=data)
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


def get_user_name(telegram_id):
    url = f'{base_url()}clients/{telegram_id}/'
    response = get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{data['first_name']} {data['last_name']}"
    return None


def get_services_list(client):
    url = f'{base_url()}services/?client={client}'
    response = get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    return []


def get_nomenclature(id):
    url = f'{base_url()}nomenclature/{id}'
    response = get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    return []