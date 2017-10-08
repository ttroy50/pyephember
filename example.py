from pyephember.pyephember import EphEmber
import argparse
import sys
import getpass
import json

def main():
    # global params
    parser = argparse.ArgumentParser(prog='example',
                                     description='Example of using pyephember')
    parser.add_argument("--email", type=str,
                        help="Email Address for your account")
    parser.add_argument('--password', type=str, default="",
                        help="Password for your account")
    parser.add_argument('--zone_name', type=str, default="heating",
                        help="Zone Name to check")
    parser.add_argument('--cache_home', type=bool, default=False, 
                        help="use a new HTTP request per api request or cache data between requests")
    args = parser.parse_args()

    password = args.password
    if password is None or password == "":
        try:
            password = getpass.getpass()
        except:
            print "Unable to get password"

    try:
        t = EphEmber(args.email, password, cache_home=args.cache_home)
    except:
        print("Unable to login")
        return 1

    # Get the full home information
    print(json.dumps(t.get_home(), indent=4, sort_keys=True))
    print("----------------------------------")
    # Get only zone information
    print(json.dumps(t.get_zones(), indent=4, sort_keys=True))
    print("----------------------------------")
    # Get a zone by name
    print(json.dumps(t.get_zone(args.zone_name), indent=4, sort_keys=True))
    print("----------------------------------")
    # Get information about a zone
    print("{} current temperature is {}".format(args.zone_name, t.get_zone_temperature(args.zone_name)))
    print("{} active : {}".format(args.zone_name, t.is_zone_active(args.zone_name)))

    return 0

if __name__ == '__main__':
    sys.exit(main())


