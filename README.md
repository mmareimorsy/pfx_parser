# pfx_parser

Internet routing table is typically captured & stored into MRT formatted files, MRT is described in [RFC6396](https://datatracker.ietf.org/doc/html/rfc6396), The MRT files are available for public use as collected by [RIPE_NCC](https://www.ripe.net/analyse/internet-measurements/routing-information-service-ris/archive/ris-raw-data)

As listed on RIPE NCC webpage, there are already alot of open source tools available to process MRT files [Tools](https://ris.ripe.net/docs/20_raw_data_mrt.html#tooling), this repo is relying on one of those tools which is [MRT parser](https://github.com/t2mune/mrtparse) to help in parsing the MRT files.

It is a common requirement for network engineers to try sending a copy or more of the current internet routing table to a routing device under test, this is usually done to test convergence, FIB capacity, etc..

The purpose of pfx_parser.py in this repo is the following:

* Parse & re-format the content of an MRT file to a summarized JSON file
* The output JSON file is meant to be used later with [GoBGP](https://github.com/osrg/gobgp), which is an open source BGP client.
* GoBGP is used in this case as a BGP speaker to send to the device under test a copy of the internet routing table with its BGP path attributes, so it becomes a quick way to build a test setup when there is no access to commerical network test tools.

## How to setup

Please install via PIP the packages in requirements.txt 

```
python3 -m pip install -r requirements.txt
```

## How to use

1) Please download an MRT file to use, example snapshot from [April 2023](https://data.ris.ripe.net/rrc00/2023.04/bview.20230424.1600.gz)

2) There is a small CLI wrapper around the script, you can use help to see the available options:

```
./pfx_parser.py --help
usage: --help to list available commands

Inet prefix parser

options:
  -h, --help            show this help message and exit
  -m MRT_FILE, --mrt_file MRT_FILE
                        MRT file to parse
  -a, --all_paths       save all paths instead of best path only
```

3) Example:

```
./pfx_parser.py -m bview.20230424.1600.gz
```
The script expects two arguments:

* Required argument:

    * MRT gzipped file (-m, --mrt_file)

* Optional argument:
    * -a,--all_paths: Toggle best path only or all paths option

As MRT files store all available BGP paths as seen by BGP collectors so this means that for a single prefix there is at least a handful BGP paths (each with its own set of attributes) for that given prefix.

To save time & space, the script by default runs a not so accurate BGP path selection against the available paths for each prefix, so the default expected end result is for a single prefix to have a single BGP path, below is an example result for 0.0.0.0/0 prefix.


```
{
  "0.0.0.0/0": [
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 1,
          "value": [
            "58057"
          ]
        }
      ],
      "NEXT_HOP": "94.177.122.247"
    }
  ]
},
```

If the desired outcome however is to have all the available paths stored in the JSON output file, then you can run the script with ```-a``` option to save all the paths & don't run the BGP selection, if you do so it is expected that the DUT receiving the paths will just select one path to install.

```
./pfx_parser.py -m ../../pfx_parser/bview.20230424.1600.gz -a
```

This leads to following paths stored for 0.0.0.0/0 prefix

```
{
  "0.0.0.0/0": [
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 2,
          "value": [
            "37721",
            "6762"
          ]
        }
      ],
      "NEXT_HOP": "165.16.221.66",
      "COMMUNITY": [
        "37721:4000",
        "37721:4008",
        "37721:4200",
        "37721:4260"
      ]
    },
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 2,
          "value": [
            "44393",
            "50892"
          ]
        }
      ],
      "NEXT_HOP": "49.12.70.222"
    },
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 1,
          "value": [
            "58057"
          ]
        }
      ],
      "NEXT_HOP": "94.177.122.247"
    },
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 2,
          "value": [
            "44393",
            "50892"
          ]
        }
      ],
      "NEXT_HOP": "49.12.70.222"
    },
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 1,
          "value": [
            "58057"
          ]
        }
      ],
      "NEXT_HOP": "94.177.122.247"
    },
    {
      "ORIGIN": {
        "2": "INCOMPLETE"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 1,
          "value": [
            "55720"
          ]
        }
      ],
      "NEXT_HOP": "103.212.68.10"
    },
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 1,
          "value": [
            "50628"
          ]
        }
      ],
      "NEXT_HOP": "178.208.11.4"
    },
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 1,
          "value": [
            "34927"
          ]
        }
      ],
      "NEXT_HOP": "45.134.89.1"
    },
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 1,
          "value": [
            "35708"
          ]
        }
      ],
      "NEXT_HOP": "94.177.122.231"
    },
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 2,
          "value": [
            "44103",
            "1299"
          ]
        }
      ],
      "NEXT_HOP": "185.235.144.33",
      "MULTI_EXIT_DISC": 0
    },
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 1,
          "value": [
            "47422"
          ]
        }
      ],
      "NEXT_HOP": "94.177.122.241"
    },
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 2,
          "value": [
            "34854",
            "1299"
          ]
        }
      ],
      "NEXT_HOP": "2.56.11.1",
      "COMMUNITY": [
        "34854:3001"
      ]
    },
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 2,
          "value": [
            "50304",
            "1299"
          ]
        }
      ],
      "NEXT_HOP": "31.169.49.228"
    },
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 3,
          "value": [
            "131477",
            "60068",
            "174"
          ]
        }
      ],
      "NEXT_HOP": "103.102.5.1"
    },
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 2,
          "value": [
            "61292",
            "24482"
          ]
        }
      ],
      "NEXT_HOP": "185.152.34.255"
    },
    {
      "ORIGIN": {
        "0": "IGP"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 3,
          "value": [
            "34927",
            "12186",
            "174"
          ]
        }
      ],
      "NEXT_HOP": "193.148.251.1",
      "COMMUNITY": [
        "34927:210"
      ]
    },
    {
      "ORIGIN": {
        "2": "INCOMPLETE"
      },
      "AS_PATH": [
        {
          "type": {
            "2": "AS_SEQUENCE"
          },
          "length": 1,
          "value": [
            "55720"
          ]
        }
      ],
      "NEXT_HOP": "45.116.179.212"
    }
  ]
},
```

Output will be saved in local directory as "ipv4_rib.json" & "ipv6_rib.json" for IPv4 & IPv6 internet prefixes respectively.

Example results from this [snapshot April 2023]()can be downloaded from Gdrive [Here](https://drive.google.com/drive/folders/1-2CZHaXhaQ_j9WdbaT3KqjPMG-FWzeob?usp=sharing)

Note: MRT files are known to be large in size & content, so it is expected for the script to take some time to finish executing (~25 minutes on my test setup which is a 12th gen intel i7 CPU)

### References

* [RFC6396](https://datatracker.ietf.org/doc/html/rfc6396)
* [mrt parser](https://github.com/t2mune/mrtparse)
* [GoBGP](https://github.com/osrg/gobgp)
* [GoBGP API](https://pkg.go.dev/github.com/osrg/gobgp/api)
