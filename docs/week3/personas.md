## Mika Santos, the person waiting

> "I come down with my basket and there are already six others on the floor, and nobody knows whose turn it is." (interview)

| | |
| --- | --- |
| **Photo or sketch** | ![Photo of Mika](./screenshots/persona_mika.jpg) |
| **Age, role and background** | 20, 3rd-year nursing student living in a dormitory. Her class and hospital duty schedule changes every week, so she can only do laundry in short gaps. |
| **Goals** | 1. Get a place in line for the service she needs (wash and dry, wash only, or dry only) without wasting a free hour.<br>2. Know roughly when her turn will come so she can go back to her room and study.<br>3. Be sure nobody cuts in front of her. |
| **Frustrations** | 1. Baskets left on the floor or on machines mark the "queue", and nobody agrees on the order (observation).<br>2. She walks down three floors, finds no free machine, and has to walk back up and try again (interview).<br>3. She can't tell how long she will wait, so she either stands around or risks missing her turn (interview). |
| **Devices and context** | Her own Android phone, on mobile data that is often slow or used up. She uses it in her room, in the stairwell, or in the laundry area while carrying a basket with one hand. |
| **Tech comfort** | High. She uses banking, ride and school apps daily, but she has little patience for apps that need sign-up or many taps. |
| **Accessibility needs** | One hand is often busy holding a basket, so large tap targets are needed. Slow or limited mobile data means pages must load fast and use little data. The laundry room is loud, so sound alerts alone are not enough; she needs a visible and vibrating notification. |

### Scenario

It is 6:40 on a Tuesday evening and Mika has a free hour before her duty briefing. She carries her basket toward the laundry room and sees most machines running and several baskets on the floor. Instead of guessing, she stops at the door, scans the posted QR code, picks "Wash and dry", types her name, and taps "Get queue number". The app tells her she is number 4 and that about 25 minutes remain. She puts her basket on the rack and goes back to her room to review her notes. When she is next, her phone vibrates and the app shows "You're next, please come in within 5 minutes." She returns, loads a washer, and leaves the queue.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Get a queue number for Wash and dry, Wash only, or Dry only | Join queue | FR-01 |
| Check position and estimated wait | My place | FR-02 |
| Get an alert when her turn is near | My place | FR-03 |
| Leave the queue voluntarily or when served | My place | FR-04 |

### What this means for my interface

1. Because Mika often carries a basket with one hand, my interface must let her get a queue number with three large choices (Wash and dry, Wash only, Dry only) and a name, with no account or sign-up.
2. Because her mobile data is slow and limited, my interface must load a lightweight "My place" screen that shows her number, position and wait first, with no heavy images or animations.
3. Because the laundry room is loud and she leaves to study, my interface must alert her with a visible message and vibration, not sound alone, and show a clear time limit to come back.
4. Because she can't tell how long she will wait (interview), my interface must show her position and estimated wait in large, plain numbers at the top of the screen.

---

## Mang Ernie Dela Cruz, the staff member

> "All day they ask me 'Am I next? Am I next?' while I'm trying to load and unload the machines." (interview)

| | |
| --- | --- |
| **Photo or sketch** | ![Photo of Mang Ernie](./screenshots/persona_ernie.jpg) |
| **Age, role and background** | 52, laundry attendant and dorm utility staff. He has worked at the facility for eight years and manages the room from 3 pm to 10 pm, including collecting payments and fixing machine jams. |
| **Goals** | 1. Serve people in a fair order, matched to what they need (wash and dry, wash only, or dry only), without arguments.<br>2. Spend less time answering "whose turn is it?" and more time keeping machines running.<br>3. Handle people who don't show up without losing track of the line. |
| **Frustrations** | 1. Students argue over who arrived first, and he is the one blamed (interview).<br>2. He keeps a handwritten list on a notebook page that gets wet, lost or messy (observation).<br>3. People walk away after being called, so he waits and then has to decide what to do with their place (observation). |
| **Devices and context** | A shared tablet, phone (or the desk PC) at the counter. His hands are often wet or holding clothes, he stands up often, and the room is hot and noisy. |
| **Tech comfort** | Low to medium. He uses Facebook Messenger and a basic phone daily, but he is not confident with new apps and worries about making a mistake that nobody can undo. |
| **Accessibility needs** | Older eyes need large text and strong contrast. Wet or gloved fingers need large buttons with space between them to avoid wrong taps. A shared device means the screen must work in bright light and a noisy room. Labels should be in plain language, not technical terms. |

### Scenario

It is a busy Sunday afternoon and eight people are waiting while Mang Ernie unloads a dryer. He glances at the counter tablet, where the staff dashboard is already open and shows each person's name, service and arrival time. A dryer is now free and the dashboard shows "Next: Jun, #3, Dry only" in large text, so he taps "Call next" and Jun's phone is notified. Five minutes later Jun has not arrived, so he taps "Remove" and the app marks him as a no-show. Then Jun comes up the stairs, so Mang Ernie taps "Undo" and Jun's place is restored. After Jun's clothes are now in the machine, Mang Ernie taps "Mark as served" which then removes Jun's place in the queue. He goes back to the machines without writing anything in his notebook.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| See the full queue in order, with each person's service | Staff dashboard | FR-05 |
| Call the next person | Staff dashboard | FR-06 |
| Skip or remove a no-show, mark someone as served, with undo | Staff dashboard | FR-07 |

### What this means for my interface

1. Because Mang Ernie has wet hands and older eyes, my interface must use large text, strong contrast and big buttons spaced far apart on the counter tablet.
2. Because he is blamed for unfair order (interview), my interface must show the queue in a single, clear order with arrival times and the service each person needs, so everyone can see the same list.
3. Because people walk away after being called (observation), my interface must let him remove a no-show in one tap and show a clear status for each person (waiting, called, no-show).
4. Because he is not confident with new apps, my interface must use plain words ("Call", "Mark as served", "Remove"), and offer an easy undo for removing someone.