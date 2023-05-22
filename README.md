# pfx_parser# pfx_parser

Internet routing table is typically captured & stored into MRT formatted files, MRT is described in RFC6396[https://datatracker.ietf.org/doc/html/rfc6396], The MRT files are available for public use as collected by RIPE_NCC[https://www.ripe.net/analyse/internet-measurements/routing-information-service-ris/archive/ris-raw-data]

As listed on RIPE NCC webpage, there are already alot of open source tools available to process MRT files Tools[https://ris.ripe.net/docs/20_raw_data_mrt.html#tooling]

It is a common requirement for network engineers to try sending a copy or more from the current internet routing table to a routing system under test, this is usually done to test convergence, FIB capacity, etc..

The purpose of pfx_parser.py in this repo is the following:

* Parse & re-format the content of an MRT file to a summarized JSON file
* The output JSON file is meant to be used later with GoBGP[https://github.com/osrg/gobgp], which is an open source BGP client.
* GoBGP is used in this case as a BGP speaker to send to the device under test a copy of the internet routing table with its BGP path attributes, so it becomes a quick way to build a test setup when there is no access to commerical network test tools.

## How to setup

## How to use

### References

* MRT format: RFC6396[https://datatracker.ietf.org/doc/html/rfc6396]
* mrt parser[https://github.com/t2mune/mrtparse]
* GoBGP[https://github.com/osrg/gobgp]
