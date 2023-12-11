from flask import Flask, render_template, url_for, request, redirect, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id
    

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    Street_Number = db.Column(db.Integer, nullable=False)
    Street_Name = db.Column(db.String(200), nullable=False)
    Address_Line_2 = db.Column(db.String(200), nullable=False)
    City = db.Column(db.String(200), nullable=False)
    Zip = db.Column(db.Integer, nullable=False)
    State = db.Column(db.String(2), nullable=False)
    Phone = db.Column(db.String(10), nullable=False)
    Phone2 = db.Column(db.String(10), nullable=True)
    Phone3 = db.Column(db.String(10), nullable=True)
    Fax = db.Column(db.String(10), nullable=True)
    def __repr__(self):
        return '<Task %r>' % self.id
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        Prop_Name = request.form['Name']
        Prop_Street_Number = request.form['Street_Number']
        Prop_Street_Name = request.form['Street_Name']
        Prop_Address_Line_2 = request.form['Address_Line_2']
        Prop_City = request.form['City']
        Prop_Zip = request.form['Zip']
        Prop_State = request.form['State']
        Prop_Phone = request.form['Phone']
        Prop_Phone2 = request.form['Phone2']
        Prop_Phone3 = request.form['Phone3']
        Prop_Fax = request.form['Fax']
        New_Property = Property(Name=Prop_Name, Street_Number=Prop_Street_Number,
                                     Street_Name=Prop_Street_Name, Address_Line_2=Prop_Address_Line_2,
                                     City=Prop_City, State=Prop_State, Phone=Prop_Phone, Zip=Prop_Zip,
                                     Phone2=Prop_Phone2, Phone3=Prop_Phone3, Fax=Prop_Fax)

        try:
            db.session.add(New_Property)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your property'
    else:
        return render_template('index.html')
    
    
@app.route('/api/properties')
def properties():
    Properties = Property.query.order_by(Property.date_created).all()

    json_properties = []
    for property in Properties:
        json_properties.append(property.as_dict())

    return json_properties


from flask import request, jsonify

@app.route('/api/addproperties', methods=['POST', 'GET'])
def create_property():
    if request.method == 'POST':
        name = request.json['Name']
        street_number = request.json['Street_Number']
        street_name = request.json['Street_Name']
        address_line_2 = request.json['Address_Line_2']
        city = request.json['City']
        zip_code = request.json['Zip']
        state = request.json['State']
        phone = request.json['Phone']
        phone2 = request.json['Phone2']
        phone3 = request.json['Phone3']
        fax = request.json['Fax']

        # Creating a new Property object
        new_property = Property(
            Name=name,
            Street_Number=street_number,
            Street_Name=street_name,
            Address_Line_2=address_line_2,
            City=city,
            Zip=zip_code,
            State=state,
            Phone=phone,
            Phone2=phone2,
            Phone3=phone3,
            Fax=fax
        )

        # Adding the new property to the database session
        db.session.add(new_property)
        db.session.commit()

        return jsonify({'message': 'Property created successfully!'}), 201  # Return success message with HTTP status code 201
    else:
        return jsonify({'error': 'Method not allowed'}), 405  # Return error for unsupported methods


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect ('/')
    except:
        return 'There was a problem deleting that task'
    
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)
    

if __name__=="__main__":
    app.run(debug=True)