#!/usr/bin/env bash
cd $(dirname $0)
bin/buildout -Nc buildout-prod.cfg install instance
cp etc/wsgi/instance.ini production.ini
bin/buildout -Nc buildout-dev.cfg  install instance
cp etc/wsgi/instance.ini development.ini
sed -re "s:$PWD:%(here)s:g" -i production.ini development.ini


