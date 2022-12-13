1. What is a routing protocol?
A routing protocol is a set of software instructions and capabilities that allow routers in a network to share network information, compute the best paths to those network destinations, and automatically adjust to topology changes in the network. 

2. What basic procedures should a routing algorithm define?
    - a procedure for passing reachability information to neighbors
    - a procedure for receiving reachability information from neighboring routers
    - a procedure for calculating best path to destination networks and recording that information in the route table.
    - a procedure for reacting to topology changes in the network

3. Why do routing protocols use metrics?
To calculate which is the optimal path to a network. Path determination. 

4. What is convergence time?
The amount of time it takes for each routing table to be finish calculating best paths and to be "stable"

5. What is load balancing? Name 4 different types of load balancing?
Load balancing is leverage two paths simulataneously to send traffic to a single destination. Allows for sharing the load. 4 types include: per-packet, per-destination, equal cost, and unequal cost.

6. What is a distance vector routing protocol?
A routing protocol that does not have a complete view of the network but has to determine best path based on the information given to it by neighboring routers, typically based on hop count or a metric of some sort. Also called routing by rumor or equivelant to simply following road signs to where you want to go. 

7. Name several problems associated with distance vector protocols?
Distance vector protocols tend to be slower to converge. Rely on information from neighbors for best path calculation so they are susceptible to disinformation. Have to deal with routing loop issues and therefore need to implement more loop prevention mechanisms such as split horizon.

8. What are neighbors?
Two routers who have established a protocol for interacting with each other to exchange routing information and to track the status of each other.

9. What is the purpose of route invalidation timers?
This is the timer interval when a route becomes invalid if neighboring routers haven't refreshed the route within this time period. 

10. Explain the difference between split horizon and split horizon with poisoned reverse.
Split horizon says that routes will not be shared back out the same interface that it just learned them on. Split horizon with poison reverse will share the routes back out that same interface but with a poisened metric. Bad news is better then good news. The poisoned metric will ensure that if the better route goes away that the routers won't inadvertently cause a routing loop by sharing information back to the source in the event of a failure. 

11. What is the counting to infinity problem?
When a distance vector route shares a route with a neihboring router, the neighboring router will take the route and had its hop count or metric on top before forwarding to the next neighbor. Counting to infinity happens when you have routers in some sort of ring that keep sharing that route which each other around the ring, always adding the metric on top. In converged, stable network this problem does not when the route is actually reachable at a lower metric by one of the routers. However, if that link with the route fails, the router that was sharing that information will see another "route" around the ring to that same destination and "think" that is now the best path. It will take that route and start sharing it with its other neighbors. They will then keep sharing and sharing, increasing the hop count until "infinity" is reached. Either causing the routers to crash or by reaching some arbitrary number that infinity represents. The most common is 16 hops.

12. What are holddown timers, and how do they work?
If a router learns that a metric to destination network has just increased it will set a timer for that network and will not accept any new information regarding that route until the timer has been reached. This prevents bad routing information from being shared to quickly and for the right information to be shared within that time period. 

13. What are the differences between distance vector and link state routing protocols?
Distance vector choses the best exit path from the router to a neighboring routers based on information they shared with the router. It has no view of the network beyond its immediate neighbors and the metrics they have added to the routes. Link state on the other hand, will build a topology database view of the entire network to which it is a part of and will then compute the best paths towards destination networks using the SPF algorithm. It's not just trusting the information provided by neighbors, but looking at the whole map. 

Distance vector does updates to broadcast addresses it does not establish neighor connections. Link state does. 

14. What is the purpose of a topilogical database?
A view of every route on the network and every path to that route. It is used to calculate the best path to each route from each router. 

15. Explain the basic steps involved in converging a link state network?
First each router needs to establish neighbor relationships with their neighboring routers. Next they need to share all router link-state advertisements with each other and then share all stub-network link statement advertisements with each other. They build the topology database and add the best paths to each router link and stub network in the route table as it builds the database until no new link state advertisements are received.

16. Why are sequence numbers important in link state protocols?
Each route has a sequence number which tells the router whether a route has new information in it. 

17. What purpose does aging serve in a link state protocols?
Each route has an age that is incremented on each router as it is shared to ensure that every router knows it has the latest information, and it also serves to know when a route is stale and no longer reachable on the network. If a router hasn't refreshed the LSA for a route before the MaxAge has been reached then each router will share the route with the max age set and flush them out of the database. 

18. Explain how an SPF algorithm works.
The spf algorithm works by creating three branches of the topology database. The tree database, the candidate database, and the link state database. First it adds itself to the tree database with a cost of 0. Next it takes all router link triples (Router ID, Neighbor ID, Cost) and starts moving them to the candidate database. The cost from the root is calculated to each link and the lowest cost is moved to the tree database and the higher cost paths are removed from the candidate database and remain in the link state database. Essentially every time it moves a route from candidate to the tree it looks at the neighbor ID that was just moved to the tree and adds all other routes with that neighbor ID as the Router ID to the candidate list to be examined and costs to be calculated. It repeats this until the tree database is completed. 

19. How do areas benefit a link state network?
Create sub-networks in order to reduce the size of the link state database to help make each router more effiecient and faster. 

20. What is an autonomous system?
An autonomous system is an adminstrative routing domain and a process domain that either separates IGP process from other IGP process or routing domains that EGPs route between.

21. What is the difference between an IGP and an EGP?
An IGP is an interior gateway protocol that routes within an autonomous system and an EGP routes between autonomous systems. 