# Week 3 accessibility checks

The checks below cover all three screens: **Join queue**, **My place**, and
**Staff dashboard**.

## 9a. Lighthouse

The Lighthouse accessibility score was initially **82–84**. After replacing
the Bootstrap assets with their minimized versions (`.min.js`), the score improved to
**90–92**.

## 9b. Keyboard

All three screens can be used with a keyboard only. Tab moves through the
navigation links, controls, forms, actions, and pagination. The focused
control is visibly identifiable. The mobile navigation toggle is also
keyboard reachable.

## Manual checklist

| Check | Join | My place | Staff |
| --- | --- | --- | --- |
| Every input has a visible label | ✅ Name, Mobile Number, and Service have associated labels. | ✅ No user input fields on this screen. | ✅ The Service filter has an associated label. |
| Error messages say what to do, in text | ✅ Validation messages say exactly what to enter or choose. | ✅ No validation input on this screen. | ✅ No user-entered fields requiring validation on this screen. |
| Status is shown in words, not only color | ✅ No queue status is needed before joining. | ✅ Waiting, Called, Served, and No-show are written in the status badge. | ✅ Waiting and Called are written in each status badge. |
| Text and buttons are readable at 375 px with no sideways page scroll | ✅ Verified at 375 px with no document overflow. | ✅ Verified at 375 px with no document overflow. | ✅ Verified at 375 px with no document overflow; only the table region scrolls horizontally when needed. |
| Buttons are at least about 44 × 44 px on a phone | ✅ The navigation toggle and Get a ticket button are at least 44 px high. | ✅ The navigation toggle and Leave the queue button are at least 44 px high. | ✅ Call Next, Serve, No-show, pagination links, and the navigation toggle are at least 44 px high. |
| Page has one `<h1>` and headings in order | ✅ One h1: Join the queue. | ✅ One h1: the selected service name. | ✅ One h1: Staff Dashboard; the next ticket name and queue title use h2. |
| `<html lang="en">` (or your language) is set | ✅ `lang="en"` is set in the shared layout. | ✅ `lang="en"` is set in the shared layout. | ✅ `lang="en"` is set in the shared layout. |

## Fixes

- Replaced bootstrap assets to their minimized versions.
- Changed the staff next-ticket name from a second `<h1>` to `<h2>` so the
  staff page has one clear top-level heading.
- Increased staff row action buttons to a minimum height of `2.75rem`
  (44px).
- Increased pagination links and the mobile navigation toggle to a minimum
  height of `2.75rem`.
