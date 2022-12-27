<p align="center">
  <img src="https://github.com/MrezaDorudian/HunterBee/blob/main/Logo.png" />
</p>  

### My B.Sc. final project on the field of cyber-security and Threat Hunting using Machine Learning approaches.  
---
# Description
This project is a highly configurable threat-hunting system that helps security experts and threat hunters gather, manage, and use logs effectively in order to detect and mitigate potential threats. The system works on both system and network logs and consists of two separate programs: one that is deployed on clients to gather logs and filter important data, and another that is deployed on a central server to receive client logs, process them using machine learning techniques, and inform the user if necessary.

## Phase 1 - Gathering Logs from clients
The client-side program is responsible for gathering system and network logs. System logs can be gathered using tools such as Sysmon and Windows Event Logs, and network logs can be gathered using tools such as Wireshark, Snort, and Suricata. Once the logs are gathered, they are compiled and sent to the central server when they reach a certain volume.
  

## Phase 2 - Processing Logs in server
The server-side program receives the logs from the clients and uses machine learning techniques, such as clustering, to significantly reduce the volume of logs. The remaining logs can then be checked and analyzed by a human expert to complete the threat-hunting process.

---

# Resources
[This repository](https://github.com/MrezaDorudian/ThreatHunting) includes a collection of resources on threat hunting and network security, including papers, open source projects, and YouTube videos. These resources can be found in the repository and may be useful for those interested in learning more about threat hunting and staying up-to-date on the latest techniques and tools. 

# Contribution
If you would like to contribute to this project, we welcome your contributions and would be glad to have your help. Please feel free to fork the repository and submit pull requests with any changes or additions that you think would be beneficial to the project.

Thank you for considering contributing to our threat-hunting system!
