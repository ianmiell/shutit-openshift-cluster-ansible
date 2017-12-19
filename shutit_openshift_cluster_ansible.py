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
if [[ $(command -v virsh) ]] && [[ $(kvm-ok 2>&1 | command grep 'can be used') != '' ]]
then
	virsh list | grep ${MODULE_NAME} | awk '{print $1}' | xargs -n1 virsh destroy
fi
''')
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
    vb.memory = "''' + memory + '''"
  end

  config.vm.define "openshiftansible1" do |openshiftansible1|
    openshiftansible1.vm.box = ''' + '"' + vagrant_image + '"' + '''
    openshiftansible1.vm.hostname = "openshiftansible1.vagrant.test"
    config.vm.provider :virtualbox do |vb|
      vb.name = "shutit_openshift_cluster_ansible_1"
    end
  end
  config.vm.define "openshiftansible2" do |openshiftansible2|
    openshiftansible2.vm.box = ''' + '"' + vagrant_image + '"' + '''
    openshiftansible2.vm.hostname = "openshiftansible2.vagrant.test"
    config.vm.provider :virtualbox do |vb|
      vb.name = "shutit_openshift_cluster_ansible_2"
    end
  end
  config.vm.define "openshiftansible3" do |openshiftansible3|
    openshiftansible3.vm.box = ''' + '"' + vagrant_image + '"' + '''
    openshiftansible3.vm.hostname = "openshiftansible3.vagrant.test"
    config.vm.provider :virtualbox do |vb|
      vb.name = "shutit_openshift_cluster_ansible_3"
    end
  end
  config.vm.define "openshiftansible4" do |openshiftansible4|
    openshiftansible4.vm.box = ''' + '"' + vagrant_image + '"' + '''
    openshiftansible4.vm.hostname = "openshiftansible4.vagrant.test"
    config.vm.provider :virtualbox do |vb|
      vb.name = "shutit_openshift_cluster_ansible_4"
    end
  end
  config.vm.define "openshiftansible5" do |openshiftansible5|
    openshiftansible5.vm.box = ''' + '"' + vagrant_image + '"' + '''
    openshiftansible5.vm.hostname = "openshiftansible5.vagrant.test"
    config.vm.provider :virtualbox do |vb|
      vb.name = "shutit_openshift_cluster_ansible_5"
    end
  end
  config.vm.define "openshiftansible6" do |openshiftansible6|
    openshiftansible6.vm.box = ''' + '"' + vagrant_image + '"' + '''
    openshiftansible6.vm.hostname = "openshiftansible6.vagrant.test"
    config.vm.provider :virtualbox do |vb|
      vb.name = "shutit_openshift_cluster_ansible_6"
    end
  end
  config.vm.define "openshiftansible7" do |openshiftansible7|
    openshiftansible7.vm.box = ''' + '"' + vagrant_image + '"' + '''
    openshiftansible7.vm.hostname = "openshiftansible7.vagrant.test"
    config.vm.provider :virtualbox do |vb|
      vb.name = "shutit_openshift_cluster_ansible_7"
    end
  end
end''')
		pw = shutit.get_env_pass()
		try:
			shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'] + " openshiftansible1",{'assword for':pw,'assword:':pw},timeout=99999)
		except NameError:
			shutit.multisend('vagrant up openshiftansible1',{'assword for':pw,'assword:':pw},timeout=99999)
		if shutit.send_and_get_output("""vagrant status 2> /dev/null | grep -w ^openshiftansible1 | awk '{print $2}'""") != 'running':
			shutit.pause_point("machine: openshiftansible1 appears not to have come up cleanly")
		try:
			shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'] + " openshiftansible2",{'assword for':pw,'assword:':pw},timeout=99999)
		except NameError:
			shutit.multisend('vagrant up openshiftansible2',{'assword for':pw,'assword:':pw},timeout=99999)
		if shutit.send_and_get_output("""vagrant status 2> /dev/null | grep -w ^openshiftansible2 | awk '{print $2}'""") != 'running':
			shutit.pause_point("machine: openshiftansible2 appears not to have come up cleanly")
		try:
			shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'] + " openshiftansible3",{'assword for':pw,'assword:':pw},timeout=99999)
		except NameError:
			shutit.multisend('vagrant up openshiftansible3',{'assword for':pw,'assword:':pw},timeout=99999)
		if shutit.send_and_get_output("""vagrant status 2> /dev/null | grep -w ^openshiftansible3 | awk '{print $2}'""") != 'running':
			shutit.pause_point("machine: openshiftansible3 appears not to have come up cleanly")
		try:
			shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'] + " openshiftansible4",{'assword for':pw,'assword:':pw},timeout=99999)
		except NameError:
			shutit.multisend('vagrant up openshiftansible4',{'assword for':pw,'assword:':pw},timeout=99999)
		if shutit.send_and_get_output("""vagrant status 2> /dev/null | grep -w ^openshiftansible4 | awk '{print $2}'""") != 'running':
			shutit.pause_point("machine: openshiftansible4 appears not to have come up cleanly")
		try:
			shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'] + " openshiftansible5",{'assword for':pw,'assword:':pw},timeout=99999)
		except NameError:
			shutit.multisend('vagrant up openshiftansible5',{'assword for':pw,'assword:':pw},timeout=99999)
		if shutit.send_and_get_output("""vagrant status 2> /dev/null | grep -w ^openshiftansible5 | awk '{print $2}'""") != 'running':
			shutit.pause_point("machine: openshiftansible5 appears not to have come up cleanly")
		try:
			shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'] + " openshiftansible6",{'assword for':pw,'assword:':pw},timeout=99999)
		except NameError:
			shutit.multisend('vagrant up openshiftansible6',{'assword for':pw,'assword:':pw},timeout=99999)
		if shutit.send_and_get_output("""vagrant status 2> /dev/null | grep -w ^openshiftansible6 | awk '{print $2}'""") != 'running':
			shutit.pause_point("machine: openshiftansible6 appears not to have come up cleanly")
		try:
			shutit.multisend('vagrant up --provider ' + shutit.cfg['shutit-library.virtualization.virtualization.virtualization']['virt_method'] + " openshiftansible7",{'assword for':pw,'assword:':pw},timeout=99999)
		except NameError:
			shutit.multisend('vagrant up openshiftansible7',{'assword for':pw,'assword:':pw},timeout=99999)
		if shutit.send_and_get_output("""vagrant status 2> /dev/null | grep -w ^openshiftansible7 | awk '{print $2}'""") != 'running':
			shutit.pause_point("machine: openshiftansible7 appears not to have come up cleanly")


		# machines is a dict of dicts containing information about each machine for you to use.
		machines = {}
		machines.update({'openshiftansible1':{'fqdn':'openshiftansible1.vagrant.test'}})
		ip = shutit.send_and_get_output('''vagrant landrush ls 2> /dev/null | grep -w ^''' + machines['openshiftansible1']['fqdn'] + ''' | awk '{print $2}' ''')
		machines.get('openshiftansible1').update({'ip':ip})
		machines.update({'openshiftansible2':{'fqdn':'openshiftansible2.vagrant.test'}})
		ip = shutit.send_and_get_output('''vagrant landrush ls 2> /dev/null | grep -w ^''' + machines['openshiftansible2']['fqdn'] + ''' | awk '{print $2}' ''')
		machines.get('openshiftansible2').update({'ip':ip})
		machines.update({'openshiftansible3':{'fqdn':'openshiftansible3.vagrant.test'}})
		ip = shutit.send_and_get_output('''vagrant landrush ls 2> /dev/null | grep -w ^''' + machines['openshiftansible3']['fqdn'] + ''' | awk '{print $2}' ''')
		machines.get('openshiftansible3').update({'ip':ip})
		machines.update({'openshiftansible4':{'fqdn':'openshiftansible4.vagrant.test'}})
		ip = shutit.send_and_get_output('''vagrant landrush ls 2> /dev/null | grep -w ^''' + machines['openshiftansible4']['fqdn'] + ''' | awk '{print $2}' ''')
		machines.get('openshiftansible4').update({'ip':ip})
		machines.update({'openshiftansible5':{'fqdn':'openshiftansible5.vagrant.test'}})
		ip = shutit.send_and_get_output('''vagrant landrush ls 2> /dev/null | grep -w ^''' + machines['openshiftansible5']['fqdn'] + ''' | awk '{print $2}' ''')
		machines.get('openshiftansible5').update({'ip':ip})
		machines.update({'openshiftansible6':{'fqdn':'openshiftansible6.vagrant.test'}})
		ip = shutit.send_and_get_output('''vagrant landrush ls 2> /dev/null | grep -w ^''' + machines['openshiftansible6']['fqdn'] + ''' | awk '{print $2}' ''')
		machines.get('openshiftansible6').update({'ip':ip})
		machines.update({'openshiftansible7':{'fqdn':'openshiftansible7.vagrant.test'}})
		ip = shutit.send_and_get_output('''vagrant landrush ls 2> /dev/null | grep -w ^''' + machines['openshiftansible7']['fqdn'] + ''' | awk '{print $2}' ''')
		machines.get('openshiftansible7').update({'ip':ip})


		shutit.login(command='vagrant ssh ' + sorted(machines.keys())[0],check_sudo=False)
		shutit.login(command='sudo su -',password='vagrant',check_sudo=False)
		shutit.logout()
		shutit.logout()
		shutit.log('''Vagrantfile created in: ''' + shutit.build['this_vagrant_run_dir'],add_final_message=True,level=logging.DEBUG)
		shutit.log('''Run:

	cd ''' + shutit.build['this_vagrant_run_dir'] + ''' && vagrant status && vagrant landrush ls

To get a picture of what has been set up.''',add_final_message=True,level=logging.DEBUG)

		return True


	def get_config(self, shutit):
		shutit.get_config(self.module_id,'vagrant_image',default='ubuntu/xenial64')
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