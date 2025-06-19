from database import db
from datetime import datetime

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(50), unique=True, nullable=False)
    problem_summary = db.Column(db.Text, nullable=False)
    detection_time = db.Column(db.DateTime, nullable=False)
    affected_systems = db.Column(db.String(255), nullable=False)
    detection_method = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Integer, nullable=False)
    responsible = db.Column(db.String(100), nullable=False)
    technical_details = db.Column(db.Text)
    attachments = db.Column(db.String(255))
    status = db.Column(db.String(20), default='new')  # new, confirmed, rejected, closed
    war_room_url = db.Column(db.String(255))
    reviewed_by = db.Column(db.String(100))
    review_comment = db.Column(db.Text)
    root_cause = db.Column(db.Text)
    solution = db.Column(db.Text)
    closed_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'external_id': self.external_id,
            'problem_summary': self.problem_summary,
            'detection_time': self.detection_time.isoformat() if self.detection_time else None,
            'affected_systems': self.affected_systems,
            'detection_method': self.detection_method,
            'category': self.category,
            'responsible': self.responsible,
            'technical_details': self.technical_details,
            'attachments': self.attachments,
            'status': self.status,
            'war_room_url': self.war_room_url,
            'reviewed_by': self.reviewed_by,
            'review_comment': self.review_comment,
            'root_cause': self.root_cause,
            'solution': self.solution,
            'closed_at': self.closed_at.isoformat() if self.closed_at else None
        }