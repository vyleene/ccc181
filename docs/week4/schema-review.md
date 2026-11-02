# LaundryQ schema self-review

## 1. Coverage

All requirements marked **Stores data? = Yes** have a matching table or
column:

- **FR-01:** `users` stores the resident's name and mobile number; `services`
  identifies the selected laundry service; `tickets` records the visit.
- **FR-02:** `tickets.id` and `tickets.status` are stored, while the number
  ahead is computed from `created_at`.
- **FR-03 and FR-06:** `tickets.called_at` records the call event that triggers
  the visible alert.
- **FR-04 and FR-07:** `tickets.status`, `left_at`, `served_at`, and
  `no_show_at` record queue outcomes.
- **FR-05:** `users`, `services`, and `tickets` provide the ordered queue,
  resident name, service, and status.
- **FR-08:** `services.name` and `services.active` support service management.
- **FR-09:** `tickets.left_at`, `service_id`, and `status` support the daily
  service report.
- **FR-12:** `tickets.id` provides the confirmation number.

The Week 3 persona tasks are also covered: residents can join a service queue,
check their number and position, receive the call event, and leave; staff can
see the ordered queue, call the next person, mark a ticket served, and mark a
no-show. No table is unnecessary: `users`, `services`, and `tickets` each
represent a different fact. The `role` column is needed to distinguish staff
from residents.

## 2. One fact in one place

> **Works well:** Resident details are stored only in `users`, service details
> are stored only in `services`, and tickets keep only `user_id` and
> `service_id`. This prevents a name, mobile number, or service name from
> being copied into every ticket row.

> **Problem:** Event timestamps can become inconsistent with `status` if an
> application update writes one without the other, such as a ticket marked
> `served` without `served_at`.

> **Change:** Keep the separate event columns because they are historical facts
> needed for reports. When implementing the database, add status-transition
> validation in the service layer and use one transaction to update the status
> and its timestamp together.

## 3. Facts, not results

> **Works well:** The schema stores `created_at`, not a mutable queue position,
> count, or waiting time. The number of people ahead is computed from earlier
> waiting tickets for the same service.

> **Problem:** None found in the current tables. Storing a position or daily
> count would become stale whenever someone joins, leaves, or is served.

> **Change:** Keep the schema as written. Compute queue position and daily
> totals from ticket facts when the staff or resident requests them.

## 4. Bad data

> **Works well:** A generated identity primary key prevents two tickets from
> receiving the same ticket number, foreign keys reject missing users or
> services, the mobile-number check catches malformed resident numbers, and
> the service-name `UNIQUE` constraint prevents duplicate service names.

> **Problem:** A double tap can still create two valid tickets for the same
> person because duplicate visits are not automatically distinguishable from a
> legitimate later visit.

> **Change:** Keep this as an application-level concern rather than adding a
> permanent unique constraint on `user_id`: one resident may legitimately
> return for another laundry visit. The join form's submit guard should be
> combined with a database transaction and an idempotency key when the
> database-backed join flow is implemented.

## 5. Deletes

> **Works well:** Both foreign keys deliberately use `ON DELETE RESTRICT`.
> Deleting a user or service cannot erase tickets that staff need for queue
> history and reports.

> **Problem:** `RESTRICT` means staff cannot delete a user or service that has
> tickets, so a physical delete cannot be used for routine account or service
> cleanup.

> **Change:** Keep `RESTRICT`. Services should be switched off with
> `services.active = false`, and user records should be retained for ticket
> history. This protects the facts needed for reporting.

## 6. Types

> **Works well:** Every time value uses `timestamptz`; identity values use
> integer types; `active` uses boolean; and status and role are text values
> constrained by `CHECK` clauses.

> **Problem:** None found in the current schema. Mobile numbers are correctly
> stored as text because the leading `0` is meaningful and arithmetic is not
> performed on them.

> **Change:** Keep the types. Do not convert mobile numbers to integers or
> timestamps to text, because either choice would lose validation or
> time-zone-safe behavior.
