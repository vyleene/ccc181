# LaundryQ requirements

**Setting:** University dormitory laundry room, especially busy evenings and
weekends

**People who wait:** [Mika Santos, the person waiting](week3/personas.md)

**People who serve:** [Mang Ernie Dela Cruz, the staff member](week3/personas.md)

**Problem statement:** A dormitory resident needs a way to join the correct
laundry queue and know when to return without standing beside the machines,
because unclear basket-based queues make people lose their place and waste
limited study time.

## Functional requirements

| ID | Requirement | Priority | Stores data? | Status |
| --- | --- | --- | --- | --- |
| FR-01 ★ | A resident can join a queue for a specific laundry service by entering their name and mobile number. | Must | Yes | Built (Week 3) |
| FR-02 | A resident can see their ticket number, current status, how many people are ahead of them. | Must | Yes | Built (Week 3) |
| FR-03 ★ | A resident can receive a visible alert when they are called | Must | Yes | Later |
| FR-04 | A resident can leave the queue before being served. | Must | Yes | Built (Week 3) |
| FR-05 | A staff member can see the active queue in ticket order, including each resident's name, laundry service, and status. | Must | Yes | Built (Week 3) |
| FR-06 ★ | A staff member can call the next waiting resident for the selected laundry service. | Must | Yes | Built (Week 3) |
| FR-07 | A staff member can mark a called ticket as served or no-show. | Must | Yes | Built (Week 3) |
| FR-08 ★ | A staff member can add, rename, and switch off a laundry service. | Must | Yes | This week |
| FR-09 | A staff member can see how many residents left before being served, per service and per day. | Should | Yes | Later |
| FR-10 | A senior citizen or person with a disability can join a priority laundry lane that is served first. | No | Yes | Out-of-scope |
| FR-11 | A resident can switch the queue screens to a larger text size. | No | No | Out-of-scope |
| FR-12 | A resident can receive a confirmation containing their ticket number after joining the queue. | Should | Yes | Built (Week 3) |

## Non-functional requirements

| ID | Requirement | Category | Priority |
| --- | --- | --- | --- |
| NFR-01 | No active ticket or service is lost when the application or database restarts. | Reliability | Must |
| NFR-02 | Two residents can never receive the same ticket number, even if they join at the same moment. | Data integrity | Must |
| NFR-03 | The My place screen loads in under 2 seconds on a mobile-data connection in a normal test run. | Performance | Should |
| NFR-04 | Every resident and staff screen scores at least 90 in the Lighthouse accessibility check. | Accessibility | Must |
| NFR-05 | No password, production credential, or secret key is stored in the repository. | Security | Must |

## MVP

The MVP consists of **FR-01, FR-02, FR-04, FR-05, FR-06, FR-07, FR-08,
NFR-01, NFR-02, NFR-03, NFR-04, and NFR-05**. These requirements cover joining
and tracking a laundry queue, the staff's core workflow, and the reliability,
performance, accessibility, and security needed for a usable first release.

## Out of scope

- **FR-10 priority lanes** are out of scope for this semester because they add
  policy and fairness decisions that should be agreed with dormitory staff
  before implementation.
- **FR-11 larger-text switching** is out of scope for the MVP because the
  current responsive design and accessibility work provide a usable baseline;
  it can be added after the core database workflow is stable.
- Payment processing, machine-status monitoring, and user accounts are also
  out of scope because the current problem is queue coordination rather than
  payment or machine control.

## Requirements review

| Who (role only, no full name) | What they said | What I changed |
| --- | --- | --- |
| Dental student | “The queue needs to show a fair order and each person's service.” | Kept FR-05 as a Must requirement for an ordered queue with names, services, and statuses. |