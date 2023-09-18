from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .config import Config
from .models import db, Donation, DonationDistribution

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Create the database tables
with app.app_context():
    # db.drop_all()     
    db.create_all()

# home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for donation registration form
@app.route('/donation_register', methods=['GET', 'POST'])
def donation_register():
    if request.method == 'POST':
        donor_name = request.form['donor_name']
        donation_type = request.form['donation_type']
        quantity = int(request.form['quantity'])

        new_donation = Donation(donor_name=donor_name, donation_type=donation_type, quantity=quantity)
        db.session.add(new_donation)
        db.session.commit()

        return redirect(url_for('donation_register'))

    return render_template('donation_form.html')

@app.route('/donation_distribution', methods=['GET', 'POST'])
def donation_distribution():
    if request.method == 'POST':
        donation_type = request.form['donation_type']
        quantity = int(request.form['quantity'])
        distribution_date = datetime.strptime(request.form['distribution_date'], '%Y-%m-%dT%H:%M')
        

        new_input = DonationDistribution(donation_type=donation_type, quantity=quantity, distribution_date=distribution_date)
        db.session.add(new_input)
        db.session.commit()

        return redirect(url_for('donation_register'))

    return render_template('donation_distribution_form.html')

@app.route('/donation_reports')
def donation_reports():
    # Query the database to get donation totals grouped by type
    donation_totals = (
        db.session.query(
            Donation.donation_type,
            db.func.sum(Donation.quantity).label('donation_quantity'),
            db.func.sum(DonationDistribution.quantity).label('distribution_quantity')
        )
        .outerjoin(
            DonationDistribution,
            Donation.donation_type == DonationDistribution.donation_type
        )
        .group_by(Donation.donation_type)
        .order_by(db.func.sum(Donation.quantity).desc())
        .all()
    )
    
    return render_template('donation_reports.html', donation_totals=donation_totals)

if __name__ == '__main__':
    app.run(debug=True)