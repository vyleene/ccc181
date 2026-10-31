"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import os
import re
from datetime import timedelta, timezone

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Service, Ticket, User, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)
PH_TIME = timezone(timedelta(hours=8))


@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""

@app.cli.command("seed")
def seed():
    """Add LaundryQ's starting services if they are not there yet."""
    starting = ("Wash and dry", "Wash only", "Dry only")
    for name in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name))
    db.session.commit()
    print("Services are ready.")


@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html", name="Ana")


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return render_template(
        "ticket.html",
        ticket=t,
        service=t.service,
        ahead=people_ahead(t),
    )

@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return {"status": t.status, "ahead": people_ahead(t)}


def people_ahead(t):
    """Count waiting tickets for the same service that joined before t."""
    stmt = (
        db.select(func.count())
        .select_from(Ticket)
        .where(
            Ticket.service_id == t.service_id,
            Ticket.status == "waiting",
            Ticket.created_at < t.created_at,
        )
    )
    return db.session.scalar(stmt)

@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)

    t["status"] = "no-show"
    flash(f"Ticket #{ticket_id} has left the queue.", "success")
    return redirect(url_for("index"))


def all_services():
    return db.session.scalars(
        db.select(Service).where(Service.active.is_(True)).order_by(Service.name)
    ).all()


@app.get("/join")
def join_form():
    return render_template("join.html", services=all_services(), form={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    mobile_number = form.get("mobile_number", "").strip()
    service_id = form.get("service_id", type=int)

    errors = {}
    if not name or len(name) > 120:
        errors["name"] = "Enter your name (up to 120 characters)."
    if not re.fullmatch(r"09\d{9}", mobile_number):
        errors["mobile_number"] = "Enter an 11-digit mobile number starting with 09."
    service = db.session.get(Service, service_id) if service_id else None
    if service is None or not service.active:
        errors["service_id"] = "Choose a service."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template(
            "join.html",
            services=all_services(),
            form=form,
            errors=errors,
        ), 400

    user = db.session.scalar(
        db.select(User).filter_by(mobile_number=mobile_number)
    )
    if user is None:
        user = User(name=name, mobile_number=mobile_number)
        db.session.add(user)

    ticket = Ticket(user=user, service=service)
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Something went wrong saving your ticket. Please try again.", "danger")
        return render_template(
            "join.html",
            services=all_services(),
            form=form,
            errors={},
        ), 409

    flash(f"You joined the queue. Your ticket is #{ticket.id}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    page = max(request.args.get("page", 1, type=int), 1)
    page_size = 10
    stmt = (
        db.select(Ticket)
        .where(Ticket.status.in_(["waiting", "called"]))
        .order_by(Ticket.created_at)
    )
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    queue = db.session.scalars(stmt).all()
    total_pages = max((len(queue) + page_size - 1) // page_size, 1)
    page = min(page, total_pages)
    start = (page - 1) * page_size
    page_queue = queue[start:start + page_size]
    return render_template(
        "staff.html",
        queue=queue,
        page_queue=page_queue,
        services=all_services(),
        selected=service_id,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = {"call": "called", "serve": "served", "no-show": "no-show"}.get(action)
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None or new_status is None:
        abort(404)
    t["status"] = new_status
    flash(f"Ticket #{ticket_id} marked {new_status}.", "info")
    return redirect(url_for("staff_dashboard"))


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)