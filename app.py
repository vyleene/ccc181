"""LaundryQ Flask application."""

import os
import re
from datetime import timedelta, timezone

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
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
PAGE_SIZE = 10
STAFF_ACTIONS = {
    "call": "called",
    "serve": "served",
    "no-show": "no-show",
}

# ---------------------------------------------------------------------------
# Template helpers and CLI commands
# ---------------------------------------------------------------------------

@app.template_filter("local")
def local_time(value):
    """Format a database timestamp in Philippine time."""
    if value is None:
        return ""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p")


@app.cli.command("seed")
def seed():
    """Add LaundryQ's starting services if they are not present."""
    starting_services = ("Wash and dry", "Wash only", "Dry only")

    for name in starting_services:
        service = db.session.scalar(
            db.select(Service).filter_by(name=name)
        )
        if service is None:
            db.session.add(Service(name=name))

    db.session.commit()
    print("Services are ready.")


# ---------------------------------------------------------------------------
# Shared database queries
# ---------------------------------------------------------------------------

def all_services():
    """Return all services for staff views."""
    statement = db.select(Service).order_by(Service.name)
    return db.session.scalars(statement).all()


def active_services():
    """Return services currently available to residents."""
    statement = db.select(Service).filter_by(active=True).order_by(Service.name)
    return db.session.scalars(statement).all()


def people_ahead(ticket):
    """Count earlier waiting tickets for the same service."""
    statement = (
        db.select(func.count())
        .select_from(Ticket)
        .where(
            Ticket.service_id == ticket.service_id,
            Ticket.status == "waiting",
            Ticket.created_at < ticket.created_at,
        )
    )
    return db.session.scalar(statement)


def session_ticket():
    """Return the resident's active ticket, if one is stored in the session."""
    ticket_id = session.get("ticket_id")
    if ticket_id is None:
        return None

    ticket = db.session.get(Ticket, ticket_id)
    if ticket is None or ticket.status not in ("waiting", "called"):
        session.pop("ticket_id", None)
        return None
    return ticket


@app.context_processor
def inject_session_ticket():
    """Make the resident's active ticket available to every template."""
    return {"my_ticket": session_ticket()}


# ---------------------------------------------------------------------------
# Public and resident routes
# ---------------------------------------------------------------------------

@app.get("/")
def index():
    """Show the LaundryQ welcome page."""
    return render_template("index.html", name="Ana")


@app.get("/join")
def join_form():
    """Show the resident queue form."""
    current_ticket = session_ticket()
    if current_ticket is not None:
        return redirect(url_for("ticket", ticket_id=current_ticket.id))
    return render_template("join.html", services=active_services(), form={})


