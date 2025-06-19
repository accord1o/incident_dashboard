from flask import Flask, render_template, jsonify, request
from database import db, init_db
from models import Incident
import datetime
from sync import sync_incidents

app = Flask(__name__)
init_db(app)

# Создаем базу данных и выполняем синхронизацию при запуске
with app.app_context():
    db.create_all()
    # Проверяем, есть ли уже данные в базе
    if Incident.query.count() == 0:
        print("Выполняем начальную синхронизацию...")
        sync_incidents()


@app.route('/')
def main_dashboard():
    return render_template('dashboard.html', now=datetime.datetime.now())


# API для получения списка аварий
@app.route('/api/incidents')
def get_incidents():
    incidents = Incident.query.all()
    return jsonify([incident.to_dict() for incident in incidents])


# API для подтверждения аварии
@app.route('/api/incidents/<int:id>/confirm', methods=['POST'])
def confirm_incident(id):
    incident = Incident.query.get(id)
    if incident:
        incident.status = 'confirmed'
        incident.reviewed_by = request.json.get('reviewed_by', 'Система')
        incident.review_comment = request.json.get('comment', '')
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Incident not found'}), 404



# API для отклонения аварии
@app.route('/api/incidents/<int:id>/reject', methods=['POST'])
def reject_incident(id):
    incident = Incident.query.get(id)
    if incident:
        incident.status = 'rejected'
        incident.reviewed_by = request.json.get('reviewed_by', 'Система')
        incident.review_comment = request.json.get('comment', '')
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Incident not found'}), 404


# API для изменения категории
@app.route('/api/incidents/<int:id>/category', methods=['POST'])
def update_category(id):
    incident = Incident.query.get(id)
    if incident:
        new_category = request.json.get('category')
        if new_category in [1, 2, 3, 4, 5]:
            incident.category = new_category
            db.session.commit()
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error', 'message': 'Invalid category'}), 400
    return jsonify({'status': 'error', 'message': 'Incident not found'}), 404


# API для создания аварийной комнаты
@app.route('/api/incidents/<int:id>/war_room', methods=['POST'])
def create_war_room(id):
    incident = Incident.query.get(id)
    if incident:
        incident.war_room_url = f"https://meet.jit.si/incident-{id}-{datetime.datetime.now().strftime('%Y%m%d')}"
        db.session.commit()
        return jsonify({'status': 'success', 'url': incident.war_room_url})
    return jsonify({'status': 'error', 'message': 'Incident not found'}), 404


# API для закрытия аварии
@app.route('/api/incidents/<int:id>/close', methods=['POST'])
def close_incident(id):
    incident = Incident.query.get(id)
    if incident:
        incident.status = 'closed'
        incident.closed_at = datetime.datetime.now()
        incident.root_cause = request.json.get('root_cause', '')
        incident.solution = request.json.get('solution', '')
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Incident not found'}), 404


# API для синхронизации
@app.route('/api/sync', methods=['POST'])
def sync_incidents_api():
    try:
        sync_incidents()
        return jsonify({"success": True, "message": "Синхронизация выполнена успешно"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# API для оповещения бизнеса
@app.route('/api/incidents/<int:id>/notify', methods=['POST'])
def notify_business(id):
    incident = Incident.query.get(id)
    if incident:
        # Здесь должна быть реальная логика отправки уведомлений
        print(f"Оповещение бизнеса о аварии ID: {id}")
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Incident not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        incidents = Incident.query.all()
        print(f"В базе {len(incidents)} аварий:")
        for incident in incidents:
            print(f"- {incident.problem_summary} (ID: {incident.id})")

    app.run(debug=True, port=5000)