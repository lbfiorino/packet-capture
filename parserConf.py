import configparser

capture = configparser.ConfigParser()
capture.read("capture.ini")


traffic_type='normal'
for t in capture['target']:
    target_ip = capture['target'][t]
    for h in capture[traffic_type]:
        host_ip = capture[traffic_type][h]
        pcapfile = host_ip+"_"+traffic_type+".pcap"
        print("tcpdump -U -ni enp0s3 -w "+pcapfile+" 'host "+target_ip+" and (src "+host_ip+" or dst "+host_ip+"' 2> /dev/null")

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


