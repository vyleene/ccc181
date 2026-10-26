# Usability test

## 10a. Testing

The participant was asked to think aloud and completed the three tasks without
help. The complete flow took about **1 minute and 20 seconds**.

### Task 1

> “You just arrived. Get in line for one of your services.”

- **Finished:** Yes
- **Time:** About 24 seconds
- **Observation:** The participant completed the flow without hesitation or
  surprise. They navigated from home to Join the queue and submitted the form.
- **Persona rules that held up:** The interface let the participant choose a
  service, enter a name and mobile number, and get a queue number without an
  account or sign-up. The simple form and large controls supported Mika's
  one-handed phone use.
- **Rules that did not hold up:** None observed for this task.

### Task 2

> “How many people are ahead of you? What is your number?”

- **Finished:** Yes
- **Time:** About 8 seconds
- **Observation:** The participant found the ticket number and people-ahead
  count immediately, with no hesitation or surprise.
- **Persona rules that held up:** The lightweight My place screen showed the
  number and position first, using large, plain text.
- **Rules that did not hold up:** The participant's broader test feedback
  identified that the screen did not show an estimated wait or a visible alert
  with a return time. These rules were not needed to finish this task, but
  they remain unmet.

### Task 3

> “Pretend you are the staff member. Call the next person and mark them as
> served.”

- **Finished:** Yes
- **Time:** About 29 seconds
- **Observation:** The participant had slight trouble understanding how to
  mark a person served because the Call Next button is at the top while the
  serving action is inside the table.
- **Persona rules that held up:** Large text, strong contrast, large buttons,
  a clearly ordered queue, visible statuses, plain words, and actions for
  calling, serving, and removing a no-show all supported Mang Ernie's needs.
- **Rules that did not hold up:** The queue did not show arrival times, so the
  participant could not verify order using the same evidence described in the
  staff persona.

## 10b. One improvement

### Problem

The most serious observed problem was the hesitation in Task 3. The participant
understood **Call Next**, but the table action labeled **Serve** did not match
the task wording “mark them as served” closely enough. The separate locations
of the call and serve actions increased the chance of a wrong or delayed tap.

### Fix

The table action now says **Mark as served** instead of **Serve**. The
ticket-specific accessible label already says “Mark ticket [number] as
served,” so the visible label now matches the accessible label, persona
language, and task instruction. This is a small recognition and consistency
improvement that does not change the existing workflow.

## 10c. Before and after

- **Before:** The row action was labeled **Serve**, and the participant paused
  before connecting it to “mark them as served.”
- **After:** The row action is labeled **Mark as served**, making the intended
  action explicit.
