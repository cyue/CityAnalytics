
**Description**

Generally, we give two options for system deployment and invocation: one is that the one can run scripts in respect of only some part of the whole application he interests, we divide the ansible auto-deploy script into modules, each module concerns an aspect of functionality of the application; another is simpler with only two scripts to run. We strongly recommend the demonstrator follow the former scheme, i.e. execute each module separately. Because the analysis script consumes too much time which could hinder the demonstration, so you may want to execute it at last in demonstration situation. Before running anything, you need to make sure the working environment is Linux and pre installed Python and Ansible. In below, we firstly gives step-by-step instruction of the first option and meanwhile illustrate functionality of each module:

1. Run the following command in current directory to initialize 4 Ubuntu VMs on Nectar 
  * ***“python cloud_a2_boto.py [your nectar access id] [your nectar access key] [instance key name]”***
2. You could run the script without any arguments, the script will use the default arguments, but that may fail because the default account may run out of allocated resource.  
3. Go to directory “cloud_asg” and edit file “ansible_hosts” to replace the IP address with your remote VMs on nectar. Make sure IPs under “[cloud_asg]” include IPs under “[app]” in file “ansible_hosts”
4. Add your Nectar instance access key file in directory “cloud_asg” and replace the private key file name in “ansible.cfg” in the same directory. Alternatively, you can do nothing on this step, then the following steps will deploy all on our nectar VMs. 
5. Run the following command in “cloud_asg/ansible” directory to create working directory on remote Nectar VMs
  * ***“ansible-playbook roles/create_workdir/tasks/create_workdir.yml”***
6. Run the following command in “cloud_asg/ansible” directory to deploy CouchDB on remote Nectar VMs
  * ***“ansible-playbook roles/couchdb/tasks/deploy_couchdb.yml”***
7. Run the following command in “cloud_asg/ansible” directory to install all packages in need on remote Nectar VMs
  * ***“ansible-playbook roles/pkg_installation/tasks/install_pkg.yml”***
8. Run the following command in “cloud_asg/ansible” directory to deploy tweets harvest scripts and run harvest scripts on remote Nectar VMs
  * ***“ansible-playbook roles/harvest/tasks/deploy_harvest.yml”***
9. Run the following command in “cloud_asg/ansible” directory to deploy analysis scripts and run all analytic scripts on remote Nectar VMs
  * ***“ansible-playbook roles/scenario/tasks/deploy_analytics.yml”***
10. Run the following command in “cloud_asg/ansible” directory to deploy web server and start the web server on remote Nectar VMs
  * ***“ansible-playbook roles/webserver/tasks/deploy_webserver.yml”***

Now, you can check the website and analytic results on “http://[your webserver IP]/” (IP defined in “ansible_hosts” under section [app]). 

Alternatively, you can run the following command to replace step 5 to step 10:
  * ***“ansible-playbook deploy_env.yml”***
  * ***“ansible-playbook deploy_app.yml”***

