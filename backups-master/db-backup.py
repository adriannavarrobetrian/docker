#!/usr/bin/python
import logging
import paramiko
import os
from datetime import datetime, timedelta
import argparse
import sys
import boto
import re
import time
from boto.s3.key import Key

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  %(levelname)-6s %(message)s',
                    datefmt='%m-%d-%-y %H:%M:%S',
                    filename='/opt/backups/logs/db-backup.log',
                    filemode='a')

logging.getLogger("paramiko").setLevel(logging.WARNING)
stdout = logging.StreamHandler(sys.stdout)
format = logging.Formatter('%(asctime)s  %(levelname)-6s %(message)s')
stdout.setFormatter(format)

logger = logging.getLogger()
logger.addHandler(stdout)

full_backup = ['admin', 'api', 'cms', 'engine', 'file', 'gbase']
now = datetime.today()
yest = datetime.today() - timedelta(7)
dateString = '%s-%s-%s' % (now.day, now.month, now.year)
date = '%s%02d%02d' % (yest.year, yest.month, yest.day)

def runMYSQLdump(server, user, databases):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=server, username=user)
	transport = ssh.get_transport()
	transport.set_keepalive(30)
	session = transport.open_channel("session")
	session.get_pty()
	file = ('DATABASE_BACKUP-%s-%s.sql.bz2' % ("-".join(databases), dateString))
	logger.info('Starting mysqldump for the following databases: %s ' % (" ".join(databases)))
	command = ('sudo mysqldump --single-transaction --skip-lock-tables --quick --databases %s | bzip2 -9 > /store/mysql/backup/%s' % (" ".join(databases), file))
        session.exec_command(command)
        while True:
	    if session.recv_exit_status() == 0:
		break
#	    lines = stdout.readlines()
#	    for line in lines:
#                print line
	    time.sleep(30)
	ssh.close()
	logger.info('Created %s for the following databases: %s ' % (file, " ".join(databases)))
    except Exception as e:
        logger.error('Error received connecting to %s: %s' % (server, e))

def retrieveBackup(server, user, databases):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=server, username=user)
        sftp = ssh.open_sftp()
	file = ('DATABASE_BACKUP-%s-%s.sql.bz2' % ("-".join(databases), dateString))
        logger.info('Retrieving %s backup from %s ' % (file, server))
        sftp.get('/store/mysql/backup/%s' % (file), '/tmp/%s' % (file))
	sftp.remove('/store/mysql/backup/%s' % (file))
        sftp.close()
	logger.info('Retrieved %s mysql backup from %s ' % (file, server))
    except Exception as e:
        logger.error('Error received connecting to %s: %s' % (server, e))
    return file

def uploadBackupToS3(environment, backup_file):
    upload = ('/tmp/%s' % (backup_file))
    try:
        logger.info('Attempting to upload %s to S3' % (backup_file))
        s3_connection = boto.connect_s3()
        bucket = s3_connection.get_bucket('greenlightpower', validate=True)
        k = Key(bucket)
	k.key = ('mysql_backups/%s/%s' % (environment, backup_file))
        k.set_contents_from_filename(upload)
	logger.info('Upload of %s complete' % (backup_file))
	os.remove(upload)
    except Exception as e:
	logger.error('Error uploading to S3: %s' % (e))
     
def cleanUpOldBackups(environment):
    try:
        logger.info('Removing old backups')
        s3_connection = boto.connect_s3()
        bucket = s3_connection.get_bucket('greenlightpower', validate=True)
        for key in bucket.list(prefix='mysql_backups/%s/' % (environment), delimiter='/'):
	    m = re.search('sql.bz2', key.name)
	    if m:
	        create_time = datetime.strptime(
                key.last_modified,
	        '%Y-%m-%dT%H:%M:%S.000Z'
                )
	        if create_time < datetime.utcnow() - timedelta(days=7):
		    logger.info('Deleting old backup: %s' % (key.name))
		    k = Key(bucket = bucket, name=key.name)
		    k.delete()
    except Exception as e:
        logger.error('Error cleaning up: %s' % (e))

def main():
 
    environments = ["prod", "test", "sandbox"]

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server",
                       help="REQUIRED: Specify the server to connect to",
                       dest="server")
    parser.add_argument("-d", "--databases",
                       help="Specify the databases to backup. If not specified a full run will be completed",
                       dest="databases",
 		       default=full_backup,
		       nargs="+")
    parser.add_argument("-u", "--user",
                       help="REQUIRED: Specify the OS to connect to - remote user must have sudo to complete",
                       dest="user")
    parser.add_argument("-e", "--environment",
                       help="REQUIRED: Specify which environment this backup is of",
                       dest="environment",
		       choices=environments)

    opts = parser.parse_args()

    if opts.server is None or opts.user is None or opts.environment is None:
        parser.print_help()
        sys.exit(0)
 
    runMYSQLdump(opts.server, opts.user, opts.databases)
    backup_file = retrieveBackup(opts.server, opts.user, opts.databases)
    uploadBackupToS3(opts.environment, backup_file)
    cleanUpOldBackups(opts.environment)

if __name__ == '__main__':
    main()
