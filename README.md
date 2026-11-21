# Cut the Sub

Grade 3 fractions interactive that goes with "The Party Sub" two-day lesson and the Fraction Sleeve Mat.

- **Compare mode:** kids predict which fraction is bigger, then two 24-bite subs fill from 0 to check.
- **Estimate mode:** kids cut a sub of random length at a target fraction, then watch equal hops from 0 show the true spot. Stars for accuracy; 5 strong cuts in a row unlocks the next level. Level 4 goes from 0 to 2.
- **Show my teacher:** end-of-session summary. Nothing is saved or sent anywhere.

One self-contained `index.html`, no external libraries, fonts, or tracking. Works on Chromebooks.

`slides/` holds the exact fraction visuals used in the Canva decks.

## Cut the Sub: Shop Shift

A bigger game version at `/shopshift/`: 4 weeks × 5 shifts as the sub business grows (deli → food truck → ballpark → catering a party). 20 voiced customers and 200 orders across nine order types: split it, cut it, who got more, same amount, leftovers, name the cut, check the rookie, two pieces, and line them up. The scaffold fades from a 24-box strip (like the Fraction Sleeve) to a marked number line, to 0 and 1 only, to nothing. Every Friday, Inspector Hale gives a 3-question check on a bare number line. Rush-hour speed tips (bonus only), surprise events, upgrades, and local saving.

- `shopshift/index.html` – the game (built from `src.html` with the order data inlined)
- `shopshift/art/` – customer cutouts and props (WebP)
- `shopshift/voice/` – voice clips (`<customer>_o1..o8`, `_happy1-2`, `_unsure1-2`); missing clips fall back to text
- `shopshift/tools/` – order generator and build script
