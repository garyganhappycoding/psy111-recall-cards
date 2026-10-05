# PSY 111 Recall Cards

Tap-to-reveal study cards and paraphrase tables for PSY 111 at HELP University.

Topics: Intro to Psychology (Module 0), Personality 1, Personality 2, Motivation, Emotion, Intelligence.

Modes: **Learning** (read the card, tap Done, then answer from memory), **Test** (answer straight away) and
**Quiz** (confirm, then every card in the current view as a 4-option question, with score and a retry for missed ones).
After revealing, mark each card Understand / Not sure / Totally forgot and filter by status to revise weak cards.

- `index.html` — the whole app (no build step)
- `cards.json` — the card deck (`deck`, `sec`, `name`, `clues`, `ans`; one answer point per line)

To change the default cards for everyone, edit `cards.json` and push — Vercel redeploys automatically.

## Source slides

When an answer is revealed, the lecture slide(s) it came from are shown underneath. Each card in `cards.json`
has `src: {f: <deck file>, p: [slide numbers]}`. The slide images in `slides/` are AES-GCM encrypted; the key
is held in Supabase (`recall_secrets`) and only returned by `recall_slide_key` to a signed-in session, so the
pictures only show for signed-in users. Signed-out visitors see the source label only.

## Accounts

People create an account with an email and password and can use it immediately — no confirmation email.
Accounts live in the Supabase project `psy111-recall-cards`:

- `recall_accounts` — email + bcrypt password hash
- `recall_sessions` — sign-in tokens (stored hashed)
- `recall_state` — each account's revealed cards, paraphrase drafts, card edits and card status
  (Understand / Not sure / Totally forgot) and previous answers (`attempts`). The page saves through `recall_save_state_v3`;
  the older `recall_save_state` and `_v2` are kept so nobody on an old copy of the page loses anything.

The tables have row-level security on with no policies, so the browser can't read them directly; the page
only talks to them through the `recall_*` database functions, which check the session token first.
Signed-out visitors save in their browser only.

Passwords can't be reset by email (there's no email step). To reset one, delete the row in
`recall_accounts` and the person can sign up again.
