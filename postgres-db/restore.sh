#!/usr/bin/sh

pg_restore -U postgres -W -d al_test ./slit.sql 
