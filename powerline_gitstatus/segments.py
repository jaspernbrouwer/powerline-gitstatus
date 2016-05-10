# vim:fileencoding=utf-8:noet

from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info
from subprocess import PIPE, Popen
import os, re, string


@requires_segment_info
class GitStatusSegment(Segment):

    def execute(self, pl, command):
        pl.debug('Executing command: %s' % ' '.join(command))

        proc = Popen(command, stdout=PIPE, stderr=PIPE)
        out, err = [item.decode('utf-8') for item in proc.communicate()]

        if out:
            pl.debug('Command output: %s' % out.strip(string.whitespace))
        if err:
            pl.debug('Command errors: %s' % err.strip(string.whitespace))

        return (out.splitlines(), err.splitlines())

    def get_base_command(self, cwd, use_dash_c):
        if use_dash_c:
            return ['git', '-C', cwd]

        while cwd and cwd != os.sep:
            gitdir = os.path.join(cwd, '.git')

            if os.path.isdir(gitdir):
                return ['git', '--git-dir=%s' % gitdir, '--work-tree=%s' % cwd]

            cwd = os.path.dirname(cwd)

        return None

    def parse_branch(self, line):
        if not line:
            return ('', False, 0, 0)

        if line.startswith('## '):
            line = line[3:]

        match = re.search('^Initial commit on (.+)$', line)
        if match is not None:
            return (match.group(1), False, 0, 0)

        match = re.search('^(.+) \(no branch\)$', line)
        if match is not None:
            return (match.group(1), True, 0, 0)

        match = re.search('^(.+?)\.\.\.', line)
        if match is not None:
            branch = match.group(1)

            match = re.search('\[ahead (\d+), behind (\d+)\]$', line)
            if match is not None:
                return (branch, False, int(match.group(2)), int(match.group(1)))
            match = re.search('\[ahead (\d+)\]$', line)
            if match is not None:
                return (branch, False, 0, int(match.group(1)))
            match = re.search('\[behind (\d+)\]$', line)
            if match is not None:
                return (branch, False, int(match.group(1)), 0)

            return (branch, False, 0, 0)

        return (line, False, 0, 0)

    def parse_status(self, lines):
        staged    = len([True for l in lines if l[0] in 'MRC' or (l[0] == 'D' and l[1] != 'D') or (l[0] == 'A' and l[1] != 'A')])
        unmerged  = len([True for l in lines if l[0] == 'U' or l[1] == 'U' or (l[0] == 'A' and l[1] == 'A') or (l[0] == 'D' and l[1] == 'D')])
        changed   = len([True for l in lines if l[1] == 'M' or (l[1] == 'D' and l[0] != 'D')])
        untracked = len([True for l in lines if l[0] == '?'])

        return (staged, unmerged, changed, untracked)

    def build_segments(self, branch, detached, tag, behind, ahead, staged, unmerged, changed, untracked, stashed):
        if detached:
            branch_group = 'gitstatus_branch_detached'
        elif staged or unmerged or changed or untracked:
            branch_group = 'gitstatus_branch_dirty'
        else:
            branch_group = 'gitstatus_branch_clean'

        segments = [
            {'contents': u'\ue0a0 %s' % branch, 'highlight_groups': [branch_group, 'gitstatus_branch', 'gitstatus'], 'divider_highlight_group': 'gitstatus:divider'}
        ]

        if tag:
            segments.append({'contents': u' \u2605 %s' % tag, 'highlight_groups': ['gitstatus_tag', 'gitstatus'], 'divider_highlight_group': 'gitstatus:divider'})
        if behind:
            segments.append({'contents': ' ↓ %d' % behind, 'highlight_groups': ['gitstatus_behind', 'gitstatus'], 'divider_highlight_group': 'gitstatus:divider'})
        if ahead:
            segments.append({'contents': ' ↑ %d' % ahead, 'highlight_groups': ['gitstatus_ahead', 'gitstatus'], 'divider_highlight_group': 'gitstatus:divider'})
        if staged:
            segments.append({'contents': ' ● %d' % staged, 'highlight_groups': ['gitstatus_staged', 'gitstatus'], 'divider_highlight_group': 'gitstatus:divider'})
        if unmerged:
            segments.append({'contents': ' ✖ %d' % unmerged, 'highlight_groups': ['gitstatus_unmerged', 'gitstatus'], 'divider_highlight_group': 'gitstatus:divider'})
        if changed:
            segments.append({'contents': ' ✚ %d' % changed, 'highlight_groups': ['gitstatus_changed', 'gitstatus'], 'divider_highlight_group': 'gitstatus:divider'})
        if untracked:
            segments.append({'contents': ' … %d' % untracked, 'highlight_groups': ['gitstatus_untracked', 'gitstatus'], 'divider_highlight_group': 'gitstatus:divider'})
        if stashed:
            segments.append({'contents': ' ⚑ %d' % stashed, 'highlight_groups': ['gitstatus_stashed', 'gitstatus'], 'divider_highlight_group': 'gitstatus:divider'})

        return segments

    def __call__(self, pl, segment_info, use_dash_c=True, show_tag=False):
        pl.debug('Running gitstatus %s -C' % ('with' if use_dash_c else 'without'))

        cwd = segment_info['getcwd']()

        if not cwd:
            return

        base = self.get_base_command(cwd, use_dash_c)

        if not base:
            return

        status, err = self.execute(pl, base + ['status', '--branch', '--porcelain'])

        if err and ('error' in err[0] or 'fatal' in err[0]):
            return

        branch, detached, behind, ahead = self.parse_branch(status.pop(0))

        if not branch:
            return

        if branch == 'HEAD':
            branch = self.execute(pl, base + ['rev-parse', '--short', 'HEAD'])[0][0]

        staged, unmerged, changed, untracked = self.parse_status(status)

        stashed = len(self.execute(pl, base + ['stash', 'list', '--no-decorate'])[0])

        if show_tag:
            tag, err = self.execute(pl, base + ['describe', '--tags', '--abbrev=0'])

            if err and ('error' in err[0] or 'fatal' in err[0]):
                tag = ''
            else:
                tag = tag[0]
        else:
            tag = ''

        return self.build_segments(branch, detached, tag, behind, ahead, staged, unmerged, changed, untracked, stashed)


gitstatus = with_docstring(GitStatusSegment(),
'''Return the status of a Git working copy.

It will show the branch-name, or the commit hash if in detached head state.

It will also show the number of commits behind, commits ahead, staged files,
unmerged files (conflicts), changed files, untracked files and stashed files
if that number is greater than zero.

:param bool use_dash_c:
    Call git with ``-C``, which is more performant and accurate, but requires git 1.8.5 or higher.
    Otherwise it will traverse the current working directory up towards the root until it finds a ``.git`` directory, then use ``--git-dir`` and ``--work-tree``.
    True by default.

:param bool show_tag:
    Show the most recent tag reachable in the current branch.
    False by default, because it needs to execute git an additional time.

Divider highlight group used: ``gitstatus:divider``.

Highlight groups used: ``gitstatus_branch_detached``, ``gitstatus_branch_dirty``, ``gitstatus_branch_clean``, ``gitstatus_branch``, ``gitstatus_tag``, ``gitstatus_behind``, ``gitstatus_ahead``, ``gitstatus_staged``, ``gitstatus_unmerged``, ``gitstatus_changed``, ``gitstatus_untracked``, ``gitstatus_stashed``, ``gitstatus``.
''')
