# QDAPS-Mininet
This is the code of QDAPS which is implemented in mininet.
1. Install P4_16 environment via [https://github.com/p4lang/p4c](https://github.com/p4lang/p4c) and [https://github.com/p4lang/behavioral-model](https://github.com/p4lang/behavioral-model).

2.Set the environment variables in the file 'env.sh' according to the actual path of bmv2 and p4c.

3.Enter to the  `/qdaps` directory. 
`cd qdaps`

4.run the program and then set the flow table. 
`./run_demo.sh`

`./add_entry.sh`

5.run wireshark to capture the packets.
 `sudo wireshark`

6.using `exit` to exit the program and use `sudo mn -c` to clean the mininet configuration files.

7.running `./cleanup.sh` to delete the generated intermediate files.
