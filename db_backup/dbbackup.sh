#!/bin/bash

# Database credentials
user="root"
password="840821"
host="localhost"
db_name_test="test"
db_name_documents="documents"
db_name_log="log"
db_name_myblog="myblog"

# Other options
backup_path="/home/yebin/pyprojects/db_backup/mysql"
date=$(date +"%d-%m-%Y")

# Set default file permissions
umask 177

# Dump database into SQL file
mysqldump --user=$user --password=$password --host=$host $db_name_test > $backup_path/$db_name_test-$date.sql
mysqldump --user=$user --password=$password --host=$host $db_name_documents > $backup_path/$db_name_documents-$date.sql
mysqldump --user=$user --password=$password --host=$host $db_name_log > $backup_path/$db_name_log-$date.sql
mysqldump --user=$user --password=$password --host=$host $db_name_myblog > $backup_path/$db_name_myblog-$date.sql

# Delete files older than 30 days
find $backup_path/* -mtime +30 -exec rm {} \;
