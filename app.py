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
    {"number": 1, "name": "Mika Santos", "mobile_number": "09123456789", "service_id": 1, "status": "waiting"},
    {"number": 2, "name": "Carlo Reyes", "mobile_number": "09123456780", "service_id": 1, "status": "waiting"},
    {"number": 3, "name": "Nena Dela Cruz", "mobile_number": "09123456781", "service_id": 2, "status": "waiting"},
    {"number": 4, "name": "Jun Bautista", "mobile_number": "09123456782", "service_id": 2, "status": "called"},
    {"number": 5, "name": "Bea Navarro", "mobile_number": "09123456783", "service_id": 3, "status": "waiting"},
    {"number": 6, "name": "Ana Villanueva", "mobile_number": "09123456784", "service_id": 1, "status": "waiting"},
    {"number": 7, "name": "Rafael Mendoza", "mobile_number": "09123456785", "service_id": 2, "status": "waiting"},
    {"number": 8, "name": "Liza Fernandez", "mobile_number": "09123456786", "service_id": 3, "status": "waiting"},
    {"number": 9, "name": "Marco Dizon", "mobile_number": "09123456787", "service_id": 1, "status": "called"},
    {"number": 10, "name": "Sofia Aguilar", "mobile_number": "09123456788", "service_id": 2, "status": "waiting"}
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


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    page = max(request.args.get("page", 1, type=int), 1)
    page_size = 10
    queue = [t for t in TICKETS if t["status"] in ("waiting", "called")]
    if service_id:
        queue = [t for t in queue if t["service_id"] == service_id]
    queue.sort(key=lambda t: t["number"])
    total_pages = max((len(queue) + page_size - 1) // page_size, 1)
    page = min(page, total_pages)
    start = (page - 1) * page_size
    page_queue = queue[start:start + page_size]
    names = {s["id"]: s["name"] for s in SERVICES}
    return render_template("staff.html", queue=queue, page_queue=page_queue,
                           services=SERVICES, names=names, selected=service_id,
                           page=page, page_size=page_size, total_pages=total_pages)


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