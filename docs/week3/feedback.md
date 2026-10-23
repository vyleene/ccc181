# Week 3 usability review

## Join queue

1. **Can my persona tell what to do on this screen within 5 seconds?**  
   Yes. “Join the queue” is the clear page title, the form has familiar labels, and “Get a ticket” is the prominent final action.

2. **Is the ticket status always visible where the person needs it?**  
   This screen does not yet have a ticket status. That is appropriate because the resident is still joining the queue; status appears on the My place screen after submission.

3. **Do the words match what people in my setting actually say?**  
   Mostly. “Name,” “Mobile Number,” “Service,” and “Get a ticket” are understandable in a dorm laundry setting. “Ticket” is acceptable because it identifies the resident's queue number, although “queue number” would be the most literal local wording.

4. **Is the action the staff member does most often the easiest one to reach?**  
   This is a resident screen, so the relevant frequent action is joining the queue. “Get a ticket” is the full-width, large button and is easy to reach.

5. **Does the phone version still show the most important thing first?**  
   Yes. The title, short explanation, and form are presented in a single column with large controls suitable for one-handed use.

6. **Which “Because …, my interface must …” rules does this screen follow, and which does it break?**  
   It follows the rule that Mika can join without an account or sign-up and uses large controls for one-handed use. It partially breaks the rule requiring three large service choices: the current design uses one select control rather than three visible choices. No change is required for the current review because the select control remains a short, familiar interaction and keeps the small-screen form compact.

**Works well:** The large, direct “Get a ticket” button gives Mika an obvious next step and supports recognition rather than recall.  
**Problem:** The service choices are hidden inside a select control, so Mika cannot see the three available services immediately. This is a minor recognition rather than recall issue.  
**Change:** Keep the current wireframe. The service label and “Choose a service” prompt make the control understandable, and avoiding extra visible controls keeps the mobile form compact.

## My place

1. **Can my persona tell what to do on this screen within 5 seconds?**  
   Yes. The large ticket number, service, position, and status immediately explain where the resident is in the queue.

2. **Is the ticket status always visible where the person needs it?**  
   Yes. “Current status” is displayed near the top beside the resident's position, inside a live status region. It is visible without scrolling.

3. **Do the words match what people in my setting actually say?**  
   Yes, for the most important information. “Your ticket number,” “Current status,” “Your position,” and “Leave the queue” are plain and familiar. “Selected service” is also clear enough for the laundry context.

4. **Is the action the staff member does most often the easiest one to reach?**  
   Staff actions do not belong on this resident screen. The resident's relevant action, leaving the queue, is a large full-width button and is easy to reach when needed.

5. **Does the phone version still show the most important thing first?**  
   Yes. The ticket number is largest, followed by service, current status, and position. The card remains readable on a phone.

6. **Which “Because …, my interface must …” rules does this screen follow, and which does it break?**  
   It follows the rules requiring the ticket number, position, and status to appear first in a lightweight screen, and it provides a visible status rather than relying on sound. It partially breaks the rules requiring an estimated wait, a visible time limit to return, and vibration when the turn is near: the current screen shows position but not an estimated wait, return deadline, or vibration behavior. No change is required for this review because the existing visible position and status already support the core task and the screen remains clear.

**Works well:** The status and position panels are visible together near the top, which supports visibility of status and lets Mika quickly decide whether she needs to return.  
**Problem:** The screen does not show an estimated wait or a clear “return within” time, which could leave Mika unsure whether she can safely go back to studying. This is a visibility of status issue.  
**Change:** Keep the current wireframe. The current screen is intentionally focused and readable; the existing status and position information are sufficient for this review without adding more visual density.

## Staff dashboard

1. **Can my persona tell what to do on this screen within 5 seconds?**  
   Yes. “Staff Dashboard,” the large next ticket card, and the prominent “Call Next” button make the immediate task clear.

2. **Is the ticket status always visible where the person needs it?**  
   Yes. Each queue row has a centered Waiting or Called badge, and the next ticket is shown separately above the table.

3. **Do the words match what people in my setting actually say?**  
   Yes. “Call Next,” “Serve,” and “No-show” match the revised persona's plain-language examples. “Ticket” and the ticket number are also consistent with the resident view.

4. **Is the action the staff member does most often the easiest one to reach?**  
   Yes. “Call Next” is the largest primary button in the first card and is separated from the row-level actions. It is reachable before the staff member needs to scan the table.

5. **Does the phone version still show the most important thing first?**  
   Yes. On smaller screens the next ticket and Call Next action stack into a centered layout before the queue table. The table can scroll horizontally rather than making the important action unreadably narrow.

6. **Which “Because …, my interface must …” rules does this screen follow, and which does it break?**  
   It follows the rules requiring strong contrast, large controls, a single ordered queue, visible service and status, and plain action labels including “No-show.” It partially breaks the rule requiring arrival times: the table does not currently show when each person joined. No change is required for this review because the current queue order, ticket numbers, services, statuses, and primary Call Next action make the dashboard usable for the main staff workflow.

**Works well:** The Call Next card places the most frequent staff action above the table with the next resident's number, name, service, and mobile number, supporting recognition rather than recall.  
**Problem:** The queue does not show arrival times, so Mang Ernie cannot verify the order using the same evidence as residents. This is a consistency and match with the real world issue.  
**Change:** Keep the current wireframe. The ticket number provides a clear ordered queue for the current workflow, and adding another column would reduce readability on the shared tablet and phone layouts.
