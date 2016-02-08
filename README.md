Pixelated User Agent
====================

[![Build Status](https://snap-ci.com/pixelated/pixelated-user-agent/branch/master/build_image)](https://snap-ci.com/pixelated/pixelated-user-agent/branch/master) [
![Coverage Status](https://coveralls.io/repos/pixelated/pixelated-user-agent/badge.svg?branch=master)](https://coveralls.io/r/pixelated/pixelated-user-agent?branch=master)

The Pixelated User Agent is the mail client of the Pixelated ecosystem. It is composed of two parts, a web interface written in JavaScript ([FlightJS](https://flightjs.github.io/)) and a Python API that interacts with a LEAP Provider, the e-mail platform that Pixelated is built on.

**Pixelated is still in early development state!**

![High level architecture User Agent](https://pixelated-project.org/assets/images/pixelated-user-agent.png)



## Getting started

### Registering with a LEAP provider
  * You can create a developer account at our [Dev Provider](https://dev.pixelated-project.org/).
  * If you want to run your own LEAP provider, see [pixelated-platform](https://github.com/pixelated-project/pixelated-platform).

### Requirements

  * [virtualbox](https://www.virtualbox.org/wiki/Downloads) - Virtualbox is a virtual machine provider platform. It will be used by Vagrant to create a virtual machine ready to run the Pixelated User Agent.
  * [vagrant](https://www.vagrantup.com/downloads.html) - Vagrant is a tool that automates the setup of a virtual machine with the development environment in your computer. Inside the virtual machine's filesystem, this repository will be automatically mounted in the `/vagrant` folder.

### Instructions
The easiest setup is the setup with vagrant, which we will go at greater length. There is a section on setup on the native OS as well.
For server setup, see [debian package](#debian-package) below.


#### Developer Setup With Vagrant
Please ensure that:
  * You have an email user from your preferred leap provider ([How to](#registering-with-a-leap-provider)).
  * Installed both vagrant and virtualbox or libvirt ([How to](#requirements)).
  
To setup the pixelated user agent inside a vagrant machine, please copy-paste the following command to a terminal:

```bash
 curl https://raw.githubusercontent.com/pixelated/pixelated-user-agent/master/vagrant_setup.sh | sh
```

This could take a while depending on your internet connection.
Once it is complete, you should be within the terminal of the vagrant box.

To run the pixelated user agent single user mode, please run the following:

```bash
 (user-agent-venv)vagrant@jessie:/vagrant$ pixelated-user-agent --host 0.0.0.0 -lc /vagrant/service/pixelated/certificates/dev.pixelated-project.org.ca.crt
```
You will then need to input your provider hostname, email username and password. Please follow the prompt. Please remove the `-lc` part of the command if your leap provider has a proper certificate setup.
Once that is done, you can use by browsing to [http://localhost:3333](http://localhost:3333)
 
To run the pixelated user agent multi user mode, please run the following:
```bash
 (user-agent-venv)vagrant@jessie:/vagrant$ pixelated-user-agent --host 0.0.0.0 -lc /vagrant/service/pixelated/certificates/dev.pixelated-project.org.ca.crt --multi-user --provider='dev.pixelated-project.org'
```
You will need to change dev.pixelated-project.org to the hostname of the leap provider that you will be using. Please remove the `-lc` part of the command if your leap provider has a proper certificate setup.   
Once that is done, you can use by browsing to [http://localhost:3333](http://localhost:3333), where you will be prompted for your email username and password.
 
To run the backend test:

```bash
 (user-agent-venv)vagrant@jessie:/vagrant$ cd service
 (user-agent-venv)vagrant@jessie:/vagrant/service$ ./go test 
```

To run the frontend test:

```bash
 (user-agent-venv)vagrant@jessie:/vagrant$ cd web-ui
 (user-agent-venv)vagrant@jessie:/vagrant/web-ui$ ./go test 
```

To run the functional test:

```bash
 (user-agent-venv)vagrant@jessie:/vagrant$ cd service
 (user-agent-venv)vagrant@jessie:/vagrant/service$ ./go functional 
```

Continuous Integration:
All commits to the pixelated user agent code trigger all tests to be run in [snap-ci](https://snap-ci.com/pixelated/pixelated-user-agent/branch/master).

Please note:
* You can access the guest OS shell via the command `vagrant ssh` run within the pixelated-user-agent/ folder in the host OS
* /vagrant/ in the guest OS is mapped to the pixelated-user-agent/ folder in the host OS. File changes on either side will reflect in the other.
* First time email sync could be slow, please be patient. This could be the case if you have a lot of emails already and it is the first time you setup the user agent on your machine.
* CTRL + \ will stop the server
* For all backend changes, you will need to restart the server
* For most frontend changes, you will ust need to reload the browser. Some changes (in particular, those involving css or handlebars) you will need run:
```bash
 (user-agent-venv)vagrant@jessie:/vagrant$ cd web-ui
 (user-agent-venv)vagrant@jessie:/vagrant/web-ui$ ./go build 
```
#### Developer Setup On Native OS
You will need to install python, pip, npm and openssl. On mac, please use homebrew. On debian/ubuntu, please use apt or aptitude.
You will then need to run:

```bash
$ git clone https://github.com/pixelated/pixelated-user-agent.git
$ cd pixelated-user-agent/service
$ ./go setup
```

There have been reports of issues on setting up on native OS. Please follow instructions from the output of homebrew. You might need to install compass as a GEM as well.
Please ping us on IRC ([#pixelated on irc.freenode.net](irc://irc.freenode.net/pixelated)), we will be available to help you from there.

Running the user agent, and the various tests is the same as in the [vagrant setup](#developer-setup-with-vagrant) above.

## Debian package

For people that just want to try the user agent, we have debian packages available in our [repository](http://packages.pixelated-project.org/debian/). To use it you have to add it to your sources list:

```shell

echo "deb http://packages.pixelated-project.org/debian jessie-snapshots main" > /etc/apt/sources.list.d/pixelated.list

apt-key adv --keyserver pool.sks-keyservers.net --recv-key 287A1542472DC0E3

apt-get update

apt-get install pixelated-user-agent
```
