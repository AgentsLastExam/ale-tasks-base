Read the word in `/home/user/input/word.txt` and write a greeting to
`/home/user/output/result.txt`.

The greeting must be exactly `hello`, then a space, then the word from the input
file, with no trailing newline.

Paths are written literally on purpose: they are inside the declared agent user's
home, so the unprivileged agent owns them without framework-side permission changes.
