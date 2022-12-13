1. First octet rule. Class D addresses are for multicast and the first four bits are 1110. What is the decimal range?
    224.0.0.0 - 239.255.255.255
2. Select a subnet mask for 10.0.0.0 so that there will be at least 16,000 subnets with at least 700 host addresses available on each subnet.
    255.255.252.0
    Select a subnet mask for 172.27.0.0 so that there are at least 500 subnets with at least 100 hosts. 
    255.255.255.128
3. How many subnets are available if a Class C address has six bits of subnetting. How many hosts? 
    2^6 = 64
    2^2 - 2 = 2 address
    Good for point to point links
4. Use a 28-bit mask to derive the available subnets of 192.168.147.0.Derive the available hos address of each subnet
    IP addres = 192.168.147.0
    /28 = 255.255.255.240 
    number of subnets = 2^4 or 16
    number of hosts per subnet = 2^4 -2 or 14
    host addresses available:
        192.168.147.1 - .14
        192.168.147.17 - .30
        192.168.147.33 - .46
        192.168.147.49 - .62
        192.168.147.65 - .78
        192.168.147.81 - .94
        192.168.147.97 - .110
        192.168.147.113 - .126
        192.168.147.129 - .142
        192.168.147.145 - .158
        192.168.147.161 - .174
        192.168.147.177 - .190
        192.168.147.193 - .206
        192.168.147.209 - .222
        192.168.147.225 - .238
        192.168.147.241 - .254
5. Use a 29-bit mask to derive the available subnets of 192.168.147.0
    /29 = 255.255.255.248
    number of subnets = 2^5 or 32
    number of hosts = 2^3 -2 or 6 address
    first 2 and last 2 available address:
        192.168.147.1 - .6
        192.168.147.9 - .14
        ...
        192.168.147.241 - 246
        192.168.147.249 - .254
6. Use a 20-bit mask to derive the available subnets of 172.16.0.0.
    /20 = 255.255.240.0
    number of subnets = 2^4 or 16 subnets
    number of hosts = 2^12 - 2 or 4096
    first 2 available addresses:
        172.16.0.1 - 172.16.15.254
        172.16.16.1 - 172.16.31.254
