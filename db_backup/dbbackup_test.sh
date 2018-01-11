#!/bin/bash

# Database credentials
user="root"
password="840821"
host="localhost"
db_name="test"

# Other options
backup_path="/home/yebin/pyprojects/db_backup/mysql"
date=$(date +"%d-%m-%Y")

# Set default file permissions
umask 177

# Dump database into SQL file
mysqldump --user=$user --password=$password --host=$host $db_name > $backup_path/$db_name-$date.sql

# Delete files older than 30 days
find $backup_path/* -mtime +30 -exec rm {} \;
