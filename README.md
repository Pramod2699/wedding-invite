# Pramod & Shruti — Wedding Invitation

A digital wedding invitation, built to be shared as a link on WhatsApp.

**Live link:** https://pramod2699.github.io/wedding-invite/

## What's inside

1. Opening screen with Ganesha, श्री गणेशाय नमः and the invitation, then a sealed envelope that opens with a petal shower
2. Hero with the wedding illustration and names
3. Groom: Pramod Gunaware, son of Shri Balu Gunaware & Smt. Vijaya Gunaware
4. Bride: Shruti Kaldate, daughter of Shri Dhanraj Kaldate & Smt. Meera Kaldate
5. Save the date: scratch the gold card to reveal 30 December 2026, then a live countdown
6. 29 December: Engagement (5:00 pm) and Haldi, with Add to calendar
7. 30 December: Wedding (5:45 pm), with Add to calendar
8. Venue (Shivkamal Lawns, Google Maps link) and an RSVP form that opens WhatsApp
- Background music (`audio/music.mp3`) starts when the envelope is opened, with a pause button top right
- Link preview image and title for WhatsApp (`og.jpg`)
- "Our story" section is turned off (commented out in `index.html`)

## Personal links

Add `?to=` with the guest's name to greet them on the envelope and pre-fill their RSVP:

https://pramod2699.github.io/wedding-invite/?to=Rahul%20Kaka

Use `%20` for spaces.

## Editing

- RSVP WhatsApp number: `RSVP_NUMBER` near the top of the script in `index.html`
- Scene captions: the `.chapter` blocks in `index.html`
- Images live in `img/`
