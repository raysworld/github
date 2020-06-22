#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Robin Wen <blockxyz@gmail.com>
#
# Distributed under terms of the MIT license.

import socket
import os
import sys

# we are using dnspython version 2.0.0rc1, which works only for Python 3.0+
import dns.resolver as dns_res
import dns.rdatatype as dns_type

file_path = os.path.split(os.path.realpath(__file__))[0]

def get_ip(host):
    """
    Get ip of host.
    """
    try:
        host_ip = socket.gethostbyname(host)
        return host_ip
    except:
        print("Unable to get IP of Hostname")

def get_ip_dns(host):
    """
    Get ip of host via dnspython
    """
    # create a DNS resolver
    resolver = dns_res.Resolver()
   
    try:
        # find the real domain name via CNAME (rdtype = 5)
        # see https://dnspython.readthedocs.io/en/latest/_modules/dns/rdatatype.html
        cname = resolver.resolve(host, rdtype=dns_type.CNAME, search=True)
        cname = cname[0].to_text()
    except dns_res.NoAnswer:
        # if the website address is the real name, then CNAME may find nothing, in 
        # such case we can ignore this exception
        print('CNAME not found for {}, try find its IP directly.'.format(host))
        cname = host
    except:
        print('Error querying the IP address of the website.')
        exit(-1)

    # find the ip address of the real domain
    host_ip = resolver.resolve(cname, rdtype=dns_type.A, search=True)

    return host_ip


def main():
    f = open('%s/github_hosts.txt' % file_path,'w')
    f.write("# GitHub Start\n")
    f.close()

    with open("%s/github_domain.txt" % file_path, "r") as ins:
        for host in ins:
            # print(host.strip())
            ip = get_ip_dns(host.strip())

            HOST = host.strip()
            IP = ip[0].to_text()

            print('{} {}'.format(IP, HOST))

            with open('%s/github_hosts.txt' % file_path, 'a') as result:
                result.write('{} {}\n'.format(IP, HOST))

    f = open('%s/github_hosts.txt' % file_path,'a')
    f.write("\n# GitHub End\n")
    f.close()

if __name__ == "__main__":
    main()
