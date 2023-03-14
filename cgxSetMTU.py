import cloudgenix
import logging
from pprint import pprint
import sys
import argparse
import cloudgenix_settings


# init log
cloudgenix.api_logger.setLevel(logging.WARN)
logging.basicConfig(level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARN)
logging.getLogger("urllib3").setLevel(logging.WARN)
log = logging.getLogger("cgxSetMTU")

# init cloudgenix sdk
sdk = cloudgenix.API()
res = sdk.interactive.use_token(cloudgenix_settings.CLOUDGENIX_AUTH_TOKEN)
if not res:
    log.error("Auth token invalid")
    sys.exit()

def get_args():
    parser = argparse.ArgumentParser(description="Set MTU across sites")
    parser.add_argument("--interface", "-I", default="2", action="store", help="interface to check. Default is '2'")
    parser.add_argument("--list", "-L", default=False, action="store_true", help="list elements sites")
    parser.add_argument("--mtu", "-M", default=1500, type=int, help="set the MTU to this value. Defautl is 1500")
    parser.add_argument("--elements", "-E", default=False, action='store', type=argparse.FileType('r'), help='a list of elements, one element per line. # to comment out')

    return parser.parse_args()
if __name__ == "__main__":
    # get args
    args = get_args()

    if args.list:
        for element in sdk.get.elements().cgx_content['items']:
            print(element['name'])
    elif args.elements:
        # create name to element dict
        name2element = {}
        for element in sdk.get.elements().cgx_content['items']:
            name2element[element['name']] = element

        # go over element list, skip that start with # and update interface 
        for line in args.elements.readlines():
            #remove leading and traling spaces and new lines
            element_name=line.strip()

            # skip commented lines
            if element_name[0] == "#":
                continue
            
            element = name2element[element_name]
            log.info(f"Working on {element_name}")

            # find interface
            for interface in sdk.get.interfaces(element['site_id'], element['id']).cgx_content['items']:
                if args.interface == interface['name']:
                    #update MTU
                    interface['mtu'] = args.mtu
                    res = sdk.put.interfaces(element['site_id'],element['id'],interface['id'],interface) 
                    if not res:
                        log.error("-- Interface update failed. Aborting")
                        cloudgenix.jd_detailed(res)
                        sys.exit()
                    log.info(f"-- Interface {args.interface} was set to MTU {args.mtu}")
                    break
            else:
                log.warn(f"-- Interface {args.interface} not found")
            

    else:
        log.error("--elements is missing. See -h for help")


