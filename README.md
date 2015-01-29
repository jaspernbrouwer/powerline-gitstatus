Powerline Gitstatus
===================

A [Powerline][1] segment for showing the status of a Git working copy.

By [Jasper N. Brouwer][2].

It will show the branch-name, or the commit hash if in detached head state.

It will also show the number of commits behind, commits ahead, staged files,
unmerged files (conflicts), changed files, untracked files and stashed files
if that number is greater than zero.

![screenshot][4]

Installation
------------

Installing the Gitstatus segment can be done with pip:

```txt
pip install powerline-gitstatus
```

The Gitstatus segment uses a couple of custom highlight groups. You'll need to define those groups in your colorscheme,
for example in `.config/powerline/colorschemes/default.json`:

```json
"gitstatus":                 { "fg": "gray8",           "bg": "gray2", "attrs": [] },
"gitstatus_branch":          { "fg": "gray8",           "bg": "gray2", "attrs": [] },
"gitstatus_branch_clean":    { "fg": "green",           "bg": "gray2", "attrs": [] },
"gitstatus_branch_dirty":    { "fg": "gray8",           "bg": "gray2", "attrs": [] },
"gitstatus_branch_detached": { "fg": "mediumpurple",    "bg": "gray2", "attrs": [] },
"gitstatus_behind":          { "fg": "gray10",          "bg": "gray2", "attrs": [] },
"gitstatus_ahead":           { "fg": "gray10",          "bg": "gray2", "attrs": [] },
"gitstatus_staged":          { "fg": "green",           "bg": "gray2", "attrs": [] },
"gitstatus_unmerged":        { "fg": "brightred",       "bg": "gray2", "attrs": [] },
"gitstatus_changed":         { "fg": "mediumorange",    "bg": "gray2", "attrs": [] },
"gitstatus_untracked":       { "fg": "brightestorange", "bg": "gray2", "attrs": [] },
"gitstatus_stashed":         { "fg": "darkblue",        "bg": "gray2", "attrs": [] }
```

Finally you can activate the Gitstatus segment by adding it to your segment configuration,
for example in `.config/powerline/themes/shell/default.json`:

```json
{
    "function": "powerline_gitstatus.gitstatus",
    "priority": 40
}
```

License
-------

Lincensed under [the MIT License][3].

[1]: https://powerline.readthedocs.org/en/master/
[2]: https://github.com/jaspernbrouwer
[3]: https://github.com/jaspernbrouwer/powerline-gitstatus/blob/master/LICENSE
[4]: https://github.com/jaspernbrouwer/powerline-gitstatus/blob/master/screenshot.png
