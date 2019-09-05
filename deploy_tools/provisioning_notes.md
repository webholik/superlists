Provisioning a new site
=======================

## Required packages:

* nginx
* virtualenv + pip
* (python3 and git already installed on Azure Ubuntu)

## Nginx Virtual Host Config
* See nginx.template.conf
* replace SITENAME with the actual sitename e.g. (funkymachine.eastus.cloudapp.azure.com)

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME with site

## Folder structure

/home/ankit/
    sites/
        SITENAME/
            database/
            source/
            static/
            virtualenv/
