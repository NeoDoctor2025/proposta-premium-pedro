from app import app, db
from models import Contact, Newsletter, Testimonial, Event
from flask import render_template, redirect, url_for, flash, request
import logging
from datetime import datetime

# Route for admin dashboard
@app.route('/admin')
def admin_dashboard():
    # Get counts for dashboard stats
    contact_count = Contact.query.count()
    newsletter_count = Newsletter.query.count()
    testimonial_count = Testimonial.query.count()
    event_count = Event.query.count()
    
    # Get recent contacts
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    
    return render_template(
        'admin/dashboard.html', 
        contact_count=contact_count,
        newsletter_count=newsletter_count,
        testimonial_count=testimonial_count,
        event_count=event_count,
        recent_contacts=recent_contacts
    )

# Route for contacts list
@app.route('/admin/contacts')
def admin_contacts():
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/contacts.html', contacts=contacts)

# Route for contact details
@app.route('/admin/contacts/<int:contact_id>')
def admin_contact_detail(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return render_template('admin/contact_detail.html', contact=contact)

# Route for updating contact status
@app.route('/admin/contacts/<int:contact_id>/update_status', methods=['POST'])
def admin_update_contact_status(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    new_status = request.form.get('status')
    
    if new_status in ['new', 'contacted', 'qualified', 'converted']:
        contact.status = new_status
        db.session.commit()
        flash('Status atualizado com sucesso!', 'success')
    else:
        flash('Status inválido!', 'danger')
        
    return redirect(url_for('admin_contact_detail', contact_id=contact_id))

# Route for testimonials list
@app.route('/admin/testimonials')
def admin_testimonials():
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials.html', testimonials=testimonials)

# Route for adding new testimonial
@app.route('/admin/testimonials/add', methods=['GET', 'POST'])
def admin_add_testimonial():
    if request.method == 'POST':
        doctor_name = request.form.get('doctor_name')
        specialty = request.form.get('specialty')
        content = request.form.get('content')
        image_url = request.form.get('image_url')
        stars = request.form.get('stars')
        is_featured = 'is_featured' in request.form
        
        if not doctor_name or not specialty or not content:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
        else:
            try:
                new_testimonial = Testimonial()
                new_testimonial.doctor_name = doctor_name
                new_testimonial.specialty = specialty
                new_testimonial.content = content
                new_testimonial.image_url = image_url
                new_testimonial.stars = int(stars) if stars else 5
                new_testimonial.is_featured = is_featured
                db.session.add(new_testimonial)
                db.session.commit()
                flash('Depoimento adicionado com sucesso!', 'success')
                return redirect(url_for('admin_testimonials'))
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error adding testimonial: {str(e)}")
                flash('Ocorreu um erro ao adicionar o depoimento.', 'danger')
    
    return render_template('admin/testimonial_form.html')

# Route for editing testimonial
@app.route('/admin/testimonials/edit/<int:testimonial_id>', methods=['GET', 'POST'])
def admin_edit_testimonial(testimonial_id):
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    
    if request.method == 'POST':
        doctor_name = request.form.get('doctor_name')
        specialty = request.form.get('specialty')
        content = request.form.get('content')
        image_url = request.form.get('image_url')
        stars = request.form.get('stars')
        is_featured = 'is_featured' in request.form
        
        if not doctor_name or not specialty or not content:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
        else:
            try:
                testimonial.doctor_name = doctor_name
                testimonial.specialty = specialty
                testimonial.content = content
                testimonial.image_url = image_url
                testimonial.stars = int(stars) if stars else 5
                testimonial.is_featured = is_featured
                
                db.session.commit()
                flash('Depoimento atualizado com sucesso!', 'success')
                return redirect(url_for('admin_testimonials'))
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error updating testimonial: {str(e)}")
                flash('Ocorreu um erro ao atualizar o depoimento.', 'danger')
    
    return render_template('admin/testimonial_form.html', testimonial=testimonial)

# Route for deleting testimonial
@app.route('/admin/testimonials/delete/<int:testimonial_id>', methods=['POST'])
def admin_delete_testimonial(testimonial_id):
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    
    try:
        db.session.delete(testimonial)
        db.session.commit()
        flash('Depoimento excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting testimonial: {str(e)}")
        flash('Ocorreu um erro ao excluir o depoimento.', 'danger')
    
    return redirect(url_for('admin_testimonials'))

# Route for events list
@app.route('/admin/events')
def admin_events():
    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template('admin/events.html', events=events)

# Route for adding new event
@app.route('/admin/events/add', methods=['GET', 'POST'])
def admin_add_event():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        event_date_str = request.form.get('event_date')
        registration_link = request.form.get('registration_link')
        is_active = 'is_active' in request.form
        
        if not title or not description or not event_date_str:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
        else:
            try:
                # Parse date string to datetime object
                event_date = datetime.strptime(event_date_str, '%Y-%m-%dT%H:%M')
                
                new_event = Event()
                new_event.title = title
                new_event.description = description
                new_event.event_date = event_date
                new_event.registration_link = registration_link
                new_event.is_active = is_active
                db.session.add(new_event)
                db.session.commit()
                flash('Evento adicionado com sucesso!', 'success')
                return redirect(url_for('admin_events'))
            except ValueError:
                flash('Formato de data inválido.', 'danger')
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error adding event: {str(e)}")
                flash('Ocorreu um erro ao adicionar o evento.', 'danger')
    
    return render_template('admin/event_form.html')

# Route for editing event
@app.route('/admin/events/edit/<int:event_id>', methods=['GET', 'POST'])
def admin_edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        event_date_str = request.form.get('event_date')
        registration_link = request.form.get('registration_link')
        is_active = 'is_active' in request.form
        
        if not title or not description or not event_date_str:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
        else:
            try:
                # Parse date string to datetime object
                event_date = datetime.strptime(event_date_str, '%Y-%m-%dT%H:%M')
                
                event.title = title
                event.description = description
                event.event_date = event_date
                event.registration_link = registration_link
                event.is_active = is_active
                
                db.session.commit()
                flash('Evento atualizado com sucesso!', 'success')
                return redirect(url_for('admin_events'))
            except ValueError:
                flash('Formato de data inválido.', 'danger')
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error updating event: {str(e)}")
                flash('Ocorreu um erro ao atualizar o evento.', 'danger')
    
    return render_template('admin/event_form.html', event=event)

# Route for deleting event
@app.route('/admin/events/delete/<int:event_id>', methods=['POST'])
def admin_delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    try:
        db.session.delete(event)
        db.session.commit()
        flash('Evento excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting event: {str(e)}")
        flash('Ocorreu um erro ao excluir o evento.', 'danger')
    
    return redirect(url_for('admin_events'))

# Route for newsletter subscribers
@app.route('/admin/newsletter')
def admin_newsletter():
    subscribers = Newsletter.query.order_by(Newsletter.subscribed_at.desc()).all()
    return render_template('admin/newsletter.html', subscribers=subscribers)

# Route for adding newsletter subscriber
@app.route('/admin/newsletter/add', methods=['GET', 'POST'])
def admin_add_subscriber():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        
        if not email:
            flash('O email é obrigatório.', 'danger')
        else:
            existing = Newsletter.query.filter_by(email=email).first()
            
            if existing:
                flash('Este email já está cadastrado na newsletter.', 'warning')
            else:
                try:
                    new_subscriber = Newsletter()
                    new_subscriber.email = email
                    new_subscriber.name = name
                    db.session.add(new_subscriber)
                    db.session.commit()
                    flash('Assinante adicionado com sucesso!', 'success')
                    return redirect(url_for('admin_newsletter'))
                except Exception as e:
                    db.session.rollback()
                    logging.error(f"Error adding subscriber: {str(e)}")
                    flash('Ocorreu um erro ao adicionar o assinante.', 'danger')
    
    return render_template('admin/subscriber_form.html')

# Route for deleting newsletter subscriber
@app.route('/admin/newsletter/delete/<int:subscriber_id>', methods=['POST'])
def admin_delete_subscriber(subscriber_id):
    subscriber = Newsletter.query.get_or_404(subscriber_id)
    
    try:
        db.session.delete(subscriber)
        db.session.commit()
        flash('Assinante excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting subscriber: {str(e)}")
        flash('Ocorreu um erro ao excluir o assinante.', 'danger')
    
    return redirect(url_for('admin_newsletter'))

# Route for toggling newsletter subscriber status
@app.route('/admin/newsletter/toggle/<int:subscriber_id>', methods=['POST'])
def admin_toggle_subscriber(subscriber_id):
    subscriber = Newsletter.query.get_or_404(subscriber_id)
    
    try:
        subscriber.is_active = not subscriber.is_active
        db.session.commit()
        status = "ativado" if subscriber.is_active else "desativado"
        flash(f'Assinante {status} com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error toggling subscriber: {str(e)}")
        flash('Ocorreu um erro ao alterar o status do assinante.', 'danger')
    
    return redirect(url_for('admin_newsletter'))