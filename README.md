# aik-deployment-tool
Python deployment tool

This file allows a development environment to be built
Multiple production sites to be created, deployed and maintained


FIXME: The destroy method could potentially destroy all media files or any uploads, i would advise a move / copy with a date and then delete!!!
```
Tasks:
    Build environment
    destroy environment

# Design
## Class Hierarchy

Environment

    (should switch which scripts to set the relevant import)

    set_config
    set_environment (set fabric to local or server)

    Services
        register_service (Apache, MySQL, PostGreSQL)
        restart_service

    Directory
        build_directories
        set_privileges

    Application
        setup
        install

```