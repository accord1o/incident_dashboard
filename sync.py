from models import Incident, db
from datetime import datetime
import naumen2

def fetch_incidents_from_service_desk():
    # Заглушка с данными как на скриншоте
    return [
        {
            "external_id": "INC001",
            "problem_summary": "Частичное замедление выпуска Пушкинских карт",
            "detection_time": "2025-06-17T08:15:00",
            "affected_systems": "ДБО: Пушкинская карта",
            "detection_method": "Ситуационный центр",
            "category": 3,
            "responsible": "Волосок Кирилл Геннадьевич",
            "technical_details": "Наблюдается частичное замедление выпуска Пушкинских карт и заявок на изменение ПДн в связи с увеличением времени ответа от МВД при проверке клиентских данных (задержка более 30 мин).",
            "attachments": "печатная форма запроса 4882669.pdf"
        },
        {
            "external_id": "INC002",
            "problem_summary": "Снижение производительности CRM системы",
            "detection_time": "2025-06-16T14:30:00",
            "affected_systems": "CRM система",
            "detection_method": "Мониторинг",
            "category": 2,
            "responsible": "Петров Иван Сергеевич",
            "technical_details": "Заметное снижение производительности CRM системы в часы пиковой нагрузки, время отклика увеличилось в 3 раза по сравнению с нормальными показателями.",
            "attachments": "отчет_производительность.pdf"
        },
        {
            "external_id": "INC003",
            "problem_summary": "Ошибка валидации данных в мобильном приложении",
            "detection_time": "2025-06-15T11:20:00",
            "affected_systems": "Мобильное приложение",
            "detection_method": "Обратная связь",
            "category": 4,
            "responsible": "Смирнова Ольга Васильевна",
            "technical_details": "При вводе данных в некоторых формах мобильного приложения возникала ошибка валидации. Проблема была устранена в течение 2 часов.",
            "attachments": "отчет_исправление.pdf"
        }
    ]


def sync_incidents():
    #incidents_data = fetch_incidents_from_service_desk()
    incidents_data = naumen2.get_response_list()
    new_count = 0
    update_count = 0

    for data in incidents_data:
        incident = Incident.query.filter_by(external_id=data['external_id']).first()

        if not incident:
            # Создаем новую аварию
            incident = Incident(
                external_id=data['external_id'],
                problem_summary=data['problem_summary'],
                detection_time=datetime.fromisoformat(data['detection_time']),
                affected_systems=data['affected_systems'],
                detection_method=data['detection_method'],
                category=data['category'],
                responsible=data['responsible'],
                #technical_details=data['technical_details'],
                #attachments=data['attachments'],
                status='new'
            )
            db.session.add(incident)
            new_count += 1
        else:
            # Обновляем существующую аварию
            #incident.problem_summary = data['problem_summary']
            #incident.technical_details = data['technical_details']
            # Можно обновить и другие поля, если нужно
            update_count += 1

    db.session.commit()
    print(f"Синхронизировано: добавлено {new_count}, обновлено {update_count} аварий")