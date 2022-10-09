This project is my B.Sc. final project on the field of network security and specifically Threat Hunting.
![Logo](https://github.com/MrezaDorudian/HunterBee/Logo.png)



First I gatered information about threat hunting and network security, consist of papers, open source projects,
YouTube videos etc. that can be found on this [GitHub repository](https://github.com/MrezaDorudian/ThreatHunting)

Then me and my supervisor decided to create a project that can be used to hunt for threats in the network using logs.  
our logs can be classified as:
+ system logs  
these kinds of logs can be gathered by Sysmon, Windows Event Logs, etc. We specifically use Sysmon to gather them.
+ network logs  
these logs can be gathered by Wireshark, Snort, Suricata, etc. We specifically use Wireshark to gather them.

after gathering the logs, we save them in a database, so we can use them for analysis.
