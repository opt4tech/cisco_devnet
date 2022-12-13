# Review Questions
1. What information must be stored in the routing table?
Destination network and the next hop and interface to send the packet to and out of. That last part is called the destination pointer. Think "go this way"

2. What does it mean when a route table says that an address is variably subnetted?
An address is variably subnetted when it has been subnetting with different prefix lengths. A /24 broken up into /25s and /26s

3. What are discontiguous subnets?
A discontiguous subnet is a classful network that has been subnetted and those subnets are not in the same part of the network but spread out. 

4. What IOS command is used to examine the IPv4 route table?
show ip route

5. What IOS command is used to examine the IPv6 route table?
show ipv6 route

6. What are the two bracketed numbers associated with the nondirectly connected routes in the route table?
[1,0] first number stands for the administrative distance of the protocol used, and the second number is the metric or cost. 

7. When static routes are configured to reference an exist interface instead of a next-hop address, how will the route table be different?
The route table will show those routes as connected interfaces. 

8. What is a summary route? In the context of static routing, how are summary routes useful?
It can help reduce the number of ip route statements needed in the configuration.

9. What is an administrative distance?
That is the priority of the route based on the protocols used. 0 - connected, 1 - static, 20 - bgp

10. What is a floating static route?
A secondary static route configured with a higher administrative distance so that it is only used in the event of a failure.

11. What is the different between equal cost and unequal cost load sharing?
Equal cost will do a 1 for 1 load share across links that have the same cost or are configured with 2 static routes. Unequal cost will load share proportionatley to the different costs of the routes.

12. How does the switching mode at an interface affect load sharing?
Certain switching frameworks support per packet or per destination load sharing.

13. What is a recursive table lookup?
When a route points to a next hop address that also needs to be looked up. 
