import base64
from extensions import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    availableAmount = db.Column(db.Integer, nullable=False, default=1)
    rate = db.Column(db.Integer)
    img = db.Column(db.LargeBinary)
    manufactureDate = db.Column(db.DateTime)
    expiryDate = db.Column(db.DateTime)
    section_id = db.Column(db.Integer, db.ForeignKey(
        'section.id'), nullable=False)
    avg_rating = db.Column(db.Integer)
    description = db.Column(db.String())
    # getting section details
    section = db.relationship(
        "Section", back_populates="products")

    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "rate": self.rate,
            "availableAmount": self.availableAmount,
            "manufactureDate": self.manufactureDate.strftime('%Y-%m-%d') if self.manufactureDate != None else None,
            "expiryDate": self.expiryDate.strftime('%Y-%m-%d') if self.expiryDate != None else None,
            "section": self.section.toJson(),
            "img": base64.b64encode(self.img).decode('utf-8') if self.img != None else None,
            "description": self.description
        }
