### What are the five layers of the TCP/IP protocol suite? What is the purpose of each layer?
|-----Application-----| *protocols that specify how user based services will provide access over the netowrk*
|------Transport------| *Protocols that specify how to encapsulate datagrams accross the underlying network, either connection or connectionless. Specified the protocls that control the internet layer*
|------Internet-------| *Protocols that specific how to deliver and route packets from one destination to another across logical network paths*
|------Data Link------| *Protocols that control the physical layer, how it is accessed and shared, how devices on that medium are identified, and how data is framed before being trasnmitted*
|------Physical-------| *Protocols that specify how 1s and 0s are transmited over a physical medium over which TCP/IP will be communicating*

### What is the most common version of IP version presently being used?
IPv4

### What is fragmentation? What fields of the IP header are used for fragmentation?
Fragmentation is what happens to a packet that is larger then the maximum transmission unit size for a router or interface to process or transmit. The flags fields with the DF - don't fragment bit, MF - more fragments bit, and Fragment offset field to indicate where to put the packet back together again.

### What is the purpose of the TTL field in the IP header? How does the TTL process work?
TTL stands for time to live and was suposed to indicate in seconds how old a packet was. Whan the packet TTL expires, gets to 0, then the packet will be dropped. Effectively the TTL becomes more of a hop count. Every router that a packet passes through will decrement the TTL header. The last router to decrement to zero drops the packer and sends an ICMP time to leave exceeded back to the client. 

### What is the first octet rule?
The first octet rule tells you what class of IP address a subnet is a part of. Take the first bits of the address as follows:
01 = Class A
10 = Class B
110 = Class C

### How are Class A, B, and C IP addresses recognized in dotted decimal? How are they recognized in binary?
Dottet decimal shows addresses in 4 groups of numbers ranging from 0-255 separated by dots. A machine must convert that to binary in order to process it. Dotted decimals are for humans.
Binary is shows in a 32 bit string of 1's and 0's. 

### What is the address mask, and how does it work?
The address mask tells what bits in an ip address are part of the network address and what bits are a part of the host address. It works by taking the ip address in binary and doing a bit AND operations with its subnet mask to get the network address. 

### What is a subnet? Why are subnets used in IP environments?
A subnet is when you borrow bits from the host address portion to create additional network address within that larger network. They are used to make more efficient used of ip address. 

### Why can't a subnet of all zeros or all ones be used in a classful routing environment?
Since the bit AND operations with address mask needs 1's somewhere in the address to determine where the host address begins and ends this would fail with all zeros and also with all 1's. No division would be mathematically possible. 

### What is ARP?
Address resolution protocol by a machine to find the mac address of the device on the local network from an ip address. It does this by sending an arp request where the source mac and source IP and target IP are correct and known but the target mac is set to all 0's. 

### What is proxy arp?
Proxy arp is a service that a router can provide by responding to local machines' arp requests when the arp request is for a host off network that the router knows about. 

### What is a redirect?
A redirect occurs when a client machine sends a packet to a gateway router in a network where there are two potential routers to exit the network from and that router detected that it's peer router knows the destination network that the machine wants to get to. That router will then forward the packet to the other router and send a redirect message back to the client to let them know that the other router is the bettre path in the future. 

### What is the essential difference between TCP and UDP?
TCP provides connection based transport and udp provides connectionless.

### What mechanisms does TCP use to provide connection-oriented service?
It uses:
- sequence numbers to keep packets in order and reliably delivered.
- acknowledgements, checksums and timers to ensure packets were actually received and were error free. 
- windowing to control how much date the receiving machine can process. 

### Instead of ARP, Novell NetWare uses a network address that includes a device's MAC address as the host portion. Why can't IP do this?
Because ARP address are 48bits and ip addresses are 32 bit.

### What purpose does UDP serve by providing a connectionless service on top of what already is a connectionaless service?
Faster and lighter weight applications that need speed more then reliable service.