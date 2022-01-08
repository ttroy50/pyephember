"""
Example script for PyEphEmber to dump various information from the API,
get the current temperature, and change the target temperature for a zone
"""
import argparse
import getpass
import json
import time

from pyephember.pyephember import EphEmber

# global params
parser = argparse.ArgumentParser(prog='example',
                                 description='Example of using pyephember')
parser.add_argument("--email", type=str, required=True,
                    help="Email Address for your account")
parser.add_argument('--password', type=str, default="",
                    help="Password for your account")
parser.add_argument('--zone-name', type=str, default="heating",
                    help="Zone name to check")
parser.add_argument(
    '--cache-home', type=bool, default=False,
    help="cache data between API requests"
)
parser.add_argument('--target', type=float,
                    help="Set new target temperature for the named Zone")
parser.add_argument('--advance', type=str, choices=("on","off"),
                    help="Set advance state for named Zone")
args = parser.parse_args()

password = args.password
if not password:
    password = getpass.getpass()

t = EphEmber(args.email, password, cache_home=args.cache_home)

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
print("{} current temperature is {}".format(
    args.zone_name, t.get_zone_temperature(args.zone_name)
))
print("{} target temperature is {}".format(
    args.zone_name, t.get_zone_target_temperature(args.zone_name)
))
print("{} active : {}".format(
    args.zone_name, t.is_zone_active(args.zone_name)
))
print("{} mode : {}".format(
    args.zone_name, t.get_zone_mode(args.zone_name).name
))

target = args.target
if target is not None:
    assert 0 <= target <= 25.5
    t.set_zone_target_temperature(args.zone_name, target)
    time.sleep(1)
    print("{} target temperature changed to {}".format(
        args.zone_name, t.get_zone_target_temperature(args.zone_name)
    ))

if args.advance is not None:
    print("Setting advance for {} to {}".format(args.zone_name, args.advance))
    if args.advance == 'on':
        t.set_zone_advance(args.zone_name, True)
    elif args.advance == 'off':
        t.set_zone_advance(args.zone_name, False)
