Powerline Gitstatus
===================

A [Powerline][1] segment for showing the status of a Git working copy.

By [Jasper N. Brouwer][2].

It will show the branch-name, or the commit hash if in detached head state.

It will also show the number of commits behind, commits ahead, staged files,
unmerged files (conflicts), changed files, untracked files and stashed files
if that number is greater than zero.

![screenshot][4]

Glossary
--------
- ``: branch name or commit hash
- `★`: most recent tag (if enabled)
- `↓`: n commits behind
- `↑`: n commits ahead
- `●`: n staged files
- `✖`: n unmerged files (conflicts)
- `✚`: n changed files
- `…`: n untracked files
- `⚑`: n stashed files

Requirements
------------

The Gitstatus segment requires [git][5]! Preferably, but not limited to, version 1.8.5 or higher.

Version 1.8.5 will enable the usage of the `-C` parameter, which is more performant and accurate.

Installation
------------

Installing the Gitstatus segment can be done with pip:

```txt
pip install powerline-gitstatus
```

The Gitstatus segment uses a couple of custom highlight groups. You'll need to define those groups in your colorscheme,
for example in `.config/powerline/colorschemes/default.json`:

```json
{
  "groups": {
    "gitstatus":                 { "fg": "gray8",           "bg": "gray2", "attrs": [] },
    "gitstatus_branch":          { "fg": "gray8",           "bg": "gray2", "attrs": [] },
    "gitstatus_branch_clean":    { "fg": "green",           "bg": "gray2", "attrs": [] },
    "gitstatus_branch_dirty":    { "fg": "gray8",           "bg": "gray2", "attrs": [] },
    "gitstatus_branch_detached": { "fg": "mediumpurple",    "bg": "gray2", "attrs": [] },
    "gitstatus_tag":             { "fg": "darkcyan",        "bg": "gray2", "attrs": [] },
    "gitstatus_behind":          { "fg": "gray10",          "bg": "gray2", "attrs": [] },
    "gitstatus_ahead":           { "fg": "gray10",          "bg": "gray2", "attrs": [] },
    "gitstatus_staged":          { "fg": "green",           "bg": "gray2", "attrs": [] },
    "gitstatus_unmerged":        { "fg": "brightred",       "bg": "gray2", "attrs": [] },
    "gitstatus_changed":         { "fg": "mediumorange",    "bg": "gray2", "attrs": [] },
    "gitstatus_untracked":       { "fg": "brightestorange", "bg": "gray2", "attrs": [] },
    "gitstatus_stashed":         { "fg": "darkblue",        "bg": "gray2", "attrs": [] },
    "gitstatus:divider":         { "fg": "gray8",           "bg": "gray2", "attrs": [] }
  }
}
```

Then you can activate the Gitstatus segment by adding it to your segment configuration,
for example in `.config/powerline/themes/shell/default.json`:

```json
{
    "function": "powerline_gitstatus.gitstatus",
    "priority": 40
}
```

The Gitstatus segment will use the `-C` argument by default, but this requires git 1.8.5 or higher.

If you cannot meet that requirement, you'll have to disable the usage of `-C`.
Do this by passing `false` to the `use_dash_c` argument, for example in `.config/powerline/themes/shell/__main__.json`:

```json
"gitstatus": {
    "args": {
        "use_dash_c": false
    }
}
```

Optionally the most recent tag reachable in the current branch can be shown.
You can enable this by passing `true` to the `show_tag` argument, for example in `.config/powerline/themes/shell/__main__.json`:

```json
"gitstatus": {
    "args": {
        "show_tag": true
    }
}
```

You can also specify any describe style that `git-prompt.sh` supports (via its `GIT_PS1_DESCRIBE_STYLE`) by passing `"contains"`, `"branch"`, `"describe"` or `"exact"` (which is `git-prompt.sh`'s `"default"`).
Git is executed an additional time to find this tag, so it is disabled by default.

License
-------

Licensed under [the MIT License][3].

[1]: https://powerline.readthedocs.org/en/master/
[2]: https://github.com/jaspernbrouwer
[3]: https://github.com/jaspernbrouwer/powerline-gitstatus/blob/master/LICENSE
[4]: https://github.com/jaspernbrouwer/powerline-gitstatus/blob/master/screenshot.png
[5]: https://git-scm.com/
