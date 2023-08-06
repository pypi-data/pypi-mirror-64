# Django Groups Sync


## Overview

A set of management commands to export and sync Django User Groups permissions between environments.


## Getting It

```
$ pip install django-groups-sync
```

If you want to install it from source, grab the git repository from GitHub and run setup.py:

```
$ git clone git://github.com/hansek/django-groups-sync.git
$ cd django-groups-sync
$ python setup.py install
```

## Installing It

To enable `groups_sync` in your project you need to add it to `INSTALLED_APPS` in your projects
`settings.py` file:

```
INSTALLED_APPS = (
    ...
    'groups_sync',
    ...
)
```

### Settings

* **GROUP_SYNC_FILENAME**

  Filename (and location) of JSON file for export/sync, default value `groups_permissions.json`.


## Usage

There are two management commands.

If you dont want anything to be displayed on stdout use verbosity argument `-v0`

### Export groups permissions

It will save all groups permissions from database to json file. 

```
$ python manage.py export_groups_permissions
```

**Arguments**

   * one or multiple group names you only want to include in the export data

         $ python manage.py export_groups_permissions "Group 1" "Group 2"

   * `--file` - specifies file to which the output is written (default value by `GROUP_SYNC_FILENAME`)


### Synchronize groups permissions

It will update database groups permissions by content of json file.

```
$ python manage.py sync_groups_permissions
```

**Arguments**

   * A Group name(s) which should only be synchronized (use "" if there are spaces in Group name).

         $ python manage.py export_groups_permissions "Group 1" "Group 2"

   * `--file` - specifies json data file (default value by `GROUP_SYNC_FILENAME`)

   * `--noinput` or `--no-input` - do NOT prompt the user for input of any kind

   * `--dry-run` or `-n` - do everything except modify the database


## Credits

Inspired by [Dan's Cheat Sheets > Permissions](https://cheat.readthedocs.io/en/latest/django/permissions.html).


Cheers 