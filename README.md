pdb-git
=======

Extensions to pdb.py that add commands which use git information.


Here's a story we've all lived. It goes like this:

"Oh, I have a bug in the foo module."
"Here, I'll fix the foo-module bug."
"Wait, baz is broken? I didn't even know baz *called* foo!"

What if I just want to know what I changed? What I broke? What changes are live
in the code path for this particular call? How do I do that?

This is an extension to PDB that allows you to set a breakpoint based on git
revisions. The debugger will break when it reaches a line that was last changed
in the specified set of git revisions. This lets you run the bugging function in
PDB and interactively debug only the parts of the code that you changed.
