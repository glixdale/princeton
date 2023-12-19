from flask import request,render_template,redirect, Blueprint, jsonify
from database import db
from Models.Property import Property

bp = Blueprint('property',__name__)
@bp.route("/", methods=['POST', 'GET'])
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
    
#TODO: api global error handler
@bp.route('/api/properties', methods=['POST', 'GET'])
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

@bp.route('/api/properties/<int:id>', methods=["GET","DELETE","PUT"])
def delete(id):
    if request.method == 'DELETE':
        try:
            property = Property.query.get(id)
            db.session.delete(property)
            db.session.commit()
            return {'message' : f'Property {id} deleted'}
        except:
            return {'message':f'Unable to delete property with id:{id}'}
    elif request.method == 'GET':
        try:
            return Property.query.get(id).as_dict()
        except:
            return {'message':f'Unable to find a property with id:{id}'}
    elif request.method == 'PUT':
        try:
            property = Property.query.get(id)
            property_data = request.get_json(force=True)
            property.set_from_dict(property_data)
            db.session.commit()
            return property.query.get(id).as_dict()
        except:
            return {'message':f'Unable to update a property with id:{id}'}