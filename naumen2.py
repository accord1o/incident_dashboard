# --coding:utf8--
import json
import requests
import urllib3
import time
import configparser
import base64
from dotenv import load_dotenv
import os
from datetime import datetime

#убрать и вернуть на место обычные API запросы
import cloudscraper
scraper = cloudscraper.create_scraper()


load_dotenv()  # Загружает переменные из .env
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
TOKEN_SD = os.getenv("TOKEN_SD")


def get_list_service_call():
    url = f"https://sd.pochtabank.ru/sd/services/rest/exec?accessKey={TOKEN_SD}&func=modules.sdRest.listServiceCalls&params=user"
    payload = {}
    response = scraper.get(url)
    object_json = json.loads(response.text)
    return object_json

def get_json_object(UUID):
    url = f"https://sd.pochtabank.ru/sd/services/rest/get/{UUID}?accessKey={TOKEN_SD}"
    payload = ""
    headers = {
         'Cookie': 'JSESSIONID=7746F0F8216D69C80B7D3B6CECA568AD'
     }
    response = scraper.get(url)
    object_json = json.loads(response.text)
    return object_json

#Функция получения cписка UUID обязательных полей
def get_UUID_fields_list(serviceCall_json):
  l = []
  data = serviceCall_json['totalValue']
  for i in data:
    UUID = i['UUID']
    l.append(UUID)
  return l

#Функция получения названий обязательных полей
def get_name_fields_list(serviceCall_json):
  l = []
  data = serviceCall_json['totalValue']
  for i in data:
    name = i['title']
    l.append(name)
  return l

#Функция получения списка содержания обязательных полей
def get_textValue_list(UUID_fields_list):
  l = []
  for UUID_fields in UUID_fields_list:
    UUID_fields_json = get_json_object(UUID_fields)
    data = UUID_fields_json['textValue']
    l.append(data)
  return l

#Получить словарь обязательных полей
def get_fields_dict(serviceCall_json):
    UUID_fields_list = get_UUID_fields_list(serviceCall_json)
    textValue_list = get_textValue_list(UUID_fields_list)
    textName_list = get_name_fields_list(serviceCall_json)
    fields_dict = dict(zip(textName_list, textValue_list))
    return fields_dict

##### Функция принятия в работу ######
def take_to_work(serviceCall_UUID):
    url = f"https://sd.pochtabank.ru/sd/services/rest/exec?accessKey={TOKEN_SD}&func=modules.sdRest.markServiceCall&params={serviceCall_UUID},user"
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'JSESSIONID=EDE357B4E87668E59C0C314A7959ED44'
    }
    scraper.get(url)

def next_line(serviceCall_UUID):
    take_to_work(serviceCall_UUID)
    time.sleep(30)
    url = f"https://sd.pochtabank.ru/sd/services/rest/exec?accessKey={TOKEN_SD}&func=modules.sdRestV2.routeServiceCall&params={serviceCall_UUID},'Обращение обработано автоматически, Коллеги, просьба обработать обращение',user,false"
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'JSESSIONID=EDE357B4E87668E59C0C314A7959ED44'
    }
    scraper.get(url)

########## Функция выполнения обращений ##########
def close_ticket(serviceCall_UUID, solution):
    take_to_work(serviceCall_UUID)
    attributs  = {"state":"resolved","procCodeClose":"catalogs$22736","solution":solution}
    url = 'https://sd.pochtabank.ru/sd/services/rest/edit/serviceCall$' + str(serviceCall_UUID) + '/' + str(attributs) + f'?accessKey={TOKEN_SD}'
    payload = ""
    headers = \
        {
            'Cookie': 'JSESSIONID=7746F0F8216D69C80B7D3B6CECA568AD'
        }
    scraper.get(url)

def get_response_list():
    response_list = []
    list_service_call = get_list_service_call()
    for element in list_service_call:
        result_dict = {}
        servicecall_json = get_json_object(element['uuid'])
        fields_dict = get_fields_dict(servicecall_json)
        result_dict['external_id'] = element['uuid']
        result_dict['problem_summary'] = fields_dict['Краткая суть проблемы']
        detection_time = fields_dict['Время фактического обнаружения аварии']
        date_str = "19.06.2025 14:46"
        # Парсим строку в объект datetime
        datetime_obj = datetime.strptime(detection_time, "%d.%m.%Y %H:%M")
        # Преобразуем в ISO 8601
        iso_format = datetime_obj.isoformat()
        result_dict['detection_time'] = iso_format
        result_dict['affected_systems'] = fields_dict['Затронутые системы']
        result_dict['detection_method'] = fields_dict['Способ обнаружения']
        result_dict['category'] = fields_dict['Категория аварии']
        result_dict['responsible'] = fields_dict['Ответственные за сервис']
        response_list.append(result_dict)
    return response_list

