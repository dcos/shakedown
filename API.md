# Using `shakedown` helper methods in your DC/OS tests


## Table of contents

  * [Usage](#usage)
  * [Methods](#methods)
    * General
      * [dcos_url()](#dcos_url)
      * [dcos_service_uri()](#dcos_service_uri)
      * [master_ip()](#master_ip)
    * Packaging
      * [install_package()](#install_package)
      * [install_package_and_wait()](#install_package_and_wait)
      * [uninstall_package()](#uninstall_package)
      * [uninstall_package_and_wait()](#uninstall_package_and_wait)
      * [package_installed()](#package_installed)
    * Command execution
      * [run_command()](#run_command)
      * [run_command_on_master()](#run_command_on_master)
      * [run_command_on_agent()](#run_command_on_agent)
      * [run_dcos_command()](#run_dcos_command)
    * Services
      * [get_service()](#get_service)
      * [get_service_framework_id()](#get_service_framework_id)
      * [get_service_task()](#get_service_task)
      * [get_service_tasks()](#get_service_tasks)
      * [get_service_ips()](#get_service_ips)


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


### dcos_service_uri()

The URI to a named service.

##### *parameters*

parameter | description | type | default
--------- | ----------- | ---- | -------
**service** | the name of the service | str

##### *example usage*

```python
# Print the location of the Jenkins service's dashboard
jenkins_uri = dcos_service_uri('jenkins')
print("Jenkins dashboard located at: " + jenkins_uri)
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
jenkins__tasks = get_service_task('marathon', 'jenkins')
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
