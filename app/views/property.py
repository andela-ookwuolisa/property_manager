from flask import request, render_template, redirect, session, url_for
from app import my_app, db
from app.models.user import User, Owner, Tenant
from app.models.property import Property

@my_app.route('/properties', methods=['GET', 'POST'])
def properties():
    properties = db.query(Property)
    if request.method == 'GET':
        return render_template('property.html', properties = properties)

    elif request.method == 'POST':
        property_ = Property(
            property_type = request.form.get('property_type'),
            owner_id = request.form.get('owner_id')
        )
        db.add(property_)
        db.commit()
        return render_template('property.html', properties = properties)

@my_app.route('/update', methods=['POST'])
def update():
    property_ = db.query(Property).filter(
        Property.id == request.form.get('id')
    ).first()
    if request.form.get('property_type'):
        property_.property_type = request.form.get('property_type')
    if request.form.get('owner_id'):
        property_.property_type = request.form.get('owner_id')
        
    db.add(property_)
    db.commit()
    return redirect(url_for('properties'))

@my_app.route('/delete', methods=['POST'])
def delete():
    print('hello '*7)
    property_ = db.query(Property).filter(
        Property.id == request.form.get('id')
    ).first()
    db.delete(property_)
    return redirect(url_for('properties'))

        