@app.post("/join")
def join():
    """Validate the resident form and create a ticket."""
    current_ticket = session_ticket()
    if current_ticket is not None:
        return redirect(url_for("ticket", ticket_id=current_ticket.id))

    form = request.form
    name = form.get("name", "").strip()
    mobile_number = form.get("mobile_number", "").strip()
    service_id = form.get("service_id", type=int)
    service = db.session.get(Service, service_id) if service_id else None

    errors = {}
    if not name or len(name) > 120:
        errors["name"] = "Enter your name (up to 120 characters)."
    if not re.fullmatch(r"09\d{9}", mobile_number):
        errors["mobile_number"] = (
            "Enter an 11-digit mobile number starting with 09."
        )
    if service is None or not service.active:
        errors["service_id"] = "Choose a service."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return (
            render_template(
                "join.html",
                services=active_services(),
                form=form,
                errors=errors,
            ),
            400,
        )

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
        return (
            render_template(
                "join.html",
                services=active_services(),
                form=form,
                errors={},
            ),
            409,
        )

    session["ticket_id"] = ticket.id
    flash(f"You joined the queue. Your ticket is #{ticket.id}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    """Show a resident's ticket and position in line."""
    current_ticket = db.get_or_404(Ticket, ticket_id)
    return render_template(
        "ticket.html",
        ticket=current_ticket,
        service=current_ticket.service,
        ahead=people_ahead(current_ticket),
    )


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    """Return the current ticket status and position as JSON."""
    current_ticket = db.get_or_404(Ticket, ticket_id)
    return {
        "status": current_ticket.status,
        "ahead": people_ahead(current_ticket),
    }


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    """Mark a waiting ticket as left without deleting its history."""
    current_ticket = db.get_or_404(Ticket, ticket_id)
    if current_ticket.status == "waiting":
        current_ticket.status = "left"
        db.session.commit()
    if session.get("ticket_id") == ticket_id:
        session.pop("ticket_id", None)

    flash("You left the queue.", "info")
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# Staff service management
# ---------------------------------------------------------------------------

@app.get("/staff/services")
def services_list():
    """Show all services and their ticket counts."""
    return render_template("services.html", services=all_services())


@app.post("/staff/services")
def service_create():
    """Create a service from the staff management form."""
    name = request.form.get("name", "").strip()
    if not name or len(name) > 80:
        flash("Enter a service name up to 80 characters.", "danger")
        return redirect(url_for("services_list"))

    db.session.add(Service(name=name))
    try:
        db.session.commit()
        flash(f"Service “{name}” added.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named “{name}” already exists.", "danger")

    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/edit")
def service_edit(service_id):
    """Update a service name and active status."""
    service = db.get_or_404(Service, service_id)
    name = request.form.get("name", "").strip()
    if not name or len(name) > 80:
        flash("Enter a service name up to 80 characters.", "danger")
        return redirect(url_for("services_list"))

    service.name = name
    service.active = request.form.get("active") == "on"

    try:
        db.session.commit()
        flash(f"Service “{name}” updated.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named “{name}” already exists.", "danger")

    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/delete")
def service_delete(service_id):
    """Delete a service only when it has no ticket history."""
    service = db.get_or_404(Service, service_id)
    if service.tickets:
        flash(
            f"“{service.name}” has tickets, so it cannot be deleted. "
            "Turn it off instead.",
            "danger",
        )
        return redirect(url_for("services_list"))

    db.session.delete(service)
    db.session.commit()
    flash(f"Service “{service.name}” deleted.", "warning")
    return redirect(url_for("services_list"))


# ---------------------------------------------------------------------------
# Staff queue routes
# ---------------------------------------------------------------------------

@app.get("/staff")
def staff_dashboard():
    """Show the staff queue with filtering and pagination."""
    service_id = request.args.get("service_id", type=int)
    page = max(request.args.get("page", 1, type=int), 1)

    statement = (
        db.select(Ticket)
        .where(
            Ticket.status.in_(["waiting", "called", "served", "no-show", "left"])
        )
        .order_by(Ticket.created_at)
    )
    if service_id:
        statement = statement.where(Ticket.service_id == service_id)

    queue = db.session.scalars(statement).all()
    total_pages = max((len(queue) + PAGE_SIZE - 1) // PAGE_SIZE, 1)
    page = min(page, total_pages)
    start = (page - 1) * PAGE_SIZE
    page_queue = queue[start:start + PAGE_SIZE]

    return render_template(
        "staff.html",
        queue=queue,
        page_queue=page_queue,
        services=all_services(),
        selected=service_id,
        page=page,
        page_size=PAGE_SIZE,
        total_pages=total_pages,
    )


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    """Apply a staff action to the selected ticket."""
    new_status = STAFF_ACTIONS.get(action)
    if new_status is None:
        abort(404)

    if new_status == "called":
        current_ticket = db.get_or_404(Ticket, ticket_id)
        if current_ticket.status != "waiting":
            flash("That ticket is no longer waiting.", "info")
            return redirect(
                url_for(
                    "staff_dashboard",
                    service_id=request.args.get("service_id", type=int),
                )
            )
        current_ticket.status = new_status
        current_ticket.called_at = func.now()
    else:
        current_ticket = db.get_or_404(Ticket, ticket_id)
        current_ticket.status = new_status

    db.session.commit()
    flash(f"Ticket #{current_ticket.id} marked {new_status}.", "info")
    return redirect(
        url_for(
            "staff_dashboard",
            service_id=request.args.get("service_id", type=int),
        )
    )


@app.post("/staff/tickets/<int:ticket_id>/delete")
def delete_ticket(ticket_id):
    """Permanently delete a ticket after confirmation in the browser."""
    current_ticket = db.get_or_404(Ticket, ticket_id)
    db.session.delete(current_ticket)
    db.session.commit()
    flash(f"Ticket #{ticket_id} was deleted.", "warning")
    return redirect(url_for("staff_dashboard"))


@app.route("/hello")
def hello():
    """Return the starter route response."""
    return "Hello, CCC181!"


if __name__ == "__main__":
    app.run(debug=True)
