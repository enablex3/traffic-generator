### TRAFFIC GENERATOR ###
###    VERSION 1.0    ###

###     APPENDIX A    ###
SUMMARY:
The TrafficGenerator will generate regular traffic throughout your network or public domains. The user
may select up to 5 targets and 5 ports (as of right now). Please review Appendix B for the instructions.

DISCLOSURE:
This software has been developed for educational purposes only. Please refrain from attempting any
DOS or DDOS attacks on public domains or any other domain that is unauthorized. We are not responsible
if the FBI shows up at your doorstep, puts you into a straitjacket, and charges you with heavy fines or
even jail time.

###     APPENDIX B    ###
INSTRUCTIONS:
note => the stdout display will report any verbose output or errors.
note => 'STOP' button required if you need to stop DOS or DDOS attacks.
note => ensure SSH enabled for your bots if you choose DDOS.
note => ensure Python is installed on your botnet bots for DDOS.
note => so far, only Linux distributions work with DDOS.
note => authentication failures will remove bots from the DDOS attack, but will remain in the botnet.txt 
        file.

- Regular Traffic
  1) Select transmission type
  2) Type recieve buffer size (no more than 64KB)
  3) Enter your target ipv4 addresses or public domain (e.g, www.google.com) - no more than 5
  4) Enter your target port numbers (e.g, for ssh, port 22) - no more than 5
  5) Select 'NONE' for DOS
  6) Press 'Start' - will save and validate your entered data
  7) When ready, press 'GO' - will generate traffic

- Single DOS
  1) Do all steps as in Regular Traffic up until step 5
  2) Select 'SINGLE' for DOS
  3) Press 'Start'
  4) When ready, press 'GO'
  5) If desired, press 'STOP' - will stop the DOS attack from localhost

- Distributed DOS
  1) Ensure you have entered bot info in botnet.txt
     a) File located at: C:\Users\<username>\Documents\TrafficGenerator\
     b) File format in Appendix C
  2) Select 'Yes' or 'No' for 'Include Localhost?' - will add localhost to botnet
  3) Do all steps as in Single DOS

###      APPENDIX C    ###
BOTNET FILE FORMAT
<host_ipv4_addr or domain>, <username>, <password>

Example:

192.168.120.126, root, toor
192.168.120.129, superadmin, admin321
osboxes.priv.domain, jane, jane_is_a_hacker!

###     APPENDIX D    ###
DEALING WITH ERRORS:
- Make sure files located at: C:\Users\<username>\Documents\TrafficGenerator\
  are not tampered with, unless editing your botnet.txt file

- Make sure botnet username and password are correct - the software will tell you if there
  are any authentication failures

- For DDOS, if the software reports "Process has not been terminated on bot: <bot>" then log 
  onto the bot and do:
   1) "ps -ef | grep bot_dos.py" - this is the script that is generated and copied onto your bot
   2) choose the leftmost/larger integer value as your pid
   3) "kill -9 <chosen_pid>"