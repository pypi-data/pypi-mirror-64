==============
Project Rename
==============

ProjectRename is a Django app to renaming the project of [boilerplate](https://github.com/jitender0514/django-boilerplate).

(Settings files name and strucure should be the same)

Requirements
------------

It required ``django-boilerplate`` [Project](https://github.com/jitender0514/django-boilerplate)

Quick start
-----------
1. Setup the ``django-boilerplate`` [Project](https://github.com/jitender0514/django-boilerplate) in your system.

2. Add "rename_project" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'project_rename',
    ]

3. Run ``python manage.py rename <New ProjectName>`` to rename the project.
