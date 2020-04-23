#!/usr/bin/python

# Copyright 2013-present Barefoot Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from p4_mininet import P4Switch, P4Host

import thread
import argparse
import threadpool
from time import sleep
import os
import subprocess
import commands
import time,threading
from multiprocessing import Pool


_THIS_DIR = os.path.dirname(os.path.realpath(__file__))
_THRIFT_BASE_PORT = 22222

parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", required=True)
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", required=True)
parser.add_argument('--cli', help='Path to BM CLI',
                    type=str, action="store", required=True)
parser.add_argument('--mode', choices=['l2', 'l3'], type=str, default='l3')
parser.add_argument('--without-pcap', help='Cleanup output pcap files',
                    type=str, choices=['y', 'n'], default='n')
args = parser.parse_args()

sw_macs = []
sw_addrs = []

class MyTopo(Topo):
    def __init__(self, sw_path, json_path, nb_hosts, nb_switches, links, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        for i in xrange(nb_switches):
          if(i == 0):
           s1=self.addSwitch('s%d' % (i + 1),
                            sw_path = sw_path,
                            json_path = json_path,
                            thrift_port = _THRIFT_BASE_PORT + i,
                            pcap_dump = True,
                            device_id = i)
          if(i == 1):
           s2=self.addSwitch('s%d' % (i + 1),
                            sw_path = sw_path,
                            json_path = json_path,
                            thrift_port = _THRIFT_BASE_PORT + i,
                            pcap_dump = True,
                            device_id = i)
          if(i == 2):
           s3=self.addSwitch('s%d' % (i + 1),
                            sw_path = sw_path,
                            json_path = json_path,
                            thrift_port = _THRIFT_BASE_PORT + i,
                            pcap_dump = True,
                            device_id = i)
          if(i == 3):
           s4=self.addSwitch('s%d' % (i + 1),
                            sw_path = sw_path,
                            json_path = json_path,
                            thrift_port = _THRIFT_BASE_PORT + i,
                            pcap_dump = True,
                            device_id = i)
          if(i == 4):
           s5=self.addSwitch('s%d' % (i + 1),
                            sw_path = sw_path,
                            json_path = json_path,
                            thrift_port = _THRIFT_BASE_PORT + i,
                            pcap_dump = True,
                            device_id = i)
          if(i == 5):
           s6=self.addSwitch('s%d' % (i + 1),
                            sw_path = sw_path,
                            json_path = json_path,
                            thrift_port = _THRIFT_BASE_PORT + i,
                            pcap_dump = True,
                            device_id = i)


        for h in xrange(nb_hosts):
          if(h == 0):
            h1=self.addHost('h%d' % (h + 1), ip="10.0.0.%d" % (h + 1),
                    mac="00:00:00:00:00:0%d" % (h+1))
            addrv = "10.0.0.%d" % (h+1)
            macv = "00:00:00:00:00:0%d" % (h+1)
            sw_addrs.append(addrv)
            sw_macs.append(macv)
          if(h == 1):
            h2=self.addHost('h%d' % (h + 1), ip="10.0.0.%d" % (h + 1),
                    mac="00:00:00:00:00:0%d" % (h+1))
            addrv = "10.0.0.%d" % (h+1)
            macv = "00:00:00:00:00:0%d" % (h+1)
            sw_addrs.append(addrv)
            sw_macs.append(macv)
          if(h == 2):
            h3=self.addHost('h%d' % (h + 1), ip="10.0.0.%d" % (h + 1),
                    mac="00:00:00:00:00:0%d" % (h+1))
            addrv = "10.0.0.%d" % (h+1)
            macv = "00:00:00:00:00:0%d" % (h+1)
            sw_addrs.append(addrv)
            sw_macs.append(macv)
          if(h == 3):
            h4=self.addHost('h%d' % (h + 1), ip="10.0.0.%d" % (h + 1),
                    mac="00:00:00:00:00:0%d" % (h+1))
            addrv = "10.0.0.%d" % (h+1)
            macv = "00:00:00:00:00:0%d" % (h+1)
            sw_addrs.append(addrv)
            sw_macs.append(macv)
          if(h == 4):
            h5=self.addHost('h%d' % (h + 1), ip="10.0.0.%d" % (h + 1),
                    mac="00:00:00:00:00:0%d" % (h+1))
            addrv = "10.0.0.%d" % (h+1)
            macv = "00:00:00:00:00:0%d" % (h+1)
            sw_addrs.append(addrv)
            sw_macs.append(macv)
          if(h == 5):
            h6=self.addHost('h%d' % (h + 1), ip="10.0.0.%d" % (h + 1),
                    mac="00:00:00:00:00:0%d" % (h+1))
            addrv = "10.0.0.%d" % (h+1)
            macv = "00:00:00:00:00:0%d" % (h+1)
            sw_addrs.append(addrv)
            sw_macs.append(macv)
          if(h == 6):
            h7=self.addHost('h%d' % (h + 1), ip="10.0.0.%d" % (h + 1),
                    mac="00:00:00:00:00:0%d" % (h+1))
            addrv = "10.0.0.%d" % (h+1)
            macv = "00:00:00:00:00:0%d" % (h+1)
            sw_addrs.append(addrv)
            sw_macs.append(macv)
          if(h == 7):
            h8=self.addHost('h%d' % (h + 1), ip="10.0.0.%d" % (h + 1),
                    mac="00:00:00:00:00:0%d" % (h+1))
            addrv = "10.0.0.%d" % (h+1)
            macv = "00:00:00:00:00:0%d" % (h+1)
            sw_addrs.append(addrv)
            sw_macs.append(macv)

       # for a, b in links:
            d='1ms'
            self.addLink(h1, s1,bw=20,max_queue_size=256,delay=d)
            self.addLink(h2, s1,bw=20,max_queue_size=256,delay=d)
            self.addLink(h3, s1,bw=20,max_queue_size=256,delay=d)
            self.addLink(h4, s1,bw=20,max_queue_size=256,delay=d)
            self.addLink(s1, s2,bw=20,max_queue_size=256,delay=d)
            self.addLink(s1, s3,bw=20,max_queue_size=256,delay=d)
            self.addLink(s1, s4,bw=20,max_queue_size=256,delay=d)
            self.addLink(s1, s5,bw=20,max_queue_size=256,delay=d)
            self.addLink(s2, s6,bw=20,max_queue_size=256,delay=d)
            self.addLink(s3, s6,bw=20,max_queue_size=256,delay=d)
            self.addLink(s4, s6,bw=20,max_queue_size=256,delay=d)
            self.addLink(s5, s6,bw=20,max_queue_size=256,delay=d)
            self.addLink(s6, h5,bw=20,max_queue_size=256,delay=d)
            self.addLink(s6, h6,bw=20,max_queue_size=256,delay=d)
            self.addLink(s6, h7,bw=20,max_queue_size=256,delay=d)
            self.addLink(s6, h8,bw=20,max_queue_size=256,delay=d)


def read_topo():
    nb_hosts = 0 
    nb_switches = 0
    links = []
    with open("topo.txt", "r") as f:
        line = f.readline()[:-1]
        w, nb_switches = line.split()
        assert(w == "switches")
        line = f.readline()[:-1]
        w, nb_hosts = line.split()
        assert(w == "hosts")
        for line in f:
            if not f: break
            a, b = line.split()
            links.append( (a, b) )
    return int(nb_hosts), int(nb_switches), links


def main():
    nb_hosts, nb_switches, links = read_topo()

   
    mode = args.mode

    topo = MyTopo(args.behavioral_exe,
                  args.json,
                  nb_hosts, nb_switches, links)

    net = Mininet(topo = topo,
                  host = P4Host,
                  switch = P4Switch,
                  link=TCLink,
                  controller = None )
    net.start()

   

    for n in xrange(nb_hosts):
        h = net.get('h%d' % (n + 1))
        
	for off in ["rx", "tx", "sg"]:
            cmd = "/sbin/ethtool --offload eth0 %s off" % off
            print cmd
            h.cmd(cmd)
        
	print "disable ipv6"
        h.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")
        h.cmd("sysctl -w net.ipv4.tcp_congestion_control=reno")
        h.cmd("iptables -I OUTPUT -p icmp --icmp-type destination-unreachable -j DROP")
	
	if mode == "l2":
            h.setDefaultRoute("dev eth0")
        else:
            h.setARP(sw_addrs[n], sw_macs[n])
	    h.setDefaultRoute("dev eth0 via %s" % sw_addrs[n])

    for n in xrange(nb_hosts):
        h = net.get('h%d' % (n + 1))
	h.describe()

    sleep(1)

    print "Ready !"
   
    
    time.sleep(30)
    num_list=[3,2,1,0]
    h1,h2,h3,h4,h5,h6,h7,h8=net.get('h1','h2','h3','h4','h5','h6','h7','h8')

    #iperf Server
    h5.popen('iperf -s -p 5566', shell=True)
    h5.cmdPrint('arp -s 10.0.0.1 00:00:00:00:00:01')
    h6.popen('iperf -s -p 5567', shell=True)
    h6.cmdPrint('arp -s 10.0.0.2 00:00:00:00:00:02')
    h7.popen('iperf -s -p 5568', shell=True)
    h7.cmdPrint('arp -s 10.0.0.3 00:00:00:00:00:03')
    h8.popen('iperf -s -p 5569', shell=True)
    h8.cmdPrint('arp -s 10.0.0.4 00:00:00:00:00:04')

    def loop(n):
      if n==3 :
          print 'lf4:'
          h4.cmdPrint('arp -s 10.0.0.8 00:00:00:00:00:08')
          #time.sleep(0.002)
          h4.cmdPrint('iperf -c 10.0.0.8 -p 5569 -l 1000000 -n 1 -P 2' ) #long flows
      elif n==2 :
          print 'lf3:'
          h3.cmdPrint('arp -s 10.0.0.7 00:00:00:00:00:07')
          #time.sleep(0.002)
          h3.cmdPrint('iperf -c 10.0.0.7 -p 5568 -l 1000000 -n 1 -P 2' )
      elif n==1 :
          print 'lf2:'
          h2.cmdPrint('arp -s 10.0.0.6 00:00:00:00:00:06')
          #time.sleep(0.002)
          h2.cmdPrint('iperf -c 10.0.0.6 -p 5567 -l 10000 -n 1 -P 12' ) #63%
      elif n==0 :
          print 'lf1:'
          h1.cmdPrint('arp -s 10.0.0.5 00:00:00:00:00:05')
          #time.sleep(0.002)
          h1.cmdPrint('iperf -c 10.0.0.5 -p 5566 -l 100000 -n 1 -P 4' )
    pool = threadpool.ThreadPool(4)
    requests = threadpool.makeRequests(loop,num_list)
    [pool.putRequest(req) for req in requests]
    pool.wait()


    if args.without_pcap == 'y':
        cmd = "sudo rm -rf *.pcap"
        status, output = commands.getstatusoutput(cmd)
        print "\nClean up *.pcap files. Set \"--without-pcap n\" in run.sh to disable this behavior.\n"

    CLI( net )
    net.stop()

    cmd = "sudo ./src/cleanup.sh"
    status, output = commands.getstatusoutput(cmd)
    print "\nClean up the environment.\n"

  
if __name__ == '__main__':
    setLogLevel( 'info' )
    main()

