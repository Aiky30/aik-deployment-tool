# aik-deployment-tool
Python deployment tool

This file allows a development environment to be built
Multiple production sites to be created, deployed and maintained

Install within a project using PIP
````
    pip install -e git+https://github.com/Aiky30/aik_deployment_tool.git#egg=aik_deployment_tool
````
TODO:
- Rollback:
    - copy previous code
    - copy previous virt env
    - copy previous deployment script???
    - DB
    .....
FIXME:
- The destroy method could potentially destroy all media files or any uploads, i would advise a move / copy with a date and then delete!!!
- The clean command should use the config files and code that first created all or else it won't clean properly, could create issues with bugfixes that arn't fixed. hmm, difficult
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