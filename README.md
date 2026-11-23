# Pramod & Shruti — Wedding Invitation

A digital wedding invitation, built to be shared as a link on WhatsApp.

**English:** https://pramod2699.github.io/wedding-invite/

**Marathi:** https://pramod2699.github.io/wedding-invite/mr/

## What's inside

1. Opening screen with Ganesha, श्री गणेशाय नमः and the invitation, then a sealed envelope that opens with a petal shower
2. Hero with the wedding illustration and names
3. The Groom: Pramod, son of Sau. Vijaya & Shri Balasaheb Manik Gunaware
4. The Bride: Shruti, daughter of Sau. Meera & Shri Dhanraj Ramdas Kaldate
5. Save the date: scratch the gold card to reveal 30 December 2026, then a live countdown
6. 29 December: Engagement (5:00 pm), with Add to calendar
7. 29 December: Haldi (after the engagement, onwards), with Add to calendar
8. 30 December: Wedding (5:45 pm), with Add to calendar
10. Venue (Shivkamal Lawns, Google Maps link)
11. Closing note from Pramod & Shruti and the Gunaware & Kaldate families
- Background music (`audio/music.mp3`) starts when the envelope is opened, with a pause button top right
- Auto-scroll: 8 seconds per page after opening, ends on the closing note, pauses when the guest touches or scrolls; pause/play button top right
- Link preview image and title for WhatsApp (`og.jpg`)
- "Our story" section is turned off (commented out in `index.html`)

## Personal links

Add `?to=` with the guest's name to greet them on the envelope:

https://pramod2699.github.io/wedding-invite/?to=Rahul%20Kaka

Use `%20` for spaces.

## Editing

- Scene captions: the `.chapter` blocks in `index.html`
- Images live in `img/`

## Marathi version

`mr/index.html` is generated from `index.html`. After changing the English page, rebuild it:

    python3 tools/build_mr.py

The script holds every translation next to the English text it replaces and stops with a message if any English phrase has changed, so the two versions stay in step. Each opening screen links to the other language and keeps the guest's `?to=` name.
