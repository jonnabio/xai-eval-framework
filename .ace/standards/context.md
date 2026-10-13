# Session Context Standards

> How `docs/context/ACTIVE_CONTEXT.md` and its archive are read and kept.
> Added 2026-10-12, when the file had grown to 5,300 lines and could no longer be
> read in one pass. Enforced by `scripts/pubs/check_active_context.py` (CI, `pubs-sync`).

---

## CTX-1: `ACTIVE_CONTEXT.md` holds the current state only

- Its first lines name the archive and this standard.
- It holds: the current objective, the publication status, the repository state, what
  is open with the author, the active constraints, and **one** handoff, the latest.
- Limit: **300 lines**.
- A statement that is no longer true is corrected or removed in place. It is not kept
  with a note that a later line supersedes it.

## CTX-2: history goes to the archive, verbatim

- The archive is `docs/context/archive/`: one file per day (`YYYY-MM-DD.md`) and an
  index, `README.md`, that lists every file with the titles of its sections.
- At the end of a session:
  1. Move the handoff that is in `ACTIVE_CONTEXT.md` to the archive file of its date,
     unchanged, above the sections already there. Create the file if there is none.
  2. Add the section title to the index.
  3. Write the new handoff in its place and bring the state sections up to date.
- Archive files are dated records. They are not edited afterwards, except to add a
  section moved from `ACTIVE_CONTEXT.md`.
- Both files are shared paths: they are committed apart from lane files and reach
  `main` in the session (ADR-0013).

## CTX-3: read the archive when the task needs it

`ACTIVE_CONTEXT.md` is read at every session start. The archive is **not** read by
default. Read it before acting when any of these holds:

1. The task concerns a paper, lane, experiment, decision or file that
   `ACTIVE_CONTEXT.md` names without giving the detail the task needs, or sends to the
   archive for.
2. A past decision is about to be changed, repeated or contradicted: a venue, a scope,
   a retired value, a rule the author set, a result already analysed.
3. A journal or reviewer has answered, and the reply needs what was submitted, how it
   was built, or its known limits.
4. The author asks what was done, when, or why.
5. A state in the repository is not explained by `ACTIVE_CONTEXT.md`: an unknown
   branch, a file no one claims, a failing check, a number with no origin.

How to read it:

1. Read `docs/context/archive/README.md` and choose the file by date and title.
2. For a term (a commit, a file name, a finding number), search the archive directory
   for it; do not read the files in turn.
3. Read only the sections found. Where the archive and `ACTIVE_CONTEXT.md` differ,
   `ACTIVE_CONTEXT.md` holds; if the archive looks right and the state file wrong, tell
   the author before acting.

Do not state that something was or was not done from `ACTIVE_CONTEXT.md` alone when the
answer would be in the archive.
