# checkmk-stasissqldump
Check_mk for stasis_sql_dump

# Check_mk plugin for stasis_sql_dump
# GPL (C) Lars Falk-Petersen <dev@falk-petersen.no>, 2014
#
# Check if a database server is running,
# and if so check that we have a valid backup.

* Check named stasissqldump.py
* Agent-plugin named stasissqldump
** Warning: May cause load as it will run "find" every time.

Tested on:
* Ubuntu
* CentOS

How to deploy:
scp stasissqldump.py icinga01:/usr/share/check_mk/checks/stasissqldump

Scratch notes for further development:

Get dbs from mysql:
mysql --defaults-extra-file=/etc/mysql/debian.cnf  --execute='show databases' --batch
Database
information_schema
mysql
owncloud
performance_schema
test
