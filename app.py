
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from nav import driving_distance
from datetime import datetime

app = Flask(__name__, template_folder='./')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seeker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #for signal limiting and all
db = SQLAlchemy(app)

class Seeker(db.Model):
    phone = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(200), nullable = False)
    address = db.Column(db.String(200), nullable = False)

    def _repr_(self):  #govern what to show as print when database is called
        return f"{self.phone} " # shows only symbol number and title 

@app.route("/", methods=['GET', 'POST'])
def index():
    # print(driving_distance.dist('400 Southwest Parkway', 'Houston'))
    if request.method == 'POST':
        if request.form.get('volunteer') == 'Volunteer':
            return redirect('/volunteer')
        elif request.form.get('seeker') == 'Seeker':
            return redirect('/seeker')
    
    return render_template('index.html')

@app.route('/volunteer', methods=['GET', 'POST'])
def volunteer():
    return render_template('volunteer.html')

@app.route('/seeker', methods=['GET', 'POST'])
def seeker():
    return render_template('seeker.html')

@app.route('/seeker_display', methods=['GET', 'POST'])
def seeker_display():
    headings = ("Name", "Phone Number", "Address", "Distance(Miles)")
    data = []
    if request.method == 'POST':
        Address = request.form.get('currentLocation')
        Radius = request.form.get('Radius')
        qdata = Seeker.query.all()
        
        for i in qdata:
            print("hello")
            distance = float(driving_distance.dist(Address, i.address))
            if distance < float(Radius):
                dt = (i.name, i.phone, i.address, distance)
                data.append(dt)
        print(tuple(data))    
        return render_template('/seeker_display.html', headings=headings, data=tuple(data))
        
    return render_template('seeker_display.html', headings=headings, data=tuple(data))

@app.route('/volunteer_display', methods=['GET', 'POST'])
def volunteer_display():
    if request.method == "POST":    
        Name = request.form.get('Name')
        Phone = request.form.get('Phone')
        Address = request.form.get('Address')
        print(str(Name))
        new_input = Seeker(phone=int(Phone), name=Name, address=Address)
        
        try:
            db.session.add(new_input)
            db.session.commit()
            return "Your Request Has been Submitted"
        except:
            return "There was an error adding"

    

if __name__ == "__main__":
    app.run(debug=True, port=8000)
    

    