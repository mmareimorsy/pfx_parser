#!/usr/bin/python3
import json
import sys
from mrtparse import *
from pprint import pprint
import argparse

parser = argparse.ArgumentParser(description="Inet prefix parser", usage="--help to list available commands")
parser.add_argument("-m","--mrt_file", type=str, required=True, help="MRT file to parse")
parser.add_argument("-a","--all_paths", action='store_const', const=True, help="save all paths instead of best path only")
args = parser.parse_args()

v4_rib_json = open("ipv4_rib.json","w")
v6_rib_json = open("ipv6_rib.json","w")
if args.all_paths == True:
    best_path_only = False
else:
    best_path_only = True

# return as_path, origin & MED
# default MED is set to 100 if not existing, always-compare-med behaviour
def extract_path_attrs_keys(attrs):
    res = [0, 0, 100]
    for attr in attrs:
        if attr['type'] == {1: 'ORIGIN'}:
            res[1] = list(attr.get('value', None).keys())[0]
        elif attr['type'] == {2: 'AS_PATH'}:
            res[0] = attr.get('value', None)[0]['length'] 
        elif attr['type'] == {4: 'MULTI_EXIT_DISC'}:
            res[2] = attr.get('value', 100)
    return res 

# best_path_selection gets the best BGP path from given paths 
# paths is an ordered_dict extracted from mrt_parser data rib_entries
# selection based on the following:
# local_pref & originate are skipped intentionally 
# shortest AS_path 
# origin code IGP, EGP, INCOMPLETE
# lowest MED
# rest of attributes are ignored for selection intentionally  
def best_path_selection(paths):
    best_path = None
    for path in paths:
        curr_as_path_len, curr_origin, curr_med = extract_path_attrs_keys(path['path_attributes'])
        if best_path is None:
            best_path = path['path_attributes']
            best_as_path_len, best_origin, best_med = curr_as_path_len, curr_origin, curr_med
        else:
            if curr_as_path_len < best_as_path_len:
                best_as_path_len, best_origin, best_med = curr_as_path_len, curr_origin, curr_med
                best_path = path['path_attributes']
            elif curr_as_path_len == best_as_path_len:
                if curr_origin < best_origin:
                    best_as_path_len, best_origin, best_med = curr_as_path_len, curr_origin, curr_med
                    best_path = path['path_attributes']
                elif curr_med < best_med:
                    best_as_path_len, best_origin, best_med = curr_as_path_len, curr_origin, curr_med        
                    best_path = path['path_attributes']
    return best_path

# summarize_attrs summarizes the mrt_parse format into smaller format
# later this format is to be used with GoBGP API to set path attributes
# ends up with smaller json files
def summarize_attrs(path_attrs):
    summary = {}
    for attr in path_attrs:
        key = list(attr["type"].values())[0]
        value = attr["value"]
        summary[key] = value
    return summary

def main():
    v4, v6 = 0, 0
    v4_rib_json.write("[\n")
    v6_rib_json.write("[\n")
    for entry in Reader(args.mrt_file):
        if entry.data["subtype"] == {2:'RIB_IPV4_UNICAST'}:
            if v4 != 0:
                v4_rib_json.write(",\n")
            pfx = entry.data['prefix'] + "/" + str(entry.data['length'])
            if best_path_only:
                best_path = best_path_selection(entry.data['rib_entries'])
                json.dump({pfx:[summarize_attrs(best_path)]},v4_rib_json, indent=2)
            else:
                pfx_paths = {pfx:[]}
                for path in entry.data['rib_entries']:
                    pfx_paths[pfx].append(summarize_attrs(path['path_attributes']))
                json.dump(pfx_paths,v4_rib_json, indent=2)
            v4 += 1
        elif entry.data["subtype"] == {4: 'RIB_IPV6_UNICAST'}:
            if v6 != 0:
                v6_rib_json.write(",\n")
            pfx = entry.data['prefix'] + "/" + str(entry.data['length'])
            if best_path_only:
                best_path = best_path_selection(entry.data['rib_entries'])
                json.dump({pfx:[summarize_attrs(best_path)]},v6_rib_json, indent=2)
            else:
                pfx_paths = {pfx:[]}
                for path in entry.data['rib_entries']:
                    pfx_paths[pfx].append(summarize_attrs(path['path_attributes']))
                json.dump(pfx_paths,v6_rib_json, indent=2)
            v6 += 1
    v4_rib_json.write("]")
    v6_rib_json.write("]")
    v4_rib_json.close()
    v6_rib_json.close()

if __name__ == '__main__':
    main()