import os 
import subprocess
import getpass as gp
os.system("tput setaf 1")
print("\t\t\t\tWelcome")
os.system("tput setaf 7")
print("\t\t\t------------------------")
print("Enter the password")
userpaswd = gp.getpass()
paswd = "menu"
if userpaswd != paswd:
    print("Invalid Password")
    exit()
loginto=input("chose login to local/remote system : ")
print(loginto)
if loginto=="remote":
    remoteip=input("Enter the Remote system Ip: ")
os.system("clear")
def printmenu():
    print("""
              1: Date                           17: Configure AWS Linux    
              2: Calender                       18: Login to AWS 
              3: Configure Webserver            19: Create Key pair 
              4: Create file                    20: Create Security group
              5: Create Directory               21: Add Ingress(Inbound) Rule
              6: Add User                       22: Launch Instance
              7: Start Any Service U Want       23: Create Ebs Volume
              8: Stop Service U Want            24: Attach Ebs to Instance
              9: Start Python3                  25: Create S3 bucket
             10: Configure Docker               26: Upload object on bucket
             11: Start Docker Services          27: Create LVM Partition
             12: Stop Docker Services           28: Configure System as Hadoop NameNode
             13: Restart Docker Services        29: Configure System as Hadoop DataNode
             14: Login into Docker              30: Static Partition
             15: Pull Docker Image              31: Exit
             16: Launch Docker Container
            """)
def lvm(pvname,vgname,lvsize,lvname,filesystem,mount_lvm):
    os.system("df -h")
    os.system("fdisk -l")
    os.system("pvcreate {}".format(pvname))
    os.system("vgcreate {} {}".format(vgname,pvname))
    os.system("vgs")
    os.system("lvcreate -L {} -n {} {}".format(lvsize,lvname,vgname))
    os.system("lvs")
    os.system("lsblk")
    os.system("mkfs.{} /dev/{}/{}".format(filesystem,vgname,lvname))
    os.system("mount /dev/{}/{} {}".format(vgname,lvname,mount_lvm))
    os.system("df -h")
    os.system("lsblk")
    return
def lvmremote(pvname,vgname,lvsize,lvname,filesystem,mount_lvm):
    keyyesno=input("Are you doing lvm on Aws(yes/no): ")
    if keyyesno=="yes":
        keypath=input("Enter the Aws key path(format of key should be .pem): ")
        awsuser=input("Enter the User Name of Aws instance: ")
        os.system("chmod go= {}".format(keypath))
        os.system("ssh -i {} {}@{}  yum install fdisk --nobest -y".format(keypath,awsuser,remoteip))
        os.system("ssh -i {} {}@{}  yum install lvm --nobest -y".format(keypath,awsuser,remoteip))
        os.system("ssh -i {} {}@{}  df -h".format(keypath,awsuser,remoteip))
        os.system("ssh -i {} {}@{}  fdisk -l".format(keypath,awsuser,remoteip))
        os.system("ssh -i {} {}@{}  pvcreate {}".format(keypath,awsuser,remoteip,pvname))
        os.system("ssh -i {} {}@{}  vgcreate {} {}".format(keypath,awsuser,remoteip,vgname,pvname))
        os.system("ssh -i {} {}@{}  vgs".format(keypath,awsuser,remoteip))
        os.system("ssh -i {} {}@{}  lvcreate -L {} -n {} {}".format(keypath,awsuser,remoteip,lvsize,lvname,vgname))
        os.system("ssh -i {} {}@{}  lvs".format(keypath,awsuser,remoteip))
        os.system("ssh -i {} {}@{}  lsblk".format(keypath,awsuser,remoteip))
        os.system("ssh -i {} {}@{}  mkfs.{} /dev/{}/{}".format(keypath,awsuser,remoteip,filesystem,vgname,lvname))
        os.system("ssh -i {} {}@{}  mount /dev/{}/{} {}".format(keypath,awsuser,remoteip,vgname,lvname,mount_lvm))
        os.system("ssh -i {} {}@{}  df -h".format(keypath,awsuser,remoteip))
        os.system("ssh -i {} {}@{}  lsblk".format(keypath,awsuser,remoteip))
    else:
        os.system("ssh  {}  df -h".format(remoteip))
        os.system("ssh  {}  fdisk -l".format(remoteip))
        os.system("ssh  {}  pvcreate {}".format(remoteip,pvname))
        os.system("ssh  {}  vgcreate {} {}".format(remoteip,vgname,pvname))
        os.system("ssh  {}  vgs".format(remoteip))
        os.system("ssh  {}  lvcreate -L {} -n {} {}".format(remoteip,lvsize,lvname,vgname))
        os.system("ssh  {}  lvs".format(remoteip))
        os.system("ssh  {}  lsblk".format(remoteip))
        os.system("ssh  {}  mkfs.{} /dev/{}/{}".format(remoteip,filesystem,vgname,lvname))
        os.system("ssh  {}  mount /dev/{}/{} {}".format(remoteip,vgname,lvname,mount_lvm))
        os.system("ssh  {}  df -h".format(remoteip))
        os.system("ssh  {}  lsblk".format(remoteip))
    return
