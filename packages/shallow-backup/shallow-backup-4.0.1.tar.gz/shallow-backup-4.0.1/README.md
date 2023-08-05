# shallow-backup

[![Downloads](http://pepy.tech/badge/shallow-backup)](http://pepy.tech/count/shallow-backup)
[![Build Status](https://travis-ci.com/alichtman/shallow-backup.svg?branch=master)](https://travis-ci.com/alichtman/shallow-backup)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1719da4d7df5455d8dbb4340c428f851)](https://www.codacy.com/app/alichtman/shallow-backup?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=alichtman/shallow-backup&amp;utm_campaign=Badge_Grade)
<!-- [![Coverage Status](https://coveralls.io/repos/github/alichtman/shallow-backup/badge.svg?branch=master)](https://coveralls.io/github/alichtman/shallow-backup?branch=master) -->

`shallow-backup` lets you easily create lightweight backups of installed packages, applications, fonts and dotfiles, and automatically push them to a remote Git repository.

![Shallow Backup GIF Demo](img/shallow-backup-demo.gif)

Contents
========

 * [Installation](#installation)
 * [Usage](#usage)
 * [Git Integration](#git-integration)
 * [What can I back up?](#what-can-i-back-up)
 * [Backup Customization](#backup-customization)
 * [Output Structure](#output-structure)
 * [Reinstalling Dotfiles](#reinstalling-dotfiles)
 * [Inspiration](#inspiration)
 * [Want to contribute?](#want-to-contribute)

### Installation
---

1. Install with [`pip3`](https://pypi.org/project/shallow-backup/)
    + `$ pip3 install shallow-backup`
    + `$ shallow-backup`

2. Download the `shallow-backup` binary from Releases tab.

### Usage
---

To start the interactive program, simply run `$ shallow-backup`.

`shallow-backup` was built with scripting in mind. Every feature that's supported in the interactive program is supported with command line args.

```shell
Usage: shallow-backup [OPTIONS]

  Easily back up installed packages, dotfiles, and more.
  You can edit which files are backed up in ~/.shallow-backup.

  Written by Aaron Lichtman (@alichtman).

Options:
  --add_dot                Add a dotfile or dotfolder to config by path.
  -all                     Full back up.
  -configs                 Back up app config files.
  -delete_config           Delete config file.
  -destroy_backup          Delete backup directory.
  -dotfiles                Back up dotfiles.
  -fonts                   Back up installed fonts.
  --new_path TEXT          Input a new back up directory path.
  -no_splash               Don't display splash screen.
  -old_path                Skip setting new back up directory path prompt.
  -packages                Back up package libraries.
  -reinstall_all           Full reinstallation.
  -reinstall_configs       Reinstall configs.
  -reinstall_dots          Reinstall dotfiles and dotfolders.
  -reinstall_fonts         Reinstall fonts.
  -reinstall_packages      Reinstall packages.
  --remote TEXT            Set remote URL for the git repo.
  -separate_dotfiles_repo  Use if you are trying to maintain a separate
                           dotfiles repo and running into issue #229.
  -show                    Display config file.
  -v, --version            Display version and author info.
  -help, -h, --help        Show this message and exit.
```

### Git Integration
---

**A Word of Caution**

This backup tool is git-integrated, meaning that you can easily store your backups remotely (on GitHub, for example.) Dotfiles and configuration files may contain sensitive information like API keys and ssh keys, and you don't want to make those public. To make sure no sensitive files are uploaded accidentally, `shallow-backup` creates a `.gitignore` file if it can't find one in the directory. It excludes `.ssh/` and `.pypirc` by default. It's safe to remove these restrictions if you're pushing to a remote private repository, or you're only backing up locally. To do this, you should clear the `.gitignore` file without deleting it.

_If you choose to back up to a public repository, look at every file you're backing up to make sure you want it to be public._

**What if I'd like to maintain a separate repo for my dotfiles?**

`shallow-backup` makes this easy! After making your first backup, `cd` into the `dotfiles/` directory and run `$ git init`. Create a `.gitignore` and a new repo on your favorite version control platform. This repo will be maintained independently (manually) of the base `shallow-backup` repo. Note that you may need to use the `-separate_dotfiles_repo` flag to get this to work, and it may [break some other functionality of the tool](https://github.com/alichtman/shallow-backup/issues/229). It's ok for my use case, though.

Here's a `bash` script that I wrote to automate my dotfile backup workflow. You can use this by placing it in your `~/.zshrc` or `~/.bashrc`, sourcing the file, and then running `$ backup-dots`.

```bash
# Usage: backup-dots [COMMIT MESSAGE]
backup-dots () {
	echo "Backing up..."
	crontab -l > ~/.config/crontab
	(
		shallow-backup -no_splash -dotfiles -separate_dotfiles_repo
		cd "$HOME/shallow-backup/dotfiles/" || exit
		hub stash
		hub pull
		hub stash pop
		hub add .
		commit_msg="$1" 
		if [ -z "$commit_msg" ]
		then
			hub commit --verbose
		else
			hub commit -m "$commit_msg"
		fi
		hub push
	)
}

```

### What can I back up?
---

By default, `shallow-backup` backs these up.

1. `dotfiles` and `dotfolders`.
    * `.bashrc`
    * `.bash_profile`
    * `.gitconfig`
    * `.pypirc`
    * `.config/shallow-backup.conf`
    * `.ssh/`
    * `.vim/`
    * `.zshrc`

2. App Config Files
    * Atom
    * VSCode
    * Sublime Text 2/3
    * Terminal.app

3. Installed Packages
    * `apm`
    * `brew` and `cask`
    * `cargo`
    * `gem`
    * `pip`
    * `pip3`
    * `npm`
    * `macports`
    * `VSCode` Extensions
    * `Sublime Text 2/3` Packages
    * System Applications

4. User installed `fonts`.

### Backup Customization

If you'd like to modify which files are backed up, you have to edit the `~/.config/shallow-backup.conf` file. There are two recommended ways of doing this.

1. Select the appropriate option in the CLI and follow the prompts.
2. Open the file in a text editor and make your changes.

#### .gitignore

As of `v4.0`, any `.gitignore` changes should be made in the `shallow-backup` config file. `.gitignore` changes that are meant to apply to all directories should be under the `root-gitignore` key. Dotfile specific gitignores should be placed under the `dotfiles-gitignore` key. The original `default-gitignore` key in the config is still supported for backwards compatibility, however, converting to the new config format is strongly encouraged.

#### Output Structure
---

```shell
backup_dir/
├── configs
│   ├── plist
│   │   └── com.apple.Terminal.plist
│   ├── sublime_2
│   │   └── ...
│   └── sublime_3
│       └── ...
├── dotfiles
│   ├── .bash_profile
│   ├── .bashrc
│   ├── .gitconfig
│   ├── .pypirc
│   ├── ...
│   ├── .shallow-backup
│   ├── .ssh/
│   │   └── known_hosts
│   ├── .vim/
│   └── .zshrc
├── fonts
│   ├── AllerDisplay.ttf
│   ├── Aller_Bd.ttf
│   ├── Aller_BdIt.ttf
│   ├── Aller_It.ttf
│   ├── ...
│   ├── Ubuntu Mono derivative Powerline Bold Italic.ttf
│   ├── Ubuntu Mono derivative Powerline Bold.ttf
│   ├── Ubuntu Mono derivative Powerline Italic.ttf
│   └── Ubuntu Mono derivative Powerline.ttf
└── packages
    ├── apm_list.txt
    ├── brew-cask_list.txt
    ├── brew_list.txt
    ├── cargo_list.txt
    ├── gem_list.txt
    ├── installed_apps_list.txt
    ├── npm_list.txt
    ├── macports_list.txt
    ├── pip_list.txt
    └── sublime3_list.txt
```

### Reinstalling Dotfiles

To reinstall your dotfiles, clone your dotfiles repo and make sure your shallow-backup config path can be found at either `~/.config/shallow-backup.conf` or `$XDG_CONFIG_HOME/.shallow_backup.conf`. Set the `backup-path` key in the config to the path of your cloned dotfiles. Then run `$ shallow-backup -reinstall_dots`.


When reinstalling your dotfiles, the top level `.git/`, `.gitignore`, `img/` and `README.md` files / directories are ignored.

### Inspiration
---

I back up system images of my MacBook Pro to an external SSD multiple times every week, and it always takes way too long. I wanted to speed this up, so I took a look at what was actually being backed up. I saw that my `brew`, `npm`, and `pip` libraries took up a ton more space than I imagined.

*And that's totally unnecessary.* When you back something up, you do it with the intention of being able to get back to that exact state at some point in the future. The minimum you need in order to recreate those package libraries later is just a list of the packages that are installed with each package manager. If you have these lists, restoring your system package installs is easy: `$ pip install -r pip_list.txt`, for example.

I cut down my backup size by almost `10GB` by replacing my `pip`, `brew`, `brew cask` and `npm` libraries with simple text files. I also cut down the back up time significantly since many fewer files were being copied.

Once I'd built that functionality, I wanted to have a single backup utility for files and folders often used by developers, so I added the ability to backup `dotfiles` and `fonts`. (Note: Because just having a list of installed fonts or a list of dotfiles that exist isn't very useful, `shallow-backup` creates copies of all dotfiles and user installed fonts.)

### Want to Contribute?
---

Check out `CONTRIBUTING.md` and the `docs` directory.
