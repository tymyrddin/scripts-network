# Network scripts

Some python scripting network hacks and network system administration.
With many thanks to Black Hat, Gream and ZSecurity.

## Requirements

* A small pentesting lab with kali and a windows 10 (virtual) machines. Host was an Ubuntu 20.04. 
* Python 2.7 and Python 3. Most scripts support both Python 2.7 and Python 3. Only a few only in Python 3. We chose to use `pyenv`. 

For DIY details see the Getting Started section below.

## Scripts

- [x] [MAC changer](mac_changer)
- [x] [Network scanner](network_scanner)
- [x] [ARP spoofer](arp_spoofer)
- [x] [Packet sniffer](packet_sniffer)
- [x] [DNS spoofer](DNS_spoofer)
- [ ] File interceptor
- [ ] Code injector
- [ ] Bypassing HTTPS
- [ ] ARP spoof detector

## Getting started

### Testlab

If the machine you are on supports virtualization, on Ubuntu you can use VMWare and ready-made guests or use KVM and make the virtual machines yourself.
Do not run both virtualizations, or turn off one in `systemctl` when using the other. It's a hassle though.

If you do not have virtualization, you can set up a lab with a few old buckets.

In all cases you can use testing versions from Microsoft (for 90 days). In virtualized machines make a snapshot immediately after install, to return to when time runs out.

#### Use VMWare 
* [Microsoft test VM's](https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/) - 90 days
* [ZSecurity kali linux VM](https://zsecurity.org/download-custom-kali/) - set it to 4G RAM

#### Use KVM
* [Windows 10 enterprise edition iso](https://www.microsoft.com/en-us/evalcenter/evaluate-windows-10-enterprise) - 90 days
* [Windows 10 Home or Pro iso](https://www.microsoft.com/en-in/software-download/windows10ISO) - Though you can download the image for free, you will have to use your own license key later.
* [How To Install Windows 10 on Ubuntu KVM?](https://getlabsdone.com/install-windows-10-on-ubuntu-kvm/)
* [Hosting a Kali Linux virtual machine using KVM on a Ubuntu 20.10 box](https://heds.nz/posts/hosting-kali-linux-kvm-ubuntu/)
* [Running Windows 10 on Linux using KVM with VGA Passthrough](https://www.heiko-sieger.info/running-windows-10-on-linux-using-kvm-with-vga-passthrough/)

### Python 2.7 and Python 3

```shell
Python 2.7 will reach the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 won’t be maintained after that date. A future version of pip will drop support for Python 2.7.
```

Python 2.7 causes lots of bugs due to end of life. But many scripts in kali (and elsewhere) are still in 2.7. 
Choosing to develop on the kali hacking machine in the little pentesting lab

```shell
Python 2.7 will reach the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 won’t be maintained after that date. A future version of pip will drop support for Python 2.7.
```

Python 2.7 causes lots of bugs due to end of life. But many scripts in kali (and elsewhere) are still in 2.7.

Common errors:

```shell
kali:~$ ImportError: No module named <Package Name>
kali:~$ pip: command not found error in Kali Linux
```

Messing about with system files for making scripts not being a good idea, we chose to use `pyenv`:

```shell
kali:~$ sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git
```

Run the installation script:

```shell
kali:~$ curl https://pyenv.run | bash
```

ZSH is the default shell in kali, hence edit the .zshrc file:

```shell
kali:~$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
kali:~$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
kali:~$ echo 'export PATH="$PYENV_ROOT/shims:$PATH"' >> ~/.zshrc
```

And to stop the machine finding the python executable in the `/usr/bin` directory first:
```shell
kali:~$ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc
```

If need be close terminal and open new terminal and run `eval "$(pyenv init -)"` or `source .zshrc`. 
Check the changes with `echo $PATH`.

Configure for having both available:

```shell
kali:~$ exec $SHELL
kali:~$ pyenv install 2.7.18
```

Also install the current python 3 in `pyenv`:

```shell
kali:~$ python -V
<number>
kali:~$ pyenv install <number>
```

List versions available:
```shell
kali:~$ pyenv versions     
* system (set by /home/<user>/.pyenv/version)
  2.7.18
  <number>
```

Set up virtual environment for the project or per subproject, for example:

```shell
kali:~$ cd ymrir/
kali:~$ pyenv which python
/usr/bin/python
kali:~$ pyenv virtualenv 3.9.9 ymrir
...
kali:~$ pyenv local ymrir
kali:~$ python -V
```
