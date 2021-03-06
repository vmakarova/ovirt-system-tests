#
# Copyright 2017 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#

import ovirtsdk4.types


def _get_attachment_by_id(host, network_id):
    return next(att for att in host.network_attachments_service().list()
                if att.network.id == network_id)


def modify_ip_config(engine,
                     host,
                     network_name,
                     ip_configuration):
    network_id = engine.networks_service().list(
        search='name={}'.format(network_name))[0].id

    attachment = _get_attachment_by_id(host, network_id)
    attachment.ip_address_assignments = ip_configuration

    return host.setup_networks(modified_network_attachments=[attachment],
                               check_connectivity=True)


def create_static_ip_configuration(ipv4_addr=None,
                                   ipv4_mask=None,
                                   ipv6_addr=None,
                                   ipv6_mask=None):
    assignments = []
    if ipv4_addr:
        assignments.append(ovirtsdk4.types.IpAddressAssignment(
            assignment_method=ovirtsdk4.types.BootProtocol.STATIC,
            ip=ovirtsdk4.types.Ip(
                address=ipv4_addr,
                netmask=ipv4_mask)))
    if ipv6_addr:
        assignments.append(ovirtsdk4.types.IpAddressAssignment(
            assignment_method=ovirtsdk4.types.BootProtocol.STATIC,
            ip=ovirtsdk4.types.Ip(
                address=ipv6_addr,
                netmask=ipv6_mask,
                version=ovirtsdk4.types.IpVersion.V6)))

    return assignments
