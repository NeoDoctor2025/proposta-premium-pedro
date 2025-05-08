from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from app import db

class Contact(db.Model):
    """
    Modelo para armazenar contatos/leads que preencheram o formulário
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    specialty = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='new')  # new, contacted, qualified, converted
    
    def __repr__(self):
        return f'<Contact {self.name} ({self.email})>'

class Newsletter(db.Model):
    """
    Modelo para armazenar assinantes da newsletter
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Newsletter {self.email}>'

class Testimonial(db.Model):
    """
    Modelo para armazenar depoimentos de clientes
    """
    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    stars = db.Column(db.Integer, default=5)  # Avaliação de 1 a 5
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Testimonial {self.doctor_name}>'

class Event(db.Model):
    """
    Modelo para armazenar eventos como webinars, workshops, etc.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    registration_link = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Event {self.title}>'