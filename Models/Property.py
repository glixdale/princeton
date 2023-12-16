from app import db
from datetime import datetime

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    street_number = db.Column(db.Integer, nullable=False)
    street_name = db.Column(db.String(200), nullable=False)
    address_line_2 = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(200), nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(2), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    phone2 = db.Column(db.String(10), nullable=True)
    phone3 = db.Column(db.String(10), nullable=True)
    fax = db.Column(db.String(10), nullable=True)
    
    def __repr__(self):
        return '<Task %r>' % self.id
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def set_from_dict(self,data):

        """
        Update object attributes from a dictionary.

        :param data: A dictionary containing the new data.
        """
        for key, value in data.items():
            setattr(self, key, value)
