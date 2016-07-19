# Using `shakedown` helper methods in your DC/OS tests


## Table of contents

  * [Usage](#usage)
  * [Methods](#methods)
    * General
      * [dcos_url()](#dcos_url)
      * [dcos_service_url()](#dcos_service_url)
      * [dcos_state()](#dcos_state)
      * [dcos_version()](#dcos_version)
      * [dcos_acs_token()](#dcos_acs_token)
      * [master_ip()](#master_ip)
    * Packaging
      * [install_package()](#install_package)
      * [install_package_and_wait()](#install_package_and_wait)
      * [uninstall_package()](#uninstall_package)
      * [uninstall_package_and_wait()](#uninstall_package_and_wait)
      * [package_installed()](#package_installed)
      * [get_package_repos()](#get_package_repos)
      * [add_package_repo()](#add_package_repo)
      * [remove_package_repo()](#remove_package_repo)
    * Command execution
      * [run_command()](#run_command)
      * [run_command_on_master()](#run_command_on_master)
      * [run_command_on_agent()](#run_command_on_agent)
      * [run_dcos_command()](#run_dcos_command)
    * File operations
      * [copy_file()](#copy_file)
      * [copy_file_to_master()](#copy_file_to_master)
      * [copy_file_to_agent()](#copy_file_to_agent)
      * [copy_file_from_master()](#copy_file_from_master)
      * [copy_file_from_agent()](#copy_file_from_agent)
    * Services
      * [get_service()](#get_service)
      * [get_service_framework_id()](#get_service_framework_id)
      * [get_service_task()](#get_service_task)
      * [get_service_tasks()](#get_service_tasks)
      * [get_service_ips()](#get_service_ips)
      * [get_marathon_task()](#get_marathon_task)
      * [get_marathon_tasks()](#get_marathon_tasks)
      * [service_healthy()](#service_healthy)
      * [wait_for_service_endpoint()](#wait_for_service_endpoint)
    * Tasks
      * [get_task()](#get_task)
      * [get_tasks()](#get_tasks)
      * [get_active_tasks()](#get_active_tasks)
      * [task_completed()](#task_completed)
    * ZooKeeper
      * [delete_zk_node()](#delete_zk_node)
    * Agents
      * [get_agents()](#get_agents)
      * [get_private_agents()](#get_private_agents)
      * [get_public_agents()](#get_public_agents)
      * [partition_agent()](#partition_agent)
      * [reconnect_agent()](#reconnect_agent)


## Usage

`from shakedown import *`


## Methods

### dcos_url()

The URL to the DC/OS cluster under test.

##### *parameters*

None.

##### *example usage*

```python
# Print the DC/OS dashboard URL.
dcos_url = dcos_url()
print("Dashboard located at: " + dcos_url)
```


### dcos_service_url()

The URI to a named service.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**service** | the name of the service | str

##### *example usage*

```python
# Print the location of the Jenkins service's dashboard
jenkins_url = dcos_service_url('jenkins')
print("Jenkins dashboard located at: " + jenkins_url)
```


### dcos_state()

A JSON hash containing DC/OS state information.

#### *parameters*

None.

#### *example usage*

```python
# Print state information of DC/OS slaves.
state_json = json.loads(dcos_json_state())
print(state_json['slaves'])
```


### dcos_version()

The DC/OS version number.

##### *parameters*

None.

##### *example usage*

```python
# Print the DC/OS version.
dcos_version = dcos_version()
print("Cluster is running DC/OS version " + dcos_version)
```


### dcos_acs_token()

The DC/OS ACS token (if authenticated).

##### *parameters*

None.

##### *example usage*

```python
# Print the DC/OS ACS token.
token = dcos_acs_token()
print("Using token " + token)
```



### master_ip()

The current Mesos master's IP address.

##### *parameters*

None.

##### *example usage*

```python
# What's our Mesos master's IP?
master_ip = master_ip()
print("Current Mesos master: " + master_ip)
```


### install_package()

Install a package.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**package_name** | the name of the package to install | str
package_version | the version of the package to install | str | *latest*
app_id | custom app ID | str | `None`
options_file | ? | ? | `None`
wait_for_completion | wait for service to become healthy before completing? | bool | `False`
timeout_sec | how long in seconds to wait before timing out | int | `600`

##### *example usage*

```python
# Install the 'jenkins' package; don't wait the service to register
install_package('jenkins')
```


### install_package_and_wait()

Install a package, and wait for the service to register.

*This method uses the same parameters as [`install_package()`](#install_package)*


### uninstall_package()

Uninstall a package.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**package_name** | the name of the package to install | str
app_id | custom app ID | str | `None`
all_instances | uninstall all instances? | bool | `False`
wait_for_completion | wait for service to become healthy before completing? | bool | `False`
timeout_sec | how long in seconds to wait before timing out | int | `600`

##### *example usage*

```python
# Uninstall the 'jenkins' package; don't wait for the service to unregister
uninstall_package('jenkins')
```


### uninstall_package_and_wait()

Uninstall a package, and wait for the service to unregister.

*This method uses the same parameters as [`uninstall_package()`](#uninstall_package)*


### package_installed()

Check whether a specified package is currently installed.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**package_name** | the name of the package to install | str
app_id | custom app ID | str | `None`

##### *example usage*

```python
# Is the 'jenkins' package installed?
if package_installed('jenkins'):
    print('Jenkins is installed!')
```


### add_package_repo()

Add a repository to the list of package sources.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**repo_name** | the name of the repository | str
**repo_url** | the location of the repository | str
index | the repository index order | int | *-1*

##### *example usage*

```python
# Search the Multiverse before any other repositories
add_package_repo('Multiverse', 'https://github.com/mesosphere/multiverse/archive/version-2.x.zip', 0)
```


### remove_package_repo()

Remove a repository from the list of package sources.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**repo_name** | the name of the repository | str

##### *example usage*

```python
# No longer search the Multiverse
remove_package_repo('Multiverse')
```


### get_package_repos()

Retrieve a dictionary describing the configured package source repositories.

##### *parameters*

None

##### *example usage*

```python
# Which repository am I searching through first?
repos = get_package_repos()
print("First searching " + repos['repositories'][0]['name'])
```


### run_command()

Run a command on a remote host via SSH.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**host** | the hostname or IP to run the command on | str
**command** | the command to run | str
username | the username used for SSH authentication | str | `core`
key_path | the path to the SSH keyfile used for authentication | str | `None`

##### *example usage*

```python
# I wonder what /etc/motd contains on the Mesos master?
run_command(master_ip(), 'cat /etc/motd')
```


### run_command_on_master()

Run a command on the Mesos master via SSH.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**command** | the command to run | str
username | the username used for SSH authentication | str | `core`
key_path | the path to the SSH keyfile used for authentication | str | `None`

##### *example usage*

```python
# What kernel is our Mesos master running?
run_command_on_master('uname -a')
```


### run_command_on_agent()

Run a command on a Mesos agent via SSH, proxied via the Mesos master.

*This method uses the same parameters as [`run_command()`](#run_command)*


### run_dcos_command()

Run a command using the `dcos` CLI.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**command** | the command to run | str

##### *example usage*

```python
# What's the current version of the Jenkins package?
result, error = run_dcos_command('package search jenkins --json')
result_json = json.loads(result)
print(result_json['packages'][0]['currentVersion'])
```


### copy_file()

Copy a file via SCP.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**host** | the hostname or IP to copy the file to/from | str
**file_path** | the local path to the file to be copied | str
remote_path | the remote path to copy the file to | str | `.`
username | the username used for SSH authentication | str | `core`
key_path | the path to the SSH keyfile used for authentication | str | `None`
action | 'put' (default) or 'get' | str | `put`

##### *example usage*

```python
# Copy a datafile onto the Mesos master
copy_file(master_ip(), '/var/data/datafile.txt')
```


### copy_file_to_master()

Copy a file to the Mesos master.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**file_path** | the local path to the file to be copied | str
remote_path | the remote path to copy the file to | str | `.`
username | the username used for SSH authentication | str | `core`
key_path | the path to the SSH keyfile used for authentication | str | `None`

##### *example usage*

```python
# Copy a datafile onto the Mesos master
copy_file_to_master('/var/data/datafile.txt')
```


### copy_file_to_agent()

Copy a file to a Mesos agent, proxied through the Mesos master.

*This method uses the same parameters as [`copy_file()`](#copy_file)*


### copy_file_from_master()

Copy a file from the Mesos master.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**remote_path** | the remote path of the file to copy | str |
file_path | the local path to copy the file to | str | `.`
username | the username used for SSH authentication | str | `core`
key_path | the path to the SSH keyfile used for authentication | str | `None`

##### *example usage*

```python
# Copy a datafile from the Mesos master
copy_file_from_master('/var/data/datafile.txt')
```


### copy_file_from_agent()

Copy a file from a Mesos agent, proxied through the Mesos master.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**host** | the hostname or IP to copy the file from | str
**remote_path** | the remote path of the file to copy | str
file_path | the local path to copy the file to | str | `.`
username | the username used for SSH authentication | str | `core`
key_path | the path to the SSH keyfile used for authentication | str | `None`

##### *example usage*

```python
# Copy a datafile from an agent running Jenkins
service_ips = get_service_ips('marathon', 'jenkins')
for host in service_ips:
    assert copy_file_from_agent(host, '/home/jenkins/datafile.txt')
```


### get_service()

Retrieve a dictionary describing a named service.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**service_name** | the name of the service | str
inactive | include inactive services? | bool | `False`
completed | include completed services? | bool | `False`

##### *example usage*

```python
# Tell me about the 'jenkins' service
jenkins = get_service('jenkins')
```


### get_service_framework_id()

Get the framework ID of a named service.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**service_name** | the name of the service | str
inactive | include inactive services? | bool | `False`
completed | include completed services? | bool | `False`

##### *example usage*

```python
# What is the framework ID for the 'jenkins' service?
jenkins_framework_id = get_framework_id('jenkins')
```


### get_service_task()

Get a dictionary describing a named service task.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**service_name** | the name of the service | str
**task_name** | the name of the task | str
inactive | include inactive services? | bool | `False`
completed | include completed services? | bool | `False`

##### *example usage*

```python
# Tell me about marathon's 'jenkins' task
jenkins_tasks = get_service_task('marathon', 'jenkins')
```


### get_service_tasks()

Get a list of task IDs associated with a named service.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**service_name** | the name of the service | str
inactive | include inactive services? | bool | `False`
completed | include completed services? | bool | `False`

##### *example usage*

```python
# What's marathon doing right now?
service_tasks = get_service_tasks('marathon')
```


### get_marathon_task()

Get a dictionary describing a named Marathon task.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**task_name** | the name of the task | str
inactive | include inactive services? | bool | `False`
completed | include completed services? | bool | `False`

##### *example usage*

```python
# Tell me about marathon's 'jenkins' task
jenkins_tasks = get_marathon_task('jenkins')
```


### get_marathon_tasks()

Get a list of Marathon tasks.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
inactive | include inactive services? | bool | `False`
completed | include completed services? | bool | `False`

##### *example usage*

```python
# What's marathon doing right now?
service_tasks = get_marathon_tasks()
```


### get_service_ips()

Get a set of the IPs associated with a service.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**service_name** | the name of the service | str
task_name | the name of the task to limit results to | str | `None`
inactive | include inactive services? | bool | `False`
completed | include completed services? | bool | `False`

##### *example usage*

```python
# Get all IPs associated with the 'chronos' task running in the 'marathon' service
service_ips = get_service_ips('marathon', 'chronos')
print('service_ips: ' + str(service_ips))
```

### service_healthy()

Check whether a specified service is currently healthy.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**service_name** | the name of the service | str

##### *example usage*

```python
# Is the 'jenkins' service healthy?
if service_healthy('jenkins'):
    print('Jenkins is healthy!')
```

### wait_for_service_endpoint()

Checks the service url returns HTTP 200 within a timeout if available it returns true on expiration it returns false.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**service_name** | the name of the service | str
timeout_sec | how long in seconds to wait before timing out | int | `120`

##### *example usage*

```python
# will wait
wait_for_service_endpoint("marathon-user")
```

### get_task()

Get information about a task.

*This method uses the same parameters as [`get_tasks()`](#get_tasks)*


### get_tasks()

Get a list of tasks, optionally filtered by task name.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
task_name | the nameof the task | str
completed | include completed tasks? | `True`

##### *example usage*

```python
# What tasks have been run?
tasks = get_tasks()
for task in tasks:
    print("{} has state {}".format(task['id'], task['state']))
```


### get_active_tasks()

Get a list of active tasks, optionally filtered by task name.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
task_name | the nameof the task | str
completed | include completed tasks? | `False`

##### *example usage*

```python
# What tasks are running?
tasks = get_active_tasks()
for task in tasks:
    print("{} has state {}".format(task['id'], task['state']))
```


### task_completed()

Check whether a task has completed.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
task_name | the nameof the task | str

##### *example usage*

```python
# Wait for task 'driver-20160517222552-0072' to complete
while not task_completed('driver-20160517222552-0072'):
    print('Task not complete; sleeping...')
    time.sleep(5)
```


### delete_zk_node()

Delete a named ZooKeeper node.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
node_name | the name of the node | str

##### *example usage*

```python
# Delete a 'universe/marathon-user' ZooKeeper node
delete_zk_node('universe/marathon-user')
```


### get_agents()

Retrieve a list of all agent node IP addresses.

##### *parameters*

None

##### *example usage*

```python
# What do I look like in IP space?
nodes = get_agents()
print("Node IP addresses: " + nodes)
```

### get_agents()

Retrieve a list of all agent node IP addresses.

##### *parameters*

None

##### *example usage*

```python
# What do I look like in IP space?
private_nodes = get_private_agents()
print("Private IP addresses: " + private_nodes)
```


### get_public_agents()

Retrieve a list of all public agent node IP addresses.

##### *parameters*

None

##### *example usage*

```python
# What do I look like in IP space?
public_nodes = get_public_agents()
print("Public IP addresses: " + public_nodes)
```

### partition_agent()

Separates the agent from the cluster by adjusting IPTables with the following:

```
sudo iptables -F INPUT
sudo iptables -I INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -I INPUT -p icmp -j ACCEPT
sudo iptables -I OUTPUT -p tcp --sport 5051  -j REJECT
sudo iptables -A INPUT -j REJECT
```

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
hostname | the hostname or IP of the node | str

##### *example usage*

```python
# Partition all the public nodes
public_nodes = get_public_agents()
for public_node in public_nodes:
    partition_agent(public_node)
```
### reconnect_agent()

Reconnects a previously partitioned agent by reversing the IPTable changes.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
hostname | the hostname or IP of the node | str

##### *example usage*

```python
# Reconnect the public agents
for public_node in public_nodes:
    reconnect_agent(public_node)
```