def checkJava():
    r = os.system("java -version")
    if r != 0:
        print("Java is not installed in your system....")
        return 0
    else:
        return 1
def checkHadoop():
    r = os.system("hadoop -v")
    if r != 0:
        print("hadoop is not installed in your system....")
        return 0
    else:
        return 1
def updateHdfsSite():
    filename="/etc/hadoop/hdfs-site.xml"
    f = open(filename,'r')
    file_lines=list(f.readlines())
    offset = len(file_lines) - 1
    if file_lines[offset-1] == "</property>\n":
        print("hdfs-site is already configured.........\n")
        print("checking core-site.xml.........")
        return
    folder = input("Create folder for namenode(enter path): ")
    string = "<property>\n<name>dfs.name.dir</name>\n<value>{}</value>\n</property>\n".format(folder)
    file_lines.insert(offset, string)
    print(file_lines)
    f.close()
    f = open(filename,'w+')
    for i in range(len(file_lines)):
        f.write(file_lines[i])
    f.close()
def updateCoreSite():
    filename="/etc/hadoop/core-site.xml"

    f = open(filename,'r')
    file_lines=list(f.readlines())
    offset = len(file_lines) - 1
    if file_lines[offset-1] == "</property>\n":
        print("core-site.xml is already configured.........")
        return
    string = "<property>\n<name>fs.default.name</name>\n<value>hdfs://0.0.0.0:9001</value>\n</property>\n"
    file_lines.insert(offset, string)
    print(file_lines)
    f.close()
    f = open(filename,'w+')
    for i in range(len(file_lines)):
        f.write(file_lines[i])
    f.close()
def checkNameNodeStatus():
    sub = subprocess.Popen("jps", shell=True, stdout=subprocess.PIPE)
    output = sub.stdout.read()
    if 'NameNode' in str(output):
        return 1
    else:
        return 0
def UpdateHdfsSite():
    filename="/etc/hadoop/hdfs-site.xml"
    f = open(filename,'r')
    file_lines=list(f.readlines())
    offset = len(file_lines) - 1
    if file_lines[offset-1] == "</property>\n":
        print("hdfs-site is already configured.........\n")
        print("checking core-site.xml.........")
        return
    folder = input("Create folder for datanode(enter path): ")
    string = "<property>\n<name>dfs.data.dir</name>\n<value>{}</value>\n</property>\n".format(folder)
    file_lines.insert(offset, string)
    print(file_lines)
    f.close()

    f = open(filename,'w+')
    for i in range(len(file_lines)):
        f.write(file_lines[i])
    f.close()
def UpdateCoreSite():
    filename="/etc/hadoop/core-site.xml"

    f = open(filename,'r')
    file_lines=list(f.readlines())
    offset = len(file_lines) - 1
    if file_lines[offset-1] == "</property>\n":
        print("core-site.xml is already configured.........")
        return
    ip = input("Enter ip of namenode: ")
    string = "<property>\n<name>fs.default.name</name>\n<value>hdfs://{}:9001</value>\n</property>\n".format(ip)
    file_lines.insert(offset, string)
    print(file_lines)
    f.close()

    f = open(filename,'w+')
    for i in range(len(file_lines)):
        f.write(file_lines[i])
    f.close()
