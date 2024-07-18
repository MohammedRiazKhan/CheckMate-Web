Project Documentation - CheckMate

EC2/RDS Network Diagnostic Tool

Consumer

AWS Community on Forums

Problem statement

One of the most occurring support cases/forum posts in the EC2 Linux/Windows and Database profiles are issues which involve the customer not being able to connect via SSH/RDP into their EC2 Linux/Windows instances or access their RDS instance from a client for that particular Database Engine.  Associates/Engineers then troubleshoot these common issues with the use of networking tools which are usually because of common misconfigurations (blocked ports, incorrect security groups, not in a public subnet etc.). This troubleshooting process can be sped up by automating certain checks done with the use of a software tool. When launching and configuring EC2/RDS instances there could be factors that result in the customer being unable to connect, for instance the incorrect security group policies being applied, Network Access Control lists blocking connectivity, the subnet which the instance was provisioned is a private subnet instead of a public one, the port(s) are being blocked from accessing the instance not having a Public or Elastic IP or the instance could be failing altogether,  or endpoint not resolving with it unable to make a connection to it at all. 

How to solve problem

Our recommendation is to develop a tool written in Python which will perform a sanity check to rule out common errors which may occur by performing the checks for the customer (ping, traceroute, telnet and nslookup). This tool will be integrated with the forum for the customer’s use before opening a forum post and therefore it will be public facing and available to use. 

Type of Application

It will be a downloadable desktop program since it will allow easier access to the system and its utilities (such as ping, telnet etc) in order to perform these networking checks. 

A web application would require the libraries to be integrated into the forum as well, which is not ideal

Alternatives and their limitations
Microservices as a backend hosted on an EC2 instance or Elastic Bean Stalk instance, however for this particular tool it wont benefit from being developed in such a way as the application needs to run from the local machine to the instance being tested since certain tests are there to verify if the local machine could be the problem when not being able to connect.

A web application would require the libraries to be integrated into the forum as well, this would require the application to be written as a web applications and will have similar limitations to the Microservice approach.

Supported Operating Systems

Windows, Linux & MacOS

Features

EC2

* Check if the instance can be accessed over SSH/RDP (Port 22/3389), by checking whether the ports are open on the instance
* Programmatically with the AWS CLI/SDK check the Security of the instance which is attached to it, to verify if its allowing incoming traffic on the port specified by the user i.e ssh on port 22
* Programmatically with the AWS CLI/SDK check whether the access control list is allowing traffic.
* Programmatically with the AWS CLI/SDK check if instance is in the correct subnet, by checking if the subnet has an Internet Gateway on it and in the same VPC.
* Check connectivity between client and hosts, by performing a ping and/or connect via ssh to test the connection (will require private key).
* Check whether incoming/outgoing traffic is blocked via tracert/traceroute.
* Intelligently suggest general solutions to these common checks to the user.
* Run various networking tools such as ping, traceroute, nslookup and telnet to perform networking troubleshooting.

RDS

* Perform a telnet on the specific engines port (3306, 1521, 1433, 5432) to check if the port is open and allowing any connections to it 
* nslookup to check if the IP can be resolved from the endpoint (observed that ICMP packets cannot be sent regardless of Security Group settings)

Scope

Phase 1
Phase 1 will include the following features for the first version and will be implemented using the appropriate networking tools and not programmatically:

* Check the instance’s connectivity (reachable/up or not) using ping (if ICMP incoming is enabled in security group: EC2), if there is a response (Replies for as many packets sent) from the destination host this will verify networking connectivity.
* Perform a telnet on an IP/Endpoint as well as a port supplied by the user to check if the host is firstly reachable and whether the port given is open on the destination host.
* Perform a traceroute/tracert on an IP/Endpoint supplied by the user. In order to determine if there are any issues in connecting to the AWS network, 3 things will be looked at if the host’s packet leave their own network (failure to connect may be due to their local firewall), whether the packet can successfully pass through the internet and whether the packet reaches the AWS network (Security Group).
* Do an DNS name resolution to verify if the endpoint resolves correctly to an IP address. This test will serve to test whether the host name can be successfully resolved to an IP and verify that DNS is working on the host, for phase 1 the option of specifying record types will be left out. For the purposes of the test, it will only verify if it can resolve.


Testing:

Ping

Errors

1. Destination Host Unreachable: This error indicates that a route to the destination node cannot be found.

1.  Request Timed Out: The destination IP or Host Name is not responding to the ping request.

1.  Unknown Host: IP Address or the Host Name does not exist in the network or the destination host name cannot be resolved.


Cause

1. Destination Host Unreachable: The security group is not configured to accept incoming ICMP packets and therefore it can not reach the destination endpoint.

