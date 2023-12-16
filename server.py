from flask import Flask, render_template, url_for, request, redirect, json, request, jsonify
from app import db,app
from Models.Property import Property
from faker import Faker
import random
from datetime import datetime
import sys
    
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        request_data = dict(request.form)

        new_property = Property()
        new_property.set_from_dict(request_data)

        try:
            db.session.add(new_property)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your property'
    else:
        return render_template('index.html')
        
@app.route('/api/properties', methods=['POST', 'GET'])
def create_property():
    if request.method == 'POST':
        property = Property()
        property_data = request.get_json(force=True)
        property.set_from_dict(property_data)

        # Adding the new property to the database session
        db.session.add(property)
        db.session.commit()

        return jsonify({'message': f'Property {property.name} created successfully!'}), 201  # Return success message with HTTP status code 201
    else:

        filter_params = request.args.to_dict()

        if filter_params:
            query = Property.query
            for key, value in filter_params.items():
                # Use filter_by to add conditions dynamically
                query = query.filter_by(**{key: value})
                query = query.order_by(Property.date_created)
            # Execute the query and get the list of properties
            properties = query.all()
            
        else:
            properties = Property.query.order_by(Property.date_created).all()    
        return [property.as_dict() for property in properties] or {'message' : f"No results found for {filter_params.__str__().replace('{', '').replace('}', '')}"}

@app.route('/api/properties/<int:id>', methods=["GET","DELETE","PUT"])
def delete(id):
    if request.method == 'DELETE':
        try:
            property = Property.query.filter_by(id=id).first()
            db.session.delete(property)
            db.session.commit()
            return {'message' : f'Property {id} deleted'}
        except:
            return {'message':f'Unable to delete property with id:{id}'}
    elif request.method == 'GET':
        try:
            return Property.query.filter_by(id=id).one().as_dict()
        except:
            return {'message':f'Unable to find a property with id:{id}'}
    elif request.method == 'PUT':
        try:
            property = Property.query.filter_by(id=id).first()
            property_data = request.get_json(force=True)
            property.set_from_dict(property_data)
            db.session.commit()
            return property.query.filter_by(id=id).one().as_dict()
        except:
            return {'message':f'Unable to update a property with id:{id}'}    

def generate_random_property():
    fake = Faker()

    return Property(
        name=fake.company(),
        date_created=datetime.utcnow(),
        street_number=fake.building_number(),
        street_name=fake.street_name(),
        address_line_2=fake.secondary_address(),
        city=fake.city(),
        zip=fake.zipcode(),
        state=fake.state_abbr(),
        phone=fake.phone_number(),
        phone2=fake.phone_number() if random.choice([True, False]) else None,
        phone3=fake.phone_number() if random.choice([True, False]) else None,
        fax=fake.phone_number() if random.choice([True, False]) else None
    )

# Seed the database with a specified number of random properties
def seed_database(num_properties):
    for _ in range(num_properties):
        random_property = generate_random_property()
        db.session.add(random_property)

    db.session.commit()

        
if __name__=="__main__":
        # Set the number of properties you want to generate and seed
    num_properties_to_seed = 100

    # Create tables if they do not exist
    with app.app_context():
        db.create_all()

    # Seed the database with random properties
    if Property.query.first() is None:
        seed_database(num_properties_to_seed)
    app.run(host='0.0.0.0',port=8000,debug=True)