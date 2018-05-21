import random
import logging
import string
import os
import inspect
from shutit_module import ShutItModule

class shutit_openshift_cluster_ansible(ShutItModule):


	def build(self, shutit):
		shutit.run_script('''#!/bin/bash
MODULE_NAME=shutit_openshift_cluster_ansible
rm -rf $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/vagrant_run/*
if [[ $(command -v VBoxManage) != '' ]]
then
	while true
	do
		VBoxManage list runningvms | grep ${MODULE_NAME} | awk '{print $1}' | xargs -IXXX VBoxManage controlvm 'XXX' poweroff && VBoxManage list vms | grep shutit_openshift_cluster_ansible | awk '{print $1}'  | xargs -IXXX VBoxManage unregistervm 'XXX' --delete
		# The xargs removes whitespace
		if [[ $(VBoxManage list vms | grep ${MODULE_NAME} | wc -l | xargs) -eq '0' ]]
		then
			break
		else
			ps -ef | grep virtualbox | grep ${MODULE_NAME} | awk '{print $2}' | xargs kill
			sleep 10
		fi
	done
fi
#if [[ $(command -v virsh) ]] && [[ $(kvm-ok 2>&1 | command grep 'can be used') != '' ]]
#then
#	virsh list | grep ${MODULE_NAME} | awk '{print $1}' | xargs -n1 virsh destroy
#fi''')
		vagrant_image = shutit.cfg[self.module_id]['vagrant_image']
		vagrant_provider = shutit.cfg[self.module_id]['vagrant_provider']
		gui = shutit.cfg[self.module_id]['gui']
		memory = shutit.cfg[self.module_id]['memory']
		shutit.build['vagrant_run_dir'] = os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0))) + '/vagrant_run'
		shutit.build['module_name'] = 'shutit_openshift_cluster_ansible_' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
		shutit.build['this_vagrant_run_dir'] = shutit.build['vagrant_run_dir'] + '/' + shutit.build['module_name']
		shutit.send(' command rm -rf ' + shutit.build['this_vagrant_run_dir'] + ' && command mkdir -p ' + shutit.build['this_vagrant_run_dir'] + ' && command cd ' + shutit.build['this_vagrant_run_dir'])
		shutit.send('command rm -rf ' + shutit.build['this_vagrant_run_dir'] + ' && command mkdir -p ' + shutit.build['this_vagrant_run_dir'] + ' && command cd ' + shutit.build['this_vagrant_run_dir'])
		if shutit.send_and_get_output('vagrant plugin list | grep landrush') == '':
			shutit.send('vagrant plugin install landrush')
		shutit.send('vagrant init ' + vagrant_image)
		shutit.send_file(shutit.build['this_vagrant_run_dir'] + '/Vagrantfile','''Vagrant.configure("2") do |config|
  config.landrush.enabled = true
  config.vm.provider "virtualbox" do |vb|
    vb.gui = ''' + gui + '''
  end

  config.vm.define "master1" do |master1|
    master1.vm.box = ''' + '"' + vagrant_image + '"' + '''
    master1.vm.hostname = "master1.vagrant.test"
    master1.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--memory", "2048"]
      v.name = "ansmaster1"
    end
  end
  config.vm.define "master2" do |master2|
    master2.vm.box = ''' + '"' + vagrant_image + '"' + '''
    master2.vm.hostname = "master2.vagrant.test"
    master2.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--memory", "2048"]
      v.name = "ansmaster2"
    end
  end
  config.vm.define "etcd1" do |etcd1|
    etcd1.vm.box = ''' + '"' + vagrant_image + '"' + '''
    etcd1.vm.hostname = "etcd1.vagrant.test"
    etcd1.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--memory", "1024"]
      v.name = "ansetcd1"
    end
  end
  config.vm.define "etcd2" do |etcd2|
    etcd2.vm.box = ''' + '"' + vagrant_image + '"' + '''
    etcd2.vm.hostname = "etcd2.vagrant.test"
    etcd2.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--memory", "1024"]
      v.name = "ansetcd2"
    end
  end
  config.vm.define "etcd3" do |etcd3|
    etcd3.vm.box = ''' + '"' + vagrant_image + '"' + '''
    etcd3.vm.hostname = "etcd3.vagrant.test"
    etcd3.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--memory", "1024"]
      v.name = "ansetcd3"
    end
  end
  config.vm.define "node1" do |node1|
    node1.vm.box = ''' + '"' + vagrant_image + '"' + '''
    node1.vm.hostname = "node1.vagrant.test"
    node1.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--memory", "2048"]
      v.name = "ansnode1"
    end
  end
  config.vm.define "node2" do |node2|
    node2.vm.box = ''' + '"' + vagrant_image + '"' + '''
    node2.vm.hostname = "node2.vagrant.test"
    node2.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--memory", "2048"]
      v.name = "ansnode2"
    end
  end
end''')
		################################################################################
		# Extract password from 'secret' file (which git ignores).
		# TODO: check perms are only readable by user
		try:
			pw = file('secret').read().strip()
		except IOError:
			pw = ''
		if pw == '':
			shutit.log('''================================================================================\nWARNING! IF THIS DOES NOT WORK YOU MAY NEED TO SET UP A 'secret' FILE IN THIS FOLDER!\n================================================================================''',level=logging.CRITICAL)
			pw='nopass'
		################################################################################

		################################################################################
		def vagrant_up(shutit,pw):
			try:
				shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'] + " master1",{'assword for':pw,'assword:':pw},timeout=99999)
			except NameError:
				shutit.multisend('vagrant up master1',{'assword for':pw,'assword:':pw},timeout=99999)
			if shutit.send_and_get_output("""vagrant status 2> /dev/null | grep -w ^master1 | awk '{print $2}'""") != 'running':
				shutit.pause_point("machine: master1 appears not to have come up cleanly")
			try:
				shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'] + " master2",{'assword for':pw,'assword:':pw},timeout=99999)
			except NameError:
				shutit.multisend('vagrant up master2',{'assword for':pw,'assword:':pw},timeout=99999)
			if shutit.send_and_get_output("""vagrant status 2> /dev/null | grep -w ^master2 | awk '{print $2}'""") != 'running':
				shutit.pause_point("machine: master2 appears not to have come up cleanly")
			try:
				shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'] + " etcd1",{'assword for':pw,'assword:':pw},timeout=99999)
			except NameError:
				shutit.multisend('vagrant up etcd1',{'assword for':pw,'assword:':pw},timeout=99999)
			if shutit.send_and_get_output("""vagrant status 2> /dev/null | grep -w ^etcd1 | awk '{print $2}'""") != 'running':
				shutit.pause_point("machine: etcd1 appears not to have come up cleanly")
			try:
				shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'] + " etcd2",{'assword for':pw,'assword:':pw},timeout=99999)
			except NameError:
				shutit.multisend('vagrant up etcd2',{'assword for':pw,'assword:':pw},timeout=99999)
			if shutit.send_and_get_output("""vagrant status 2> /dev/null | grep -w ^etcd2 | awk '{print $2}'""") != 'running':
				shutit.pause_point("machine: etcd2 appears not to have come up cleanly")
			try:
				shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'] + " etcd3",{'assword for':pw,'assword:':pw},timeout=99999)
			except NameError:
				shutit.multisend('vagrant up etcd3',{'assword for':pw,'assword:':pw},timeout=99999)
			if shutit.send_and_get_output("""vagrant status 2> /dev/null | grep -w ^etcd3 | awk '{print $2}'""") != 'running':
				shutit.pause_point("machine: etcd3 appears not to have come up cleanly")
			try:
				shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'] + " node1",{'assword for':pw,'assword:':pw},timeout=99999)
			except NameError:
				shutit.multisend('vagrant up node1',{'assword for':pw,'assword:':pw},timeout=99999)
			if shutit.send_and_get_output("""vagrant status 2> /dev/null | grep -w ^node1 | awk '{print $2}'""") != 'running':
				shutit.pause_point("machine: node1 appears not to have come up cleanly")
			try:
				shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'] + " node2",{'assword for':pw,'assword:':pw},timeout=99999)
			except NameError:
				shutit.multisend('vagrant up node2',{'assword for':pw,'assword:':pw},timeout=99999)
			if shutit.send_and_get_output("""vagrant status 2> /dev/null | grep -w ^node2 | awk '{print $2}'""") != 'running':
				shutit.pause_point("machine: node2 appears not to have come up cleanly")
		vagrant_up(shutit,pw)
		################################################################################


		################################################################################
		# machines is a dict of dicts containing information about each machine for you to use.
		machines = {}
		machines.update({'master1':{'fqdn':'master1.vagrant.test'}})
		ip = shutit.send_and_get_output('''vagrant landrush ls 2> /dev/null | grep -w ^''' + machines['master1']['fqdn'] + ''' | awk '{print $2}' ''')
		machines.get('master1').update({'ip':ip})
		machines.update({'master2':{'fqdn':'master2.vagrant.test'}})
		ip = shutit.send_and_get_output('''vagrant landrush ls 2> /dev/null | grep -w ^''' + machines['master2']['fqdn'] + ''' | awk '{print $2}' ''')
		machines.get('master2').update({'ip':ip})
		machines.update({'etcd1':{'fqdn':'etcd1.vagrant.test'}})
		ip = shutit.send_and_get_output('''vagrant landrush ls 2> /dev/null | grep -w ^''' + machines['etcd1']['fqdn'] + ''' | awk '{print $2}' ''')
		machines.get('etcd1').update({'ip':ip})
		machines.update({'etcd2':{'fqdn':'etcd2.vagrant.test'}})
		ip = shutit.send_and_get_output('''vagrant landrush ls 2> /dev/null | grep -w ^''' + machines['etcd2']['fqdn'] + ''' | awk '{print $2}' ''')
		machines.get('etcd2').update({'ip':ip})
		machines.update({'etcd3':{'fqdn':'etcd3.vagrant.test'}})
		ip = shutit.send_and_get_output('''vagrant landrush ls 2> /dev/null | grep -w ^''' + machines['etcd3']['fqdn'] + ''' | awk '{print $2}' ''')
		machines.get('etcd3').update({'ip':ip})
		machines.update({'node1':{'fqdn':'node1.vagrant.test'}})
		ip = shutit.send_and_get_output('''vagrant landrush ls 2> /dev/null | grep -w ^''' + machines['node1']['fqdn'] + ''' | awk '{print $2}' ''')
		machines.get('node1').update({'ip':ip})
		machines.update({'node2':{'fqdn':'node2.vagrant.test'}})
		ip = shutit.send_and_get_output('''vagrant landrush ls 2> /dev/null | grep -w ^''' + machines['node2']['fqdn'] + ''' | awk '{print $2}' ''')
		machines.get('node2').update({'ip':ip})
		################################################################################

		################################################################################
		root_pass = 'origin'
		for machine in sorted(machines.keys()):
			shutit.login(command='vagrant ssh ' + machine)
			shutit.login(command='sudo su - ')
			shutit.install('net-tools')
			shutit.send('''sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config''')
			shutit.send('''sed -i 's/.*PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config''')
			shutit.send('systemctl restart sshd')
			shutit.send('echo root:' + root_pass + ' | /usr/sbin/chpasswd')
			shutit.send('systemctl restart sshd')
			# This is to prevent ansible from getting the 'wrong' ip address for the host from eth0.
			# See: http://stackoverflow.com/questions/29495704/how-do-you-change-ansible-default-ipv4
			shutit.send('route add -net 8.8.8.8 netmask 255.255.255.255 eth1')
			ip_addr = shutit.send_and_get_output("""ip -4 route get 8.8.8.8 | head -1 | awk '{print $NF}'""")
			shutit.send(r"""sed -i 's/127.0.0.1\t\(.*\).vagrant.test.*/""" + ip_addr + r"""\t\1.vagrant.test\t\1/' /etc/hosts""")
			shutit.logout()
			shutit.logout()
		for machine in sorted(machines.keys()):
			shutit.login(command='vagrant ssh ' + machine)
			shutit.login(command='sudo su - ')
			shutit.multisend('ssh-keygen',{'Enter file in which':'','Enter passphrase':'','Enter same passphrase':''})
			for to_machine in sorted(machines.keys()):
				shutit.multisend('ssh-copy-id root@' + to_machine + '.vagrant.test',{'ontinue connecting':'yes','assword':root_pass})
				shutit.multisend('ssh-copy-id root@' + to_machine,{'ontinue connecting':'yes','assword':root_pass})
			shutit.logout()
			shutit.logout()
		################################################################################

		################################################################################
		#for machine in sorted(machines.keys()):
		#	shutit.login(command='vagrant ssh ' + machine)
		#	shutit.login(command='sudo su - ')
		#	shutit.send('origin-excluder disable')
		#	shutit.logout()
		#	shutit.logout()
		################################################################################

		################################################################################
		shutit.login(command='vagrant ssh master1',check_sudo=False)
		shutit.login(command='sudo su -',password='vagrant',check_sudo=False)
		shutit.install('epel-release')
		shutit.install('git')
		shutit.install('ansible')
		shutit.install('pyOpenSSL')
		shutit.install('python-cryptography')
		shutit.install('python-lxml')
		shutit.send('git clone -b release-3.6 https://github.com/openshift/openshift-ansible')
		shutit.send_file('/etc/ansible/hosts','''# Create an OSEv3 group that contains the master, nodes, etcd, and lb groups.
# The lb group lets Ansible configure HAProxy as the load balancing solution.
# Comment lb out if your load balancer is pre-configured.
[OSEv3:children]
masters
nodes
etcd
lb

# Set variables common for all OSEv3 hosts
[OSEv3:vars]
openshift_disable_check=disk_availability,docker_image_availability,docker_storage,memory_availability
ansible_ssh_user=root
deployment_type=origin

# Uncomment the following to enable htpasswd authentication; defaults to
# DenyAllPasswordIdentityProvider.
#openshift_master_identity_providers=[{'name': 'htpasswd_auth', 'login': 'true', 'challenge': 'true', 'kind': 'HTPasswdPasswordIdentityProvider', 'filename': '/etc/origin/master/htpasswd'}]

# Native high availbility cluster method with optional load balancer.
# If no lb group is defined installer assumes that a load balancer has
# been preconfigured. For installation the value of
# openshift_master_cluster_hostname must resolve to the load balancer
# or to one or all of the masters defined in the inventory if no load
# balancer is present.
openshift_master_cluster_method=native
openshift_master_cluster_hostname=master1.vagrant.test
openshift_master_cluster_public_hostname=master1.vagrant.test

# apply updated node defaults
openshift_node_kubelet_args={'pods-per-core': ['10'], 'max-pods': ['250'], 'image-gc-high-threshold': ['90'], 'image-gc-low-threshold': ['80']}

# override the default controller lease ttl
#osm_controller_lease_ttl=30

# enable ntp on masters to ensure proper failover
openshift_clock_enabled=true

# host group for masters
[masters]
master1.vagrant.test openshift_ip=''' + machines['master1']['ip'] + '''
master2.vagrant.test openshift_ip=''' + machines['master2']['ip'] + '''

# host group for etcd
[etcd]
etcd1.vagrant.test openshift_ip=''' + machines['etcd1']['ip'] + '''
etcd2.vagrant.test openshift_ip=''' + machines['etcd2']['ip'] + '''
etcd3.vagrant.test openshift_ip=''' + machines['etcd3']['ip'] + '''

# Specify load balancer host
[lb]
master1.vagrant.test openshift_ip=''' + machines['master1']['ip'] + '''

# host group for nodes, includes region info
[nodes]
master1.vagrant.test openshift_node_labels="{'region': 'infra', 'zone': 'default'}"
master2.vagrant.test openshift_node_labels="{'region': 'infra', 'zone': 'default'}"
node1.vagrant.test openshift_node_labels="{'region': 'primary', 'zone': 'east'}" openshift_ip=''' + machines['node1']['ip'] + '''
node2.vagrant.test openshift_node_labels="{'region': 'primary', 'zone': 'west'}" openshift_ip=''' + machines['node2']['ip'])
		# TODO: deprecation_warnings=False in ansible.cfg
		shutit.send('export ANSIBLE_KEEP_REMOTE_FILES=1') # For debug - see notes
		shutit.send('stty cols 200')
		shutit.multisend('ansible-playbook ~/openshift-ansible/playbooks/byo/openshift-preflight/check.yml',{'ontinue connecting':'yes'},timeout=99999)
		shutit.multisend('ansible-playbook ~/openshift-ansible/playbooks/byo/config.yml',{'ontinue connecting':'yes'},timeout=9999999)
		shutit.logout()
		shutit.logout()
		for machine in sorted(machines.keys()):
			if machine[:4] == 'etcd':
				# not on etcd servers
				continue
			shutit.login(command='vagrant ssh ' + machine)
			shutit.login(command='sudo su - ')
			shutit.send('origin-docker-excluder unexclude || true')
			shutit.install('docker')
			shutit.logout()
			shutit.logout()
		shutit.login(command='vagrant ssh master1',check_sudo=False)
		shutit.login(command='sudo su -',password='vagrant',check_sudo=False)
		shutit.send('stty cols 200')
		shutit.multisend('ansible-playbook ~/openshift-ansible/playbooks/byo/config.yml',{'ontinue connecting':'yes'},timeout=9999999)
		while True:
			shutit.logout()
			shutit.logout()
			shutit.send('vagrant halt')
			vagrant_up(shutit,pw)
			shutit.login(command='vagrant ssh master1',check_sudo=False)
			shutit.login(command='sudo su -',password='vagrant',check_sudo=False)
			shutit.send('stty cols 200')
			shutit.multisend('ansible-playbook ~/openshift-ansible/playbooks/byo/config.yml',{'ontinue connecting':'yes'},timeout=9999999)
			shutit.pause_point('Are we done?')
		#shutit.multisend('ansible-playbook ~/openshift-ansible/playbooks/byo/config.yml',{'ontinue connecting':'yes'}timeout=9999999)
		shutit.send('stty cols 65535')
		shutit.send('git clone https://github.com/openshift/origin')
		shutit.send('cd examples')
		# TODO: https://github.com/openshift/origin/tree/master/examples/data-population
		shutit.logout()
		shutit.logout()
		################################################################################


		################################################################################
		shutit.log('''Vagrantfile created in: ''' + shutit.build['this_vagrant_run_dir'],add_final_message=True,level=logging.DEBUG)
		shutit.log('''Run:

	cd ''' + shutit.build['this_vagrant_run_dir'] + ''' && vagrant status && vagrant landrush ls

To get a picture of what has been set up.''',add_final_message=True,level=logging.DEBUG)
		################################################################################

		return True


	def get_config(self, shutit):
		#shutit.get_config(self.module_id,'vagrant_image',default='centos/7')
		shutit.get_config(self.module_id,'vagrant_image',default='https://cloud.centos.org/centos/7/vagrant/x86_64/images/CentOS-7-x86_64-Vagrant-1804_02.VirtualBox.box')
		shutit.get_config(self.module_id,'vagrant_provider',default='virtualbox')
		shutit.get_config(self.module_id,'gui',default='false')
		shutit.get_config(self.module_id,'memory',default='1024')
		return True

	def test(self, shutit):
		return True

	def finalize(self, shutit):
		return True

	def is_installed(self, shutit):
		return False

	def start(self, shutit):
		return True

	def stop(self, shutit):
		return True

def module():
	return shutit_openshift_cluster_ansible(
		'git.shutit_openshift_cluster_ansible.shutit_openshift_cluster_ansible', 991728875.0001,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.tk.setup','shutit-library.virtualization.virtualization.virtualization','tk.shutit.vagrant.vagrant.vagrant']
	)
