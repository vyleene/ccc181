# Validation in three layers

LaundryQ validates input in the browser, in Flask, and in PostgreSQL. The
browser gives users quick feedback, Flask rejects requests that skip the
browser, and database constraints protect the data from application bugs or
direct SQL access.

## Browser validation

The join form matches the current schema:

- `name` is required and limited to 120 characters.
- `mobile_number` is required, limited to 11 characters, and must match the
  `09` plus nine digits pattern.
- `service_id` is required.

There is no email field or `avg_minutes` column in LaundryQ, so those examples
are not part of this validation table.

## Flask validation

These requests were sent with Flask's test client, bypassing browser
validation. Each returned `400 BAD REQUEST` and did not create a ticket.

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| Name is required | Flask | Posted an empty `name` to `/join` | `400 BAD REQUEST`, nothing saved |
| Mobile number must match the Philippine format | Flask | Posted `mobile_number=123` to `/join` | `400 BAD REQUEST`, nothing saved |
| Service must exist | Flask | Posted `service_id=999999` to `/join` | `400 BAD REQUEST`, nothing saved |
| Service must be active | Flask | Switched a service off, then posted its ID to `/join` | `400 BAD REQUEST`, nothing saved |

## PostgreSQL validation

Each statement was run in a transaction and rolled back after the expected
error. The following messages are the exact first lines returned by
PostgreSQL.

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| Service foreign key must exist | Database | `INSERT INTO tickets (user_id, service_id) VALUES (:user_id, 999999)` | `insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` |
| Ticket status must be allowed | Database | `UPDATE tickets SET status = 'lost' WHERE id = :ticket_id` | `new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| Mobile number must be unique | Database | Inserted a second user with an existing mobile number | `duplicate key value violates unique constraint "users_mobile_number_key"` |
| User name must not be null | Database | `INSERT INTO users (name, mobile_number) VALUES (NULL, '09999999999')` | `null value in column "name" of relation "users" violates not-null constraint` |
| Services with ticket history cannot be deleted | Database | `DELETE FROM services WHERE id = :service_id` | `update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` |

## SQL injection check

The application uses SQLAlchemy expressions and bound parameters rather than
building SQL with user input. This repository check returned no matches:

```text
git grep -nE "f[\"'].*(SELECT|INSERT|UPDATE|DELETE)" -- "*.py"
```

No SQL statements are built inside f-strings.