1. Request Timed Out: This error indicates that your host did not receive ICMP Echo Reply back from the destination node within the designated time period. The local firewall on the users computer is blocking the request. Another reason why a error timed out value may appear is because of a route from the destination that could not be found.

1. Unknow Host: IP Address or the Host Name does not exist in the network or the destination host name cannot be resolved.


Fix

1. Destination Host Unreachable: Configure security group to allow ICMP packets for the specified instance.

1. Request Timed Out: First test ping with loopback address and see if you are getting a proper reply from that address. If you are not getting a proper reply than disable the firewall and repeat the process.

1. Unknown Host: Verify the name and availability of the DNS server.


Traceroute

Errors

1. Request Timed out: The response did not return in the specified time.

Causes

1. Request Timed Out: The response did not return in the allocated time which is often related to a packet that can't exit the users local network. A firewall might be configured at the user's local.

Fix

1. Request Timed Out: Check firewall of local network and the security group that is configured for your VPC to allow ICMP packets.

nslookup

Possible errors:

i. Domain name non existent: Domain name cannot be resolved to an IP

Causes:

i. This usually occurs when the domain name exists, possible causes is an incorrect CNAME (in the case of this tool as of phase 1, it only accepts EC2 and RDS endpoints not domain names)

Fix:

i. Check DNS records to ensure it is pointing to a valid record

telnet

Possible errors:

i. Can’t connect due to connection refused

Causes:

i. This error usually occurs when the port is not allowing traffic into the host, or from the source IP

Fix:

i. Modify security group/firewall to ensure traffic is being allowed on that port and the instance is listening on that port i.e webserver on 80, ssh on 22 for the IP.


Unit Testing

Test Case Description and Expected outcome, for each unit of code (functions)

1. Ping Test

Description

Test whether the Ping function is working correctly by simulating a ping request made from a source (Local or Remote) to a remote host (IP or Endpoint) and correctly parse the information to produce a suggestion as to what to try when troubleshooting.

Inputs

Source IP: 

* Default=127.0.0.1 when none is specified
* Local to Remote=127.0.0.1 or public IP

Destination IP:

* Required as IP or Endpoint

Process

Take SIP and DIP, perform a ping with 4 requests and replies
Parse responses stores inside of array, iterate and check the output

Output

Display a pass if the test is successful
If unsuccessful give suggestion as to what could be wrong based on the result (unreachable or timing out)

Pass Criteria

Replies == 4 will be considered a pass
Replies == 3 will be issue a retest to check if the packet is lost again (sometimes one packet is lost)

2. Telnet Test

Description

This test will verify if the port is open, by simulating a request to test a port from the local machine for a specific port.
 
Inputs

Source IP: by default will be the IP of the localhost (127.0.0.1/Their Public IP) 

Destination IP: Required, this is the host to check can be endpoint or IP

Port: the required port to check if open i.e 22, 3389 or 80 etc.

Process

Get the SIP from the system, DIP as input and port number as Input perform the telnet, parse the reply and match it to common responses to determine whether its  open. Based on the response generate an output .

Output

Pass or Fail with suggestions

Pass Criteria

Port open will return a specific result for that protocol, if the appropriate result is returned it will pass else fail.

3. Nslookup Test

Description

This test will simulate a simple dns resolution test by getting the domain name to test and see whether an ip is returned. if an ip is returned it will be a success.

Inputs

Destination Endpoint of host to check whether it resolves

Process

Accepts the Destination’s endpoint(domain name) as an input
Perform DNSlookup
Parse the result to get the IP(s) returned

Output

Success/Pass if the endpoint can be resolved to an IP

Pass Criteria

Endpoint resolves to an IP it will be considered a pass.

4. Traceroute Test

Description

This test will simulate a traceroute request from the users local machine to an EC2/RDS instance, which will then tell 3 things:

1. If the packets can leave the users home network (firewall on their machine)
2. If it reaches the internet
3. If it can reach the AWSnetwork


Inputs:

SIP default = 127.0.0.1/Public IP
Take the destination IP to test

Process:

Take the endpoint/ip of host to test, perform a telnet and parse the output to see if it was successful

Output:

Results of the traceroute, the interpretation of the output and the pass/fail

Pass Criteria:

if the traceroute manages to make it to the AWS network it is a pass
If it cannot, determine where it failed and give a suggestion as to why

4. Determine instance

Description

This test will validate whether the instance type can be determined based on the endpoint given, if ip is passed in the ip should be reverse resolved to get the endpoint (in case of EC2)

Inputs:

The endpoint/i[

Process:

Parse the endpoint and determine if it contains Ec2 or RDS in its endpoint.
When an IP is supplied get the endpoint (in case of EC2)

Output:

Based on the which type of instance it is (EC2 or RDS) a limited testing is performed for RDS than Ec2 since ICMP isnt allowed for RDS

Pass Criteria:

Return EC2 or RDS when its found



























