from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Donation model
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(100), nullable=False)
    donation_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    donation_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Donation('{self.donor_name}', '{self.donation_type}', {self.quantity}, '{self.donation_date}')"

# DonationDistribution model
class DonationDistribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donation_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    distribution_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"DonationDistribution({self.donation_type}, {self.quantity}, '{self.distribution_date}')"