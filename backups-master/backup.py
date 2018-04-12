#!/usr/bin/python
import boto.ec2
import pprint
import logging
import time
import argparse
import sys
from datetime import datetime, timedelta

# Set logging 

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s   %(levelname)-6s %(message)s',
                    datefmt='%m-%d-%-y %H:%M:%S',
                    filename='/opt/backups/logs/backup.log',
                    filemode='a') 

stdout = logging.StreamHandler(sys.stdout)
format = logging.Formatter('%(asctime)s   %(levelname)-6s %(message)s')
stdout.setFormatter(format)

logger = logging.getLogger()
logger.addHandler(stdout)

now=datetime.today()
dateString='%s-%s-%s' % (now.day, now.month, now.year)

filters = {'tag-key': 'backup', 'tag-value': 'True'} 

ec2 = boto.ec2.connect_to_region('eu-west-1')

class Backup:

    def __init__(self, volume):
        self.volume = volume

    def snapSystem(self):
	try:
	    snap = ec2.create_snapshot(self.volume,'Snapshot of %s - %s - %s' % (self.instanceName(), self.volumeDevice(), dateString))
	    snap.add_tags({'backup': 'True'})
        except:
            logger.error('Failed to start Snapshotting for %s' % (self.volume))
        return snap.id

    def volID(self):
        return self.volume

    def instanceID(self):
        try:
            instance = ec2.get_all_volumes(volume_ids=self.volume)
            for i in instance:
                instanceID = i.attach_data.instance_id
            return instanceID
        except:
 	    logger.error('Failed to retrieve instance ID for %s, assuming volume has been deleted' % (self.volume))

    def instanceName(self):
	try:
            instance = ec2.get_all_instances(instance_ids=self.instanceID())
            for res in instance:
                for i in res.instances:
                    if 'Name' in i.tags:
		        name = i.tags['Name']
	except:
	    logger.error('Failed to retrieve instance Name for %s' % (self.instanceID()))
	return name

    def volumeDevice(self):
	try:
            instance = ec2.get_all_volumes(volume_ids=self.volume)
            for i in instance:
                device = i.attach_data.device
		return device
	except:
	    logger.error('Failed to retrieve Device Name for %s' % (self.volume))

class Snap:

    def __init__(self, snap):
        self.snap = snap
	self.snapshot = ec2.get_all_snapshots(snapshot_ids=self.snap)[0]

    def snapProgress(self):
        return self.snapshot.progress

    def snapDate(self):
	return self.snapshot.start_time

    def snapVolume(self):
	return self.snapshot.volume_id

    def deleteSnap(self):
        try:
	    ec2.delete_snapshot(self.snap)
	except:
	    logger.error('Could not delete snapshot: %s for volume: %s' % (self.snap, self.snapVolume()))		    

    def snapInstanceName(self):
        vol = Backup(self.snapVolume())
	return vol.instanceName()

    def snapDeviceName(self):
        vol = Backup(self.snapVolume())
        return vol.volumeDevice()

def snapshotSystems(volumes,instance,skip):
    progress_list = []
    if instance[0] == "all":
        for vol in volumes:
            back = Backup(vol.id)
	    if back.instanceName() not in skip:
                logger.info('Starting backup for %s - %s - %s' % (back.volID(), back.volumeDevice(), back.instanceName()))
	        progress_list.append(back.snapSystem())
	    else:
	        logger.info('SKIPPING backup of %s - %s - %s' % (back.volID(), back.volumeDevice(), back.instanceName()))
    else:
        for vol in volumes:
	    back = Backup(vol.id)
            if back.instanceName() in instance and back.instanceName() not in skip:
	        logger.info('Starting backup for %s - %s - %s' % (back.volID(), back.volumeDevice(), back.instanceName()))
		progress_list.append(back.snapSystem())
	    elif back.instanceName() in skip:
		logger.info('SKIPPING backup of %s - %s - %s' % (back.volID(), back.volumeDevice(), back.instanceName()))
    
    return progress_list

def snapProgress(snap_list):
    while snap_list:
        for snapID in snap_list:
	    prog = Snap(snapID)
            if prog.snapProgress() == '100%':
                logger.info('Snapshot %s has completed - %s - %s - %s' % (snapID, prog.snapVolume(), prog.snapInstanceName(), prog.snapDeviceName()))
	        snap_list.remove(snapID)
            else:
	        logger.info('Snapshot %s %s complete - %s - %s - %s' % (snapID, prog.snapProgress(), prog.snapVolume(), prog.snapInstanceName(), prog.snapDeviceName()))
        time.sleep( 20 )

def snapCleanup():
    delete_time = datetime.utcnow() - timedelta(days=7)
    snap_list = ec2.get_all_snapshots(filters = filters)

    for i in snap_list:
	snap = Snap(i.id)
	start_time = datetime.strptime(
	    snap.snapDate(),
	    '%Y-%m-%dT%H:%M:%S.000Z'
	)
        if start_time < delete_time:
            snap.deleteSnap()
            logger.info('Deleted snapshot: %s for Volume: %s - %s - %s' % (i.id, snap.snapVolume(), snap.snapInstanceName(), snap.snapDeviceName()))

def main():

    parser = argparse.ArgumentParser() 
    parser.add_argument("-i", "--instance", 
                       help="REQUIRED: Specify space separated instances or 'all' to backup all instances",
                       dest="instance",
		       nargs="+")
    parser.add_argument("-c", "--cleanup", 
                       help="Add this to cleanup old backups", 
                       action="store_true",
                       dest="cleanup")
    parser.add_argument("-s", "--skip",
                       help="Specify space separated instances to leave out of the run",
                       dest="skip",
		       default=['none'],
                       nargs="+")

    opts = parser.parse_args()

    if opts.instance is None:
        parser.print_help()
        sys.exit(0)

    volumes = ec2.get_all_volumes(filters = filters) 

    snap_list = snapshotSystems(volumes,opts.instance,opts.skip)
    snapProgress(snap_list)
 
    if opts.cleanup:
        snapCleanup()
    else:
	logger.info('Cleanup option not selected')

if __name__ == '__main__':
    main()
