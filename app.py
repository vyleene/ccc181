"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import re

from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

# Sample data for the demo. It lives in memory, so it resets every time the
# server restarts. A real app would save tickets in a database later.
SERVICES = [
    {"id": 1, "name": "Wash and dry"},
    {"id": 2, "name": "Wash only"},
    {"id": 3, "name": "Dry only"},
]

TICKETS = [
    {"number": 1, "name": "Mika", "mobile_number": "09123456789", "service_id": 1, "status": "waiting"},
    {"number": 2, "name": "Carlo", "mobile_number": "09123456789", "service_id": 1, "status": "called"},
    {"number": 3, "name": "Aling Nena", "mobile_number": "09123456789", "service_id": 2, "status": "waiting"},
    {"number": 4, "name": "Jun", "mobile_number": "09123456789", "service_id": 2, "status": "no-show"},
    {"number": 5, "name": "Bea", "mobile_number": "09123456789", "service_id": 3, "status": "served"},
]


@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html", name="Ana", tickets=TICKETS)


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    ahead = [x for x in TICKETS
             if x["service_id"] == t["service_id"]
             and x["status"] == "waiting"
             and x["number"] < t["number"]]
    service = next(s for s in SERVICES if s["id"] == t["service_id"])
    return render_template("ticket.html", ticket=t, service=service, ahead=len(ahead))


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)

    t["status"] = "no-show"
    flash(f"Ticket #{ticket_id} has left the queue.", "success")
    return redirect(url_for("index"))


@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, form={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    mobile_number = form.get("mobile_number", "").strip()
    service_id = form.get("service_id", type=int)

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    if not re.fullmatch(r"09\d{9}", mobile_number):
        errors["mobile_number"] = "Enter an 11-digit mobile number starting with 09."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({"number": number, "name": name, "mobile_number": mobile_number,
                    "service_id": service_id, "status": "waiting"})
    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))


@app.route("/staff")
def staff():
    return "Staff dashboard coming soon"


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)