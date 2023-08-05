#/usr/bin/env python

"""cli for creating ec2 snapshots"""

import argparse
from argparse import RawTextHelpFormatter as rawtxt
import datetime
import pkg_resources
import boto3
from stringcolor import cs, bold

def check_instance(ec2_client, iid):
    """check if security group exists"""
    """return a dictionary or None"""
    try:
        response = ec2_client.describe_instances(InstanceIds=[iid])
        return response["Reservations"][0]["Instances"][0]
    except Exception:
        return None

def stop_instance(ec2_client, iid):
    """stop ec2 instance"""
    try:
        response = ec2_client.stop_instances(InstanceIds=[iid])
    except Exception as e:
        print(e)
        return None
    state = 0
    while state != 80:
        state = check_instance(ec2_client, iid)
        state = state["State"]["Code"]
    return response 

def snap_instance(ec2_client, vid, descrip):
    """snap image"""
    try:
        response = ec2_client.create_snapshot(
            Description=descrip,
            VolumeId=vid,
            TagSpecifications=[
                {
                    'ResourceType': 'snapshot',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': descrip
                        },
                    ]
                },
            ],
            DryRun=False
        )
    except Exception as e:
        print(e)
        return None
    return response

def get_volume_id_from_volumes(volumes):
    volume_id = False
    for volume in volumes:
        if volume["DeviceName"] == "/dev/sda1" or volume["DeviceName"] == "/dev/xvda":
            volume_id = volume["Ebs"]["VolumeId"]
    if volume_id:
        return volume_id
    return None

def generate_description(tags):
    """generate a description for the snapshot"""
    date_and_time = str(datetime.datetime.now())
    date, time = date_and_time.split(" ")
    time = time.split(".")[0].replace(":", "-")
    descrip = "aws-snap"
    for tag in tags:
        if "Key" in tag and tag["Key"] == "Name":
            descrip = tag["Value"]
    return f'{descrip}-{date}-{time}'
        
def main():
    """cli for creating ec2 snapshots"""
    version = pkg_resources.require("aws-snap")[0].version
    parser = argparse.ArgumentParser(
        description='cli for creating ec2 snapshots',
        prog='aws-snap',
        formatter_class=rawtxt
    )
    parser.add_argument('iid', nargs="+", help='Instance ID(s)')
    parser.add_argument("-r", "--region", help="specify a region.", default=None)
    parser.add_argument('-s', '--stop', action='store_true', help='Stop EC2 before snapping')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)
    args = parser.parse_args()
    instance_ids = args.iid
    region = args.region
    stop = args.stop
    try:
        if region:
            ec2 = boto3.client('ec2', region_name=region)
        else:
            ec2 = boto3.client('ec2')
    except Exception as e:
        print(e)
    for instance in instance_ids:
        info = check_instance(ec2, instance)
        if info is None:
            print(cs(f'{instance} does not exist', "yellow3"))
            print("-------")
        else:
#            print(info["InstanceType"])
#            print(info["PublicIpAddress"])
#            print(info["SecurityGroups"])
            tags = info["Tags"]
            volumes = info["BlockDeviceMappings"]
            state = info["State"]
            if stop:
                if state != 80:
                    print("stopping {}".format(instance))
                    stop_instance(ec2, instance)
                else:
                    print("instace is already stopped")
            # snapping !!
            volume_id = get_volume_id_from_volumes(volumes)
            description = generate_description(tags)
            if volume_id is None:
                print("could not determine volume ID for {}".format(instance))
            snap_it = snap_instance(ec2, volume_id, description)
            if snap_it["ResponseMetadata"]["HTTPStatusCode"] == 200:
                print(cs(f'successfully created snapshot of {instance}', "green"))
                print(cs("NOTE:", "grey"), cs("snapshot will not be immediately available", "grey2"))
                print("snapshot ID:", cs(snap_it["SnapshotId"], "SlateBlue3"))
                print("state:", cs(snap_it["State"], "LightGoldenrod3"))
                print("volume ID:", cs(snap_it["VolumeId"], "SlateBlue3"))
                print("volume size:", cs(snap_it["VolumeSize"], "SlateBlue3"))
                print("tag name:", cs(snap_it["Description"], "SlateBlue3"))
                print()
                print(bold("to poll for snapshot status try:"))
                print(cs("aws ec2 describe-snapshots --snapshot-ids {}".format(snap_it["SnapshotId"]), "pink3"))
                print("-------")
            else:
                print(cs("unknown error creating snapshot", "Yellow3"))
                print("-------")

if __name__ == "__main__":
    main()
