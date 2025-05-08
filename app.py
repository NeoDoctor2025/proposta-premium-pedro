from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os
import logging
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize database classes
class Base(DeclarativeBase):
    pass

# Create SQLAlchemy instance
db = SQLAlchemy(model_class=Base)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "neo-doctor-default-key")

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize SQLAlchemy with app
db.init_app(app)

# Import models and create tables
with app.app_context():
    import models
    db.create_all()
    
# Import admin routes
import admin  # noqa: F401

@app.route('/')
def index():
    # Pass the current year to the template for copyright notice
    current_year = datetime.now().year
    return render_template('index.html', current_year=current_year)

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        specialty = request.form.get('specialty')
        message = request.form.get('message')
        
        # Validate required fields
        if not name or not email or not phone or not message:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('index', _anchor='contact'))
        
        # Log the form submission
        logging.info(f"Contact form submission: {name} ({email})")
        
        # Create new contact record in database
        new_contact = models.Contact()
        new_contact.name = name
        new_contact.email = email
        new_contact.phone = phone
        new_contact.specialty = specialty
        new_contact.message = message
        db.session.add(new_contact)
        db.session.commit()
        
        # Prepare email content
        email_content = f"""
        <h2>Nova mensagem de contato do site Neo Doctor</h2>
        <p><strong>Nome:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Telefone:</strong> {phone}</p>
        <p><strong>Especialidade:</strong> {specialty or 'Não informado'}</p>
        <p><strong>Mensagem:</strong></p>
        <p>{message}</p>
        """
        
        # Try to send email notification
        try:
            send_email(
                recipient='contato@neodoctor.com.br',
                subject='Nova mensagem de contato - Neo Doctor',
                body=email_content
            )
        except Exception as email_err:
            logging.error(f"Failed to send email notification: {str(email_err)}")
            # The contact is saved in the database, so we continue despite email error
        
        # If this is an AJAX request, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': 'Mensagem enviada com sucesso!'
            })
        
        # For traditional form submission
        flash('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success')
        return redirect(url_for('index', _anchor='contact'))
        
    except Exception as e:
        logging.error(f"Error in contact form: {str(e)}")
        
        # If this is an AJAX request, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'message': 'Ocorreu um erro ao enviar sua mensagem. Por favor, tente novamente.'
            })
        
        # For traditional form submission
        flash('Ocorreu um erro ao enviar sua mensagem. Por favor, tente novamente.', 'danger')
        return redirect(url_for('index', _anchor='contact'))

def send_email(recipient, subject, body):
    """
    Helper function to send emails.
    In a production environment, you would configure this with your SMTP server.
    """
    try:
        # Get email credentials from environment variables
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.example.com')
        smtp_port = int(os.environ.get('SMTP_PORT', 587))
        smtp_username = os.environ.get('SMTP_USERNAME', '')
        smtp_password = os.environ.get('SMTP_PASSWORD', '')
        sender_email = os.environ.get('SENDER_EMAIL', 'noreply@neodoctor.com.br')
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient
        
        # Add HTML content
        msg.attach(MIMEText(body, 'html'))
        
        # Connect to SMTP server and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        logging.error(f"Email sending error: {str(e)}")
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
