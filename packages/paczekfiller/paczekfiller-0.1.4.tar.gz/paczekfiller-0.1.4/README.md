# Pączek filler

This tool tries to fill in a space next to `cookiecutter`, giving the user ability to
reuse functionality stored in a single file across different projects.

Setup a folder with files you reuse in your project.
Set the `PACZEK_FILLINGS` environment variable to point that folder.
Run `paczek` - will display list of files from which you can choose a file
that will be put in your current directory.
If the file ends with `.tpl` you will be asked for values that will be put inside
the template.

Please remember, redundancy can be removed and files can me merged
using git.

## Requirements

- [fzf](https://github.com/junegunn/fzf Fuzzy Search for command line

## Usage

There are two commands:

- `paczek`
- `paczekfiller <template_filepath> <target_filepath>`

### paczek

`paczek` is a script that uses `fzf` to prodive you with a list of template files, from your template files folder.

If the file has extension `tpl`, then it is passed to `paczekfiller`. `paczekfiller` detects Jinja2 variables in that
file, asks you to provide values for then. Finally, it substitutes the variables with the value and saves the
file in your current directory with the the file name without `tpl`.

If the file is without `.tpl`, then `paczek` copies it to your current folder, using `cp`

### paczekfiller

`paczekfiller` fills out a jinja2 template file and saves it under given target filepath.

`<template_filepath>` is an absolute path.

### config

Environment variables used by command `paczek`:

- `PACZEK_FILLINGS` stores path to folder with template files

### templates

Variables are extracted from templates. Variables names are
used in user prompt. The "\_" are changed into spaces (" ").

So, for a variable `{{Some_variable}}`, script will prompt user with
this: `Some variable:`

## Installation

`pip install paczekfiller`

## Licence

MIT type.

## Authors

`paczekfiller` was written by `Kris Urbanski <kris@whereibend.space>`\_.
