from pyephember.pyephember import EphEmber
import argparse
import sys

def main():
    # global params
    parser = argparse.ArgumentParser(prog='example',
                                     description='Example of using pyephember')
    parser.add_argument("--email", type=str,
                        help="Email Address for your account")
    parser.add_argument('--password', type=str,
                        help="Password for your account")
    parser.add_argument('--zone_name', type=str, default="heating",
                        help="Zone Name to check")
    parser.add_argument('--cache_home', type=bool, default=False, 
                        help="use a new HTTP request per api request or cache data between requests")
    args = parser.parse_args()

    try:
        t = EphEmber(args.email, args.password, cache_home=args.cache_home)
    except:
        print("Unable to login")
        return 1

    # Get the full home information
    print(t.getHome())
    print("----------------------------------")
    # Get only zone information
    print(t.getZones())
    print("----------------------------------")
    # Get a zone by name
    print(t.getZone(args.zone_name))
    print("----------------------------------")
    # Get information about a zone
    print(t.getZoneTemperature(args.zone_name))
    print(t.isZoneActive(args.zone_name))

    return 0

if __name__ == '__main__':
    sys.exit(main())


