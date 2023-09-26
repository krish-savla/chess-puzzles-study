import os
from paramiko import SSHClient
from scp import SCPClient
import sys

# Define progress callback that prints the current percentage completed for the file
def progress(filename, size, sent):
    sys.stdout.write("%s's progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('homework.cs.tufts.edu', username='mrussell')
scp = SCPClient(ssh.get_transport(), progress=progress)


files = [f for f in os.listdir('.') if f.endswith('.json')]

if not files:
    print("no new .json files to write. quitting")
    exit()

if len(files) > 7:
    print("there are more than 7 json files to upload. no big deal, but please reach out to mrussell and he will take care of things manually. thanks!")
    exit()

# pick the first uuid at random
uuid = files[0].split('_')[0]

for f in files:
    f_rest = '_'.join(f.split('_')[1:])
    scp.put(f, remote_path=f'/r/emotiondata/chesspuzzles/data/{uuid}_{f_rest}')
    os.rename(f, f'uploaded/{uuid}_{f_rest}')

scp.close()
