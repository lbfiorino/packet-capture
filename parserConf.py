import configparser

capture = configparser.ConfigParser()
capture.read("capture.ini")


def start_capture(section):
    for t in capture['target']:
        target_ip_port = capture['target'][t].split(':')
        for h in capture[section]:
            host_ip = capture[section][h]
            pcapfile = host_ip+"_>_"+target_ip_port[0]+"_"+traffic_type+".pcap"
            CMD = "tcpdump -U -n -i enp0s3 -w "+pcapfile+" 'host "+target_ip_port[0]+" and host "+host_ip
            if (len(target_ip_port) == 2): 
                CMD += " and tcp port "+target_ip_port[1]+")' 2> /dev/null"
            else:
                CMD += "' 2> /dev/null"
        
            print(CMD)


traffic_type = "normal"
if (traffic_type == "all"):
    start_capture("attack")
    start_capture("normal")
else:
    start_capture(traffic_type)



# for t in capture['target']:
#     target_ip_port = capture['target'][t].split(':')
#     for h in capture[traffic_type]:
#         host_ip = capture[traffic_type][h]
#         pcapfile = host_ip+"_"+traffic_type+".pcap"
#         CMD = "tcpdump -U -n -i enp0s3 -w "+pcapfile+" 'host "+target_ip_port[0]+" and host "+host_ip
#         if (len(target_ip_port) == 2): 
#             CMD += " tcp port "+target_ip_port[1]+")' 2> /dev/null"
#         else:
#             CMD += "' 2> /dev/null"
    
#         print(CMD)

# for sect in capture.sections():
#     print("\nSection: ",sect)
#     for k,v in capture.items(sect):
#         print("Key: ",k," Value: ",v)


# print('\nTARGET')
# for k,v in capture.items('TARGET'):
#     print(k,v)

# print('\nATTACK')
# for k,v in capture.items('ATTACK'):
#     print(k,v)

# print('\nNORMAL')
# for k,v in capture.items('NORMAL'):
#     print(k,v)


