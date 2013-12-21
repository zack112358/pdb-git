"""
Add the revbreak and trevbreak commands to PDB
"""

import pdb
import collections
import glob


def do_revbreak(self, arg, temporary=False):
    """
    revbreak revspec[ in file][ where condition]
    Set a breakpoint on every line in the file which changed in the git
    revisions specified by revspec. The file argument globs shell-style using
    the glob module, allowing you to specify multiple files.

    With a condition, the expression must evaluate to true before the
    breakpoint is honored.

    For example,
    revbreak HEAD^^^..HEAD in baz.py
    would break on every line of baz.py that changed in the last three revs.

    The revspec argument is passed to the shell, which will parse it before
    handing it over to git rev-spec to enumerate revisions.

    Uncommitted changes are always included in the revisions broken on.
    """
    # err = self.set_break(filename, line, temporary, cond, funcname)
    # Example cmd:
    # revbreak revspec in files where cond 

    revspec, filename, cond = re.match(
        r"""
        ^\s*
        (.*?)
        (?:\s+in\s+(.*?))
        (?:\s+where\s+(.*?))
        \s*$
        """
        arg,
        re.VERBOSE,
    ).groups()

    revs = subprocess.check_output('git rev-list ' + revspec, shell=True)
    revs = [rev[:8] for rev in revs.split("\n")] + ['00000000']

    breakpoints = []
    
    files = glob.glob(filename)
    for filename in files:
        for line in subprocess.check_output(['git', 'annotate', filename]):
            if line[:8] in revs:
                annotation = re.match('r^(.*\))', line).group(1)
                line = int(re.match('(\d\+)\)', annotation).group(1))

                err = self.set_break(filename, line, temporary, cond, None)
                if err:
                    print >>self.stdout, '***', err
                else:
                    bp = self.get_breaks(filename, line)[-1]
                    breakpoints.append(bp)

    print >>self.stdout, "Created %d breakpoints" % (len(breakpoints))


def do_trevbreak(self, arg):
    """
    trevbreak is to revbreak as tbreak is to break
    """
    return do_revbreak(self, arg, temporary=True)
    

pdb.Pdb.do_revbreak = do_revbreak
pdb.Pdb.do_trevbreak = do_trevbreak

