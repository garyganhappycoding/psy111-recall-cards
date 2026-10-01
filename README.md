# PSY 111 Recall Cards

Tap-to-reveal study cards and paraphrase tables for PSY 111 at HELP University.

Topics: Personality 1, Personality 2, Motivation, Emotion, Intelligence.

- `index.html` — the whole app (no build step)
- `cards.json` — the card deck (`deck`, `sec`, `name`, `clues`, `ans`; one answer point per line)

To change the default cards for everyone, edit `cards.json` and push — Vercel redeploys automatically.

## Accounts

Sign-in uses Supabase email codes (project `psy111-recall-cards`). Each signed-in user's revealed cards,
paraphrase drafts and card edits are stored in the `user_state` table, protected by row-level security so
people can only read and write their own row. Signed-out visitors save in their browser only.

Supabase dashboard settings this relies on:
- Authentication → URL Configuration: Site URL and Redirect URLs set to the Vercel domain
- Authentication → Email Templates → Magic Link: includes `{{ .Token }}` so the email shows a code
- For more than a few sign-ups an hour, add custom SMTP (Authentication → SMTP Settings)