def CheckDataNodeStatus():
    sub = subprocess.Popen("jps", shell=True, stdout=subprocess.PIPE)
    output = sub.stdout.read()
    if 'DataNode' in str(output):
        return 1
    else:
        return 0
while True:    
    if loginto=="local":
        printmenu()
        ch=int(input("Enter your Choice:  "))
        if   ch==1:
            os.system("date")
        if ch==2:
            os.system("cal")
        if ch==3:
            os.system("yum install httpd")
            os.system("systemctl start httpd")
            os.system("systemctl enable httpd")
            os.system("systemctl status httpd")
        if ch==4:
            File_name=input("Enter File Name: ")
            os.system("touch {}".format(File_name))
        if ch==5:
            Dir_name=input("Enter directory Name: ")
            os.system("mkdir {}".format(Dir_name))
        if ch==6:
            User_name=input("Enter the username please: ")
            os.system("useradd {}".format(User_name))
        if ch==7:
            Serv_start=input("Enter the Service which you want to start it: ")
            os.system("systemctl start {}".format(Serv_start))
        if ch==8:
            Serv_stop=input("Enter the Service which you want to Stop it: ")
            os.system("systemctl stop {}".format(Serv_stop))
        if ch==9:
            os.system("python3")
        if ch==10:
            os.system("wget https://raw.githubusercontent.com/abhijeetdebe/DockerRepo/main/docker.repo -P /etc/yum.repos.d/")
            os.system("yum install docker-ce --nobest -y")
            os.system("systemctl start docker")
        if ch==11:
            os.system("systemctl start docker")   
        if ch==12:
            os.system("systemctl stop docker")   
        if ch==13:
            os.system("systemctl restart docker")
        if ch==14:
            username=input("Enter Username: ")
            password=input("Enter Your Password: ")
            os.system("docker login --username {} --password {}".format(username,password))
        if ch==15:
            Doc_img=input("Enter Image name and version to be Pulled(example ubuntu:14.02): ")
            os.system("docker pull {}".format(Doc_img))
        if ch==16:
            containername=input("Enter the Container Name: ")
            doc_img=input("Enter the docker image name and version to launch Container: ")
            os.system("docker run -it --name {} {}".format(containername,doc_img))
        if ch==17:
            os.system("curl ""https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"" -o ""awscliv2.zip""")
            os.system("unzip awscliv2.zip")
            os.system("sudo ./aws/install")
        if ch==18:
            print("Please Enter the Access Key, Security Key and Region Name")
            print("Wait for Prompt to Come Up")
            os.system("aws configure")
        if ch==19:
            Keyname=input("Enter the key Name: ")
            os.system("aws ec2 create-key-pair  --key-name {}".format(Keyname))
        if ch==20:
            SGname=input("Enter the Security Name: ")
            Vpcid=input("Enter the VPC ID: ")
            desc=input("Enter description in double quotes: ")
            os.system("aws ec2 create-security-group --group-name {} --description {}  --vpc-id {}".format(SGname,desc,Vpcid))
        if ch==21:
            sgid=input("Enter the Security Group ID: ")
            protocol=input("Enter the protocol name or if you want all then enter all: ")
            cidr=input("Enter the CIDR(Example : 0.0.0.0/0): ")
            if protocol== "all" :
                os.system("aws ec2 authorize-security-group-ingress --group-id {} --protocol all --cidr {}".format(sgid,cidr))
            else:
                port=input("Enter the port number: ")
                os.system("aws ec2 authorize-security-group-ingress --group-id {} --protocol {} --port {} --cidr {}".format(sgid,protocol,port,cidr))
        if ch==22:
            amid=input("Enter the AMI ID: ")
            insttype=input("Enter th Instance type: ")
            cnt=input("Enter the number of the instance you want to launch: ")
            subid=input("Enter the Subnet ID: ")
            key=input("Enter the key name: ")
            sg=input("Enter the security group id: ")
            os.system("aws ec2 run-instances  --image-id {} --instance-type {}  --count {} --subnet-id {} --key-name {} --security-group-ids {} ".format(amid,insttype,cnt,subid,key,sg))
        if ch==23:
            voltype=input("Enter the Volume type(example: gp2): ")
            size=input("Enter the Volume Size: ")
            zone=input("Enter the Availability Zone(example: us-west-1c): ")
            os.system("aws ec2 create-volume --volume-type {} --size {} --availability-zone {}".format(voltype,size,zone))
        if ch==24:
            volid=input("Enter the Volume ID: ")
            instid=input("Enter the Instance ID: ")
            dev=input("Enter the device name(example: /dev/sdf): ")
            os.system("aws ec2 attach-volume --volume-id {} --instance-id {} --device {}".format(volid,instid,dev))
        if ch==25:
            buckname=input("Enter the Bucket Name: ")
            region=input("Enter the Region ID(example: us-west-1): ")
            os.system("aws s3api create-bucket --bucket {} --region {} --create-bucket-configuration LocationConstraint={} ".format(buckname,region,region))
        if ch==26:
            source=input("Enter the Object local path: ")
            dest=input("Enter the bucket path(example s3://bucketname): ")
            os.system("aws s3 cp {} {}".format(source,dest))
        if ch==27:
            pvname=input("Enter the Physical Volume Device Name(example: /dev/sdb): ")
            vgname=input("Enter the Volume Group Name: ")
            lvsize=input("Enter the Size of LV(example: 5G): ")
            lvname=input("Enter the Logical Volume Name: ")
            filesystem=input("Enter the File system(example: xfs,ext4): ")
            mount_lvm=input("Enter the path of Existing directory to mount to LVM: ")
            lvm(pvname,vgname,lvsize,lvname,filesystem,mount_lvm)
        if ch==28:
            if checkJava:
                if checkHadoop: 
                    updateHdfsSite()
                    updateCoreSite()
                    if not checkNameNodeStatus():
                        print("Starting NameNode..............")
                        os.system("hadoop namenode -format -force")
                        os.system("hadoop-daemon.sh start namenode")
                    else:
                        print("Service running already.....")
        if ch==29:
            if checkJava :
                if checkHadoop :
                    UpdateHdfsSite()
                    UpdateCoreSite()
                    if not CheckDataNodeStatus():
                        print("Starting DataNode..............")
                        os.system("hadoop-daemon.sh start datanode")
                    else:
                        print("Service running already.....")
        if ch==30:
            c=int(input("Do you want to create(Press 1) or remove(Press 2) partition"))
            os.system("fdisk -l")
            if int(c)==1 :
                diskname=input("Enter the Device Name")
                os.system("fdisk -s /dev/{}".format(diskname))
                partsize=input("enter the partition size")
                f_name=input("Give the file name where you want to mount the harddisk")
                os.system("fdisk /dev/{}".format(diskname))
                os.system("echo n | fdisk /dev/{}".format(diskname))
                os.system("echo p | fdisk /dev/{}".format(diskname))
                os.system("echo \n | fdisk /dev/{}".format(diskname))
                os.system("echo +{}G | fdisk /dev/{}".format(partsize,diskname))
                os.system("echo w | fdisk /dev/{}".format(diskname))
                os.system("echo q | fdisk /dev/{}".format(diskname))
                os.system("mkfs.ext4 /dev/{}".format(diskname))
                os.system("mkdir /{}".format(f_name))
                os.system("mount /dev/{}  /{}".format(diskname,f_name))
            elif int(c)==2 :
                os.system("fdisk /dev/{}".format(diskname))
                os.system("echo d | fdisk /dev/{}".format(diskname))
                os.system("echo w | fdisk /dev/{}".format(diskname))
                os.system("echo q | fdisk /dev/{}".format(diskname))
        if ch==31:
            exit()
        else:
            print("Enter the Rigth Choice")
        input("Enter to continue")
        os.system("clear")
    elif loginto=="remote":
        printmenu()
        ch=int(input("Enter your Choice:  "))
        if   ch==1:
            os.system("ssh {} date".format(remoteip))
        if ch==2:
            os.system("ssh {} cal".format(remoteip))
        if ch==3:
            os.system("ssh {} yum install httpd".format(remoteip))
            os.system("ssh {} systemctl start httpd".format(remoteip))
            os.system("ssh {} systemctl enable httpd".format(remoteip))
            os.system("ssh {} systemctl status httpd".format(remoteip))
        if ch==4:
            File_name=input("Enter File Name: ")
            os.system("ssh {} touch {}".format(remoteip,File_name))
        if ch==5:
            Dir_name=input("Enter directory Name: ")
            os.system("ssh {} mkdir {}".format(remoteip,Dir_name))
        if ch==6:
            User_name=input("Enter the username please: ")
            os.system("ssh {} useradd {}".format(remoteip,User_name))
        if ch==7:
            Serv_start=input("Enter the Service which you want to start it: ")
            os.system("ssh {} systemctl start {}".format(remoteip,Serv_start))
        if ch==8:
            Serv_stop=input("Enter the Service which you want to Stop it: ")
            os.system("ssh {} systemctl stop {}".format(remoteip,Serv_stop))
        elif ch==9:
            os.system("python3")
        if ch==10:
            os.system("sudo cd /etc/yum.repos.d/ && wget https://raw.githubusercontent.com/abhijeetdebe/DockerRepo/main/docker.repo")
            os.system("ssh {} yum install docker --nobest -y".format(remoteip))
            os.system("ssh {} systemctl start docker".format(remoteip))
        if ch==11:
            os.system("ssh {} systemctl start docker".format(remoteip))   
        if ch==12:
            os.system("ssh {} systemctl stop docker".format(remoteip))   
        if ch==13:
            os.system("ssh {} systemctl restart docker".format(remoteip))
        if ch==14:
            username=input("Enter Username: ")
            useremail=input("Enter Email Address: ")
            os.system("ssh {} docker login --username={} --email={}".format(remoteip,username,useremail))
        if ch==15:
            Doc_img=input("Enter Image name and version to be Pulled(example ubuntu:14.02): ")
            os.system("ssh {} docker pull {}".format(remoteip,Doc_img))
        if ch==16:
            containername=input("Enter the Container Name: ")
            doc_img=input("Enter the docker image name and version to launch Container: ")
            os.system("ssh {} docker run -it --name {} {}".format(remoteip,containername,doc_img))
        if ch==17:
            os.system("ssh {} curl ""https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"" -o ""awscliv2.zip""".format(remoteip))
            os.system("ssh {} unzip awscliv2.zip".format(remoteip))
            os.system("ssh {} sudo ./aws/install".format(remoteip))
        if ch==18:
            print("Please Enter the Access Key, Security Key and Region Name")
            print("Wait for Prompt to Come Up")
            os.system("ssh {} aws configure".format(remoteip))
        if ch==19:
            Keyname=input("Enter the key Name: ")
            os.system("ssh {} aws ec2 create-key-pair  --key-name {}".format(remoteip,Keyname))
        if ch==20:
            SGname=input("Enter the Security Name: ")
            Vpcid=input("Enter the VPC ID: ")
            desc=input("Enter description in double quotes: ")
            os.system("ssh {} aws ec2 create-security-group --group-name {} --description {}  --vpc-id {}".format(remoteip,SGname,desc,Vpcid))
        if ch==21:
            sgid=input("Enter the Security Group ID: ")
            protocol=input("Enter the protocol name or if you want all then enter all: ")
            cidr=input("Enter the CIDR(Example : 0.0.0.0/0): ")
            if protocol== "all" :
                os.system("ssh {} aws ec2 authorize-security-group-ingress --group-id {} --protocol all --cidr {}".format(remoteip,sgid,cidr))
            else:
                port=input("Enter the port number: ")
                os.system("ssh {} aws ec2 authorize-security-group-ingress --group-id {} --protocol {} --port {} --cidr {}".format(remoteip,sgid,protocol,port,cidr))
        if ch==22:
            amid=input("Enter the AMI ID: ")
            insttype=input("Enter th Instance type: ")
            cnt=input("Enter the number of the instance you want to launch: ")
            subid=input("Enter the Subnet ID: ")
            key=input("Enter the key name: ")
            sg=input("Enter the security group id: ")
            os.system("ssh {} aws ec2 run-instances  --image-id {} --instance-type {}  --count {} --subnet-id {} --key-name {} --security-group-ids {} ".format(remoteip,amid,insttype,cnt,subid,key,sg))
        if ch==23:
            voltype=input("Enter the Volume type(example: gp2): ")
            size=input("Enter the Volume Size: ")
            zone=input("Enter the Availability Zone(example: us-west-1c): ")
            os.system("ssh {} aws ec2 create-volume --volume-type {} --size {} --availability-zone {}".format(remoteip,voltype,size,zone))
        if ch==24:
            volid=input("Enter the Volume ID: ")
            instid=input("Enter the Instance ID: ")
            dev=input("Enter the device name(example: /dev/sdf): ")
            os.system("ssh {} aws ec2 attach-volume --volume-id {} --instance-id {} --device {}".format(remoteip,volid,instid,dev))
        if ch==25:
            buckname=input("Enter the Bucket Name: ")
            region=input("Enter the Region ID(example: us-west-1): ")
            os.system("ssh {} aws s3api create-bucket --bucket {} --region {} --create-bucket-configuration LocationConstraint={}".format(remoteip,buckname,region,region))
        if ch==26:
            source=input("Enter the Object local path: ")
            dest=input("Enter the bucket path(example s3://bucketname): ")
            os.system("ssh {} aws s3 cp {} {}".format(remoteip,source,dest))
        if ch==27:
            pvname=input("Enter the Physical Volume Device Name(example: /dev/sdb): ")
            vgname=input("Enter the Volume Group Name: ")
            lvsize=input("Enter the Size of LV(example: 5G): ")
            lvname=input("Enter the Logical Volume Name: ")
            filesystem=input("Enter the File system(example: xfs,ext4): ")
            mount_lvm=input("Enter the path of Existing directory to mount to LVM: ")
            lvmremote(pvname,vgname,lvsize,lvname,filesystem,mount_lvm)
        if ch==28:
            print("Working on Hadoop NameNode Remote")
        if ch==29:
            print("Working on Hadoop Datanode Remote")
        if ch==30:
            c=int(input("Do you want to create(Press 1) or remove(Press 2) partition"))
            os.system("fdisk -l")
            if int(c)==1 :
                diskname=input("Enter the Device Name")
                os.system("ssh {} fdisk -s /dev/{}".format(remoteip,diskname))
                partsize=input("enter the partition size")
                f_name=input("Give the file name where you want to mount the harddisk")
                os.system("ssh {} fdisk /dev/{}".format(remoteip,diskname))
                os.system("ssh {} echo n | fdisk /dev/{}".format(remoteip,diskname))
                os.system("ssh {} echo p | fdisk /dev/{}".format(remoteip,diskname))
                os.system("ssh {} echo \n | fdisk /dev/{}".format(remoteip,diskname))
                os.system("ssh {} echo +{}G | fdisk /dev/{}".format(remoteip,partsize,diskname))
                os.system("ssh {} echo w | fdisk /dev/{}".format(remoteip,diskname))
                os.system("ssh {} echo q | fdisk /dev/{}".format(remoteip,diskname))
                os.system("ssh {} mkfs.ext4 /dev/{}".format(remoteip,diskname))
                os.system("ssh {} mkdir /{}".format(remoteip,f_name))
                os.system("ssh {} mount /dev/{}  /{}".format(remoteip,diskname,f_name))
            elif int(c)==2 :
                os.system("ssh {} fdisk /dev/{}".format(remoteip,diskname))
                os.system("ssh {} echo d | fdisk /dev/{}".format(remoteip,diskname))
                os.system("ssh {} echo w | fdisk /dev/{}".format(remoteip,diskname))
                os.system("ssh {} echo q | fdisk /dev/{}".format(remoteip,diskname))
        if ch==31:
            exit()
        else:
            print("Option not supported enter local or remote")
        input("Enter to continue")
        os.system("clear")
    else:
        print("Enter the Right Location")
