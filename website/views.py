import mysql.connector
from flask import Blueprint, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required, current_user

from werkzeug.utils import redirect

from website.models import Note
from website._init_ import db
import json


views = Blueprint('views', __name__)


@views.route('/guest', methods=['GET', 'POST'])
def home_guest():
    return render_template("home.html", user=current_user)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/1', methods=['GET', 'POST'])
def view_1():
    sched = []

    class user:
        def __init__(self, username, type):
            self.username = username
            self.trip_chosen = 0
            self.type = type

    class Ticket:
        def __init__(self, title, seatsLeft, startTime, endTime, price, ID):
            self.title = title
            self.seatsLeft = seatsLeft
            self.startTime = startTime
            self.endTime = endTime
            self.price = price
            self.ID = ID

    sched = [Ticket("Elestad - Hesham Barakat", 5, "9:00 am", "9:30 am", 20, 1),
             Ticket("Hesham Barakat - Nori Khatab", 12, "9:30 am", "10:00 am", 10, 2),
             Ticket("Nori Khatab - El Hay ElSabe3", 2, "10:00 am", "10:30 am", 20, 3),
             Ticket("El Hay ElSabe3 - Zaker Hussien", 5, "10:30 am", "11:00 am", 20, 4),
             Ticket("Zaker Hussien - El Manteka El Hora", 5, "11:00 am", "11:30 am", 20, 5),
             Ticket("El Manteka El Hora - El Mosheer Tantawy", 5, "11:30 am", "12:00 pm", 20, 6),
             Ticket("El Mosheer Tantawy - Cairo Festival", 5, "12:00 pm", "12:30 pm", 20, 7),
             Ticket("Cairo Festival - Elshowayfat", 5, "1:00 pm", "1:30 pm", 20, 8),
             Ticket("Elshowayfat - Air Force Hospital", 5, "1:30 pm", "2:00 pm", 20, 9),
             Ticket("Air Force Hospital - Hay El Narges", 5, "2:00 pm", "2:30 pm", 20, 10),
             Ticket("Hay El Narges - Mohamed Nageeb", 5, "2:30 pm", "3:00 pm", 20, 11),
             Ticket("Mohamed Nageeb - AUC", 5, "3:00 pm", "3:30 pm", 20, 12),
             Ticket("AUC - Emaar", 5, "3:30 pm", "4:00 pm", 20, 13),
             ]
    if request.method == 'POST':
        price = request.form.get('price')
        return render_template("payment.html", user=current_user, price=price)

    return render_template("trip.html", user=current_user, sched=sched)


@views.route('/2', methods=['GET', 'POST'])
def view_2():
    records = []

    if request.method == 'POST':
        price = request.form.get('price')
        return render_template("payment.html", user=current_user, price=price)

    return render_template("subscri.html", user=current_user, records=records)

@views.route('/pay', methods=['GET', 'POST'])
def pay():
    records = []

    if request.method == 'POST':
        price = request.form.get('price')
        return render_template("confirm.html", user=current_user, price=price)

    return render_template("payment.html", user=current_user, records=records)