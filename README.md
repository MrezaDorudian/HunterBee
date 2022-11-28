<p align="center">
  <img src="https://github.com/MrezaDorudian/HunterBee/blob/main/Logo.png" />
</p>  

### My B.Sc. final project on the field of cyber-security and Threat Hunting using Machine Learning approaches.  
---
# Description
This project is a **highly configurable** threat-hunting system, which helps security experts and threat-hunters easily gather, manage, and use **logs** effectively. It works on both system and network logs.  
There are two seperate programs.  
+ First one should be deployed on clients, and it gathers logs, filter the important data, and send the remaining to the central server for further analysis.
+ Second program should be deployed on the central server to receive client logs, process them, and inform the user if needed.  

## Phase 1 - Gathering Logs from clients
+ ### system logs  
These kinds of logs can be gathered by Sysmon, Windows Event Logs, and etc. We specifically use Sysmon to gather them.
+ ### network logs  
These logs can be gathered by Wireshark, Snort, Suricata, etc. We use Wireshark to gather them.  
after gathering logs, we compile them and as they reach a certain volume we send them to a central server.
  

## Phase 2 - Processing Logs in server
Using machine learning techniques such as clustering, we manage to reduce the log volume significantly. At this level the remaining logs can be checked and analyzed by a human expert, and complete the threat-hunting process as he/she wishes.

---

# Resources
Sources about threat hunting and network security consist of papers, open source projects,
YouTube videos etc. that can be found on this [GitHub repository](https://github.com/MrezaDorudian/ThreatHunting)

# Contribution
Feel free to contribute to this project, i'd be glad.
