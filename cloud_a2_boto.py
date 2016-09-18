import boto
import time
import sys
from boto.ec2.regioninfo import RegionInfo

# Access_key is in the 'EC2 Credentials' and key name is the 'key pair' name created previously in Nectar, here are ours

#access_key_id = '26c7db8c1d88497cbea55f3fcf8778eb'
#secret_access_key = 'b8a35f5efeeb4aefb2324a3bb914820d'
key_name = 'cloud_a2'

if len(sys.argv) == 4:
    access_key_id = sys.argv[1]
    secret_access_key = sys.argv[2]
    key_name = sys.argv[3]
elif len(sys.argv) != 1:
    sys.stderr.write(''' Wrong parameter! Please input like:
        python cloud_a2_boto.py [access_key_id] [secret_access_key] [ssh_key_name]
        Example like:
            python cloud_a2_boto.py 23cd9ou80878 b8sdf9009 remote_key.pem\n''')
    sys.exit()

#Set up the region and Establish the connection
region=RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')
ec2_comm = boto.connect_ec2(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, is_secure=True, 
    region=region, port=8773, path='/services"})/Cloud', validate_certs=False)

Volumes = []
print("connection is successed!")

# Function for Launching Instances
def launch_instance(num_of_instance):
    num = num_of_instance
    for i in range(num):
        ec2_comm.run_instances('ami-000037b9', key_name=key_name, placement='melbourne-qh2',instance_type='m1.small', security_groups=['http','ssh'])

# Function for creating volumes
def create_volume():
    for k in range(4):
        ec2_comm.create_volume(60,"melbourne-qh2")
    vol = ec2_comm.get_all_volumes()
    for volid in vol:
        Volumes.append(volid.id)

#  Verify the system status and perform the functions correspondingly
def check_status():
    print("Creating instances......")
    print('Waiting for instances to start......')
    launch_instance(4)
    reservations = ec2_comm.get_all_reservations()
    for i in range(len(reservations)):
        instance = reservations[i].instances[0]
        status = reservations[i].instances[0].update()
        while status == 'pending':
            time.sleep(30)
            print("Instance%s is %s" %(i,status))
            status = reservations[i].instances[0].update()
        if status == 'running':
            instance.add_tag("Name","Instance%s"%i)
            ec2_comm.attach_volume(Volumes[i],instance.id,"/dev/vdc")
            print("Instance %s is now ready to use" %i)
        else:
            print('Instance %s status:' %i + status)     


create_volume()
check_status()
print("Congratulations! The systems are successfully established!!!")
