# Pramod & Shruti — Wedding Invitation

A digital wedding invitation, built to be shared as a link on WhatsApp.

**Live link:** https://pramod2699.github.io/wedding-invite/

## What's inside

- Opening screen with Ganesha, श्री गणेशाय नमः and the invitation, then a sealed envelope that opens with a petal shower
- Full-screen illustrated hero with a live countdown to 30 December 2026, 5:45 pm
- "Our story" section (currently turned off; commented out in `index.html`)
- Schedule (Engagement and Haldi on 29 December, Wedding on 30 December) with Add to calendar links
- Venue card for Shivkamal Lawns with a Google Maps link
- RSVP form that opens WhatsApp with the reply pre-filled
- Link preview image and title for WhatsApp (`og.jpg`)

## Personal links

Add `?to=` with the guest's name to greet them on the envelope and pre-fill their RSVP:

https://pramod2699.github.io/wedding-invite/?to=Rahul%20Kaka

Use `%20` for spaces.

## Editing

- RSVP WhatsApp number: `RSVP_NUMBER` near the top of the script in `index.html`
- Scene captions: the `.chapter` blocks in `index.html`
- Images live in `img/`
