#
# Copyright (c) 2019 - 2020, Nordic Semiconductor ASA
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form, except as embedded into a Nordic
#    Semiconductor ASA integrated circuit in a product or a software update for
#    such product, must reproduce the above copyright notice, this list of
#    conditions and the following disclaimer in the documentation and/or other
#    materials provided with the distribution.
#
# 3. Neither the name of Nordic Semiconductor ASA nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# 4. This software, with or without modification, must only be used with a
#    Nordic Semiconductor ASA integrated circuit.
#
# 5. Any software provided in binary form under this license must not be reverse
#    engineered, decompiled, modified and/or disassembled.
#
# THIS SOFTWARE IS PROVIDED BY NORDIC SEMICONDUCTOR ASA "AS IS" AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY, NONINFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL NORDIC SEMICONDUCTOR ASA OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re
from collections import namedtuple
from typing import List

from ...zigbee_classes.long_address import LongAddress
from ..base import CommandWrapper as BaseCmdWrapper
from . import constants
from enum import Enum


MatchedEndpoint = namedtuple('MatchedEndpoint', ['src_add', 'id'])


class Commands:
    """ CLI Commands to be used with firmware which includes Zigbee CLI component with ZDO commands.
    """
    # Main command used in order to access ZDO subcommands
    MAIN = 'zdo'

    # Available ZDO commands
    EUI64 = ' '.join([MAIN, 'eui64'])
    EUI64_SET = ' '.join([MAIN, 'eui64 {dev_eui64:016X}'])
    SHORT = ' '.join([MAIN, 'short'])
    MATCH_DESC = ' '.join([MAIN, 'match_desc {dst_addr:04X} {req_addr:04X} {prof_id:04X} {input_cluster_ids} {output_cluster_ids}'])
    IEEE_ADDR = ' '.join([MAIN, 'ieee_addr {short_addr}'])
    NWK_ADDR = ' '.join([MAIN, 'nwk_addr {dst_eui64:016X}'])
    BIND = ' '.join([MAIN, 'bind on {src_eui64:016X} {src_ep} {dst_eui64:016X} {dst_ep} {cluster:01X} {dst_short:04X}'])
    MGMT_BIND = ' '.join([MAIN, 'mgmt_bind {short_addr:04X}'])
    MGMT_LQI = ' '.join([MAIN, 'mgmt_lqi {short_addr:04X}'])
    MGMT_LEAVE = ' '.join([MAIN, 'mgmt_leave {short_addr:04X}'])

    # Regex to use when parsing responses
    # Matches header of response to 'zdo mgmt_bind' CLI command
    BINDING_TABLE_HEADER_RE = re.compile(
        r"^\[idx]\s+src_address\s+src_endp\s+cluster_id\s+dst_addr_mode\s+dst_addr\s+dst_endp")

    # Matches binding table entry of response to 'zdo mgmt_bind' CLI command
    BINDING_TABLE_ENTRY_RE = re.compile(
        r"^"
        r"\[\s*(?P<idx>\d+)]"               # idx field, like: '[  0]' , '[  1]', '[120]'
        r"\s+"
        r"(?P<src_addr>[0-9a-fA-F]{16})"    # src_addr field, 16 hex digits
        r"\s+"
        r"(?P<src_endp>\d+)"                # src_endp field, decimal like '0', '1', '153'
        r"\s+"
        r"0x(?P<cluster_id>[0-9a-fA-F]+)"   # cluster_id field, hex number C fmt with 0x prefix, like: '0x104', '0x0104'
        r"\s+"
        r"(?P<dst_addr_mode>\d+)"           # dst_addr_mode field, decimal
        r"\s+"
        r"(?P<dst_addr>N/A|[0-9a-fA-F]+)"   # dst_addr field, 16 hex digits
        r"\s+"
        r"(?P<dst_endp>N/A|\d+)")           # dst_endp field, decimal like  '0', '1', '153'

    # Matches binding table recap of response to zdo mgmt_bind CLI command
    BINDING_TABLE_TOTAL_RE = re.compile(
        r"Total entries for the binding table: (\d+)")


class UnexpectedResponseError(Exception):
    """
    Exception raised when cli device responds in unexpected way.

    This may happen when cli command has changed and response can't be parsed or response is malformed.
    """
    pass


class ZigbeeBindingTableEntry:
    def __init__(self, src_addr, src_ep, cluster_id, dst_addr_mode, dst_addr, dst_ep):
        """
        Args:
            src_addr (int):         EUI64 source long address
            src_ep (int):           Source endpoint
            cluster_id (int):       Cluster id
            dst_addr_mode (int):    Destination address mode
            dst_addr (int):         EUI64 destination long address
            dst_ep (int):           Destination endpoint
        """
        self.src_addr = src_addr
        self.src_ep = src_ep
        self.cluster_id = cluster_id
        self.dst_addr_mode = dst_addr_mode
        self.dst_addr = dst_addr
        self.dst_ep = dst_ep

    def __eq__(self, other):
        return (self.src_addr == other.src_addr) and (self.src_ep == other.src_ep) and \
               (self.cluster_id == other.cluster_id) and (self.dst_addr_mode == other.dst_addr_mode) and \
               (self.dst_addr == other.dst_addr) and (self.dst_ep == other.dst_ep)

    def __str__(self):
        return self.to_row_str()

    def to_row_str(self):
        return '{:016x} {:3d} 0x{:04x} {:3d} {:016x} {:3d}'.format(self.src_addr, self.src_ep, self.cluster_id, self.dst_addr_mode, self.dst_addr, self.dst_ep)

class ZigbeeZdoMgmtLqiEntry:
    def __init__(self, ext_pan_id, ext_addr, short_addr, flags, permit_join, depth, lqi):
        """
        Args:
            ext_pan_id (int):       Extended PAN ID
            ext_addr (int):         EUI64 source long address
            short_addr (int):       Short address
            flags (int):            Flags
            permit_join (int):      Permit Join flag
            depth (int):            Tree depth
            lqi (int):              LQI
        """
        self.ext_pan_id = ext_pan_id
        self.ext_addr = ext_addr
        self.short_addr = short_addr
        self.flags = flags
        self.permit_join = permit_join
        self.depth = depth
        self.lqi = lqi

    def __eq__(self, other):
        return (self.ext_pan_id == other.ext_pan_id) and (self.ext_addr == other.ext_addr) and \
               (self.short_addr == other.short_addr) and (self.flags == other.flags) and \
               (self.permit_join == other.permit_join) and (self.depth == other.depth) and \
               (self.lqi == other.lqi)

    def __str__(self):
        return '{:016x} {:16x} 0x{:04x} 0x{:02x} {:d} {:d} {:d}'.format(self.ext_pan_id,
                self.ext_addr, self.short_addr, self.flags, self.permit_join, self.depth, self.lqi)

class ZigbeeBindingTable:
    """
    Class representing Zigbee Binding Table. It is just a list of ZigbeeBindingTableEntry objects with helper methods
    """
    def __init__(self):
        self.entries = []

    def add(self, entry):
        self.entries.append(entry)

    def contains(self, entry):
        """
        Checks if Binding Table contains given entry

        Args:
            entry (ZigbeeBindingTableEntry):    Entry to find

        Returns:

        """
        for ent in self.entries:
            if ent == entry:
                return True

        return False

    def __eq__(self, other):
        """
        Equality operator. Checks if two binding tables are equal. Note that binding table order is not important

        Args:
            other (ZigbeeBindingTable):

        Returns:
            bool: True if the two binding tables have the same entries (regardless of their order), False otherwise

        """
        if self.length != other.length:
            return False

        for ent in self.entries:
            if not other.contains(ent):
                return False

        for ent in other.entries:
            if not self.contains(ent):
                return False

        return True

    def __str__(self):
        retstr = ""
        for i, ent in enumerate(self.entries):
            retstr += f"[{i:3d}] {ent}\n"
        return retstr

    @property
    def length(self):
        return len(self.entries)


class CommandWrapper(BaseCmdWrapper):
    """ This class adds an interface for sending ZDO commands and receiving parsed
        responses through Zigbee CLI by calling methods on a device instance.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def eui64(self):
        """ Reads device's long address (EUI64) through CLI interface.

            Returns:
                LongAddress: representing device long address.

            Raises:
                ValueError: if received result with an unknown formatting
                CommandError: if CLI returns error
                TimeoutError: if timeout occurred
        """
        responses = self.cli.write_command(Commands.EUI64)
        return LongAddress(responses[-1])

    @eui64.setter
    def eui64(self, new_address):
        """ Set device's EUI64 address.

            Args:
                new_address (int): new device long address

            Raises:
                CommandError: if CLI returns error
                TimeoutError: if timeout occurred
        """
        self.cli.write_command(Commands.EUI64_SET.format(dev_eui64=new_address))

    @property
    def short_addr(self):
        """ Reads device's short address through CLI interface.

            Returns:
                int: representing device short address.

            Raises:
                ValueError: if received result with an unknown formatting
                CommandError: if device is not commissioned
                TimeoutError: if timeout occurred
        """
        responses = self.cli.write_command(Commands.SHORT)
        return int(responses[-1], 16)

    @short_addr.setter
    def short_addr(self, new_address):
        """ Currently setting device short address is not supported.

            Args:
                new_address (int): new device short (network) address

            Raises:
                ValueError: if received result with an unknown formatting
                CommandError: if device is not commissioned
                TimeoutError: if timeout occurred
                NotImplementedError: if current CLI implementation does not support network address update
        """
        raise NotImplementedError("Setting device short address is not supported")

    def match_desc(self, input_clusters, output_clusters, timeout=80.0,
                   dst_addr=constants.BROADCAST_ADDRESS_ALL_DEVICES, req_addr=constants.BROADCAST_ADDRESS_ALL_DEVICES,
                   prof_id=constants.DEFAULT_ZIGBEE_PROFILE_ID) -> List[MatchedEndpoint]:
        """ Send the Match Descriptor Request command.

            Args:
                dst_addr: 16-bit destination address
                req_addr: requested address/type
                prof_id: profile ID
                input_clusters[int]: input cluster IDs
                output_clusters[int]: output cluster IDs
                timeout (float): maximum time, in seconds, within which CLI should return command response

            Raises:
                ValueError: if attempts to write unsupported value type
                CommandError: if CLI returns error
                TimeoutError: if timeout occurred

            Returns:
                List of MatchedEndpoint
        """

        input_cluster = [str(len(input_clusters))] + [hex(e) for e in input_clusters]
        output_cluster = [str(len(output_clusters))] + [hex(e) for e in output_clusters]
        input_clusters_str = ' '.join(input_cluster)
        output_clusters_str = ' '.join(output_cluster)

        cmd = Commands.MATCH_DESC.format(dst_addr=dst_addr, req_addr=req_addr, prof_id=prof_id,
                                         input_cluster_ids=input_clusters_str, output_cluster_ids=output_clusters_str)

        response = self.cli.write_command(cmd, timeout=timeout)

        responses = []

        for r in response:
            match_response = re.search(r'src_addr=([0-9a-fA-F]+) ep=(\d+)', r)
            if match_response:
                responses.append(MatchedEndpoint(*match_response.groups()))

        return responses

    def ieee_addr(self, short_addr, timeout=20.0):
        """ Resolve the short network address `short_addr` to an EUI64 address.

            Args:
                short_addr (str): Short addres of the device
                timeout (float): maximum time, in seconds, within which CLI should return command response

            Raises:
                CommandError: if CLI returns error
                TimeoutError: if timeout occurred                

            Return:
                LongAddress: representing device long (EUI64) address.
        """
        cmd = Commands.IEEE_ADDR.format(short_addr=short_addr)
        response = self.cli.write_command(cmd, timeout=timeout)
        return LongAddress(response[-1])

    def nwk_addr(self, dst_eui64, timeout=20.0):
        """
        Resolve the EUI64 address to a short network address `short_addr`.
        Args:
            dst_eui64 (int): EUI64 address of the device for which short network address is requested
            timeout (float): maximum time, in seconds, within which CLI should return command response

        Raises:
            CommandError: if CLI returns error
            TimeoutError: if timeout occurred

        Returns:
            int: devices's short address

        """
        cmd = Commands.NWK_ADDR.format(dst_eui64=dst_eui64)
        response = self.cli.write_command(cmd, timeout=timeout)
        short_addr = int(response[-1], 16)
        return short_addr

    def bind(self, src_eui64, src_ep, dst_eui64, dst_ep, cluster, dst_short):
        """
            Send the Bind Request command.

            Args:
                src_eui64(int): EUI64 address of the source of the binding
                src_ep(int): endpoint of the source of the binding
                dst_eui64(int): EUI64 address of the destination of the binding
                dst_ep(int): endpoint of the destination of the binding
                cluster(int): ZCL cluster which is being bound
                dst_short(int): short address of where the command should be sent

            Raises:
                CommandError: if CLI returns error
                TimeoutError: if timeout occurred
        """
        cmd = Commands.BIND.format(src_eui64=src_eui64, src_ep=src_ep, dst_eui64=dst_eui64, dst_ep=dst_ep,
                                   cluster=cluster, dst_short=dst_short)
        self.cli.write_command(cmd, timeout=10.0)

    def get_binding_table(self, short_addr, timeout=20.0):
        """
        Send the zdo mgmt_bind request command and get binding table

        Args:
            short_addr (int):   Short address of target device from which binding table should be get

        Raises:
            UnexpectedResponseError: if cli response to mgmt_bind command is malformed and cannot be parsed
            CommandError: if CLI returns error
            TimeoutError: if timeout occurred

        Returns:
            ZigbeeBindingTable: Binding table filled up with entries received from given device
        """
        cmd = Commands.MGMT_BIND.format(short_addr=short_addr)
        response = self.cli.write_command(cmd, timeout=timeout)
        result = ZigbeeBindingTable()
        expected_idx = 0

        class ParsingFsmState(Enum):
            reset = 1
            header = 2
            entries = 3
            total = 4

        parsing_fsm_state = ParsingFsmState.reset

        for r in response:
            x = Commands.BINDING_TABLE_HEADER_RE.search(r)
            if x is not None:
                if parsing_fsm_state != ParsingFsmState.reset:
                    raise UnexpectedResponseError("Unexpected additional binding table header received")
                parsing_fsm_state = ParsingFsmState.header
                continue

            x = Commands.BINDING_TABLE_ENTRY_RE.search(r)
            if x is not None:
                if (parsing_fsm_state == ParsingFsmState.header) or (parsing_fsm_state == ParsingFsmState.entries):
                    received_idx = int(x.group('idx'))
                    if expected_idx != received_idx:
                        raise UnexpectedResponseError(f"Unexpected binding table idx field received ({expected_idx} != {received_idx})")

                    # Handle special cases for destination address/destination endpoint.
                    if x.group('dst_addr') == "N/A":
                        dst_addr = -1
                    else:
                        dst_addr = int(x.group('dst_addr'), 16)

                    if x.group('dst_endp') == "N/A":
                        dst_endp = -1
                    else:
                        dst_endp = int(x.group('dst_endp'))

                    # Construct object from match using groups. This shall not fail as the regex matches
                    # valid characters only
                    entry = ZigbeeBindingTableEntry(
                        src_addr=int(x.group('src_addr'), 16),
                        src_ep=int(x.group('src_endp')),
                        cluster_id=int(x.group('cluster_id'), 16),
                        dst_addr_mode=int(x.group('dst_addr_mode')),
                        dst_addr=dst_addr,
                        dst_ep=dst_endp)

                    result.add(entry)
                    expected_idx += 1
                    parsing_fsm_state = ParsingFsmState.entries

                elif parsing_fsm_state == ParsingFsmState.reset:
                    raise UnexpectedResponseError("Binding table entry received, but no header "
                                                  "had been received before")
                else:
                    raise UnexpectedResponseError(
                        "Binding table entry received after binding table recap had been received")
                continue

            x = Commands.BINDING_TABLE_TOTAL_RE.search(r)
            if x is not None:
                if parsing_fsm_state == ParsingFsmState.total:
                    raise UnexpectedResponseError(
                        "Unexpected extra binding table total entries count received")
                else:
                    total_entries_reported = int(x.group(1))
                    if total_entries_reported != expected_idx:
                        raise UnexpectedResponseError("Mismatch of real binding table entries received " 
                                                      "with reported total entries count")
                    parsing_fsm_state = ParsingFsmState.total
                continue

            # Note: We allow other lines with content not matching any of used regex, but we simply ignore them

        if parsing_fsm_state != ParsingFsmState.total:
            raise UnexpectedResponseError("Missing total binding table entries row")

        return result

    def get_lqi_table(self, short_addr, timeout=20.0):
        """
        Send the zdo mgmt_lqi request command and get lqi table

        Args:
            short_addr (int):   Short address of target device from which lqi table should be get

        Raises:
            UnexpectedResponseError: if cli response to mgmt_lqi command is malformed and cannot be parsed
            CommandError: if CLI returns error
            TimeoutError: if timeout occurred

        Returns:
            ZigbeeLqiTable: LQI table filled up with entries received from given device
        """
        # Matches binding table entry of response to 'zdo mgmt_bind' CLI command
        lqi_table_entry_re = re.compile(
            r"\[\s*(?P<idx>\d+)]"               # idx field, like: '[  0]' , '[  1]', '[120]'
            r"\s+"
            r"(?P<ext_pan_id>[0-9a-fA-F]{16})"  # ext_pan_id field, 16 hex digits
            r"\s+"
            r"(?P<ext_addr>[0-9a-fA-F]{16})"    # ext_addr field, 16 hex digits
            r"\s+"
            r"0x(?P<short_addr>[0-9a-fA-F]+)"   # short_addr, hex number C fmt with 0x prefix, like: '0x104', '0x0104'
            r"\s+"
            r"0x(?P<flags>[0-9a-fA-F]+)"        # flags field, hex number C fmt with 0x prefix, like: '0x104', '0x0104'
            r"\s+"
            r"(?P<permit_join>\d{1})"           # permit_join field, decimal
            r"\s+"
            r"(?P<depth>\d+)"                   # tree depth, decimal
            r"\s+"
            r"(?P<lqi>\d+)")                    # lqi field, decimal like  '0', '1', '153'

        lqi_table_entry_header_re = re.compile(r"^\[idx]\s+ext_pan_id\s+ext_addr\s+short_addr\s+flags\s+permit_join\s+depth\s+lqi")

        cmd = Commands.MGMT_LQI.format(short_addr=short_addr)
        response = self.cli.write_command(cmd, timeout=timeout)
        result = []

        if not lqi_table_entry_header_re.match(response[0]):
            raise UnexpectedResponseError("Header not found")

        # Cut off table header
        for r in response[1:]:
            m = lqi_table_entry_re.match(r)
            if m:
                entry = ZigbeeZdoMgmtLqiEntry(ext_pan_id=int(m.group('ext_pan_id'), 16),
                                            ext_addr=int(m.group('ext_addr'), 16),
                                            short_addr=int(m.group('short_addr'), 16),
                                            flags=int(m.group('flags'), 16),
                                            permit_join=int(m.group('permit_join')),
                                            depth=int(m.group('depth')),
                                            lqi=int(m.group('lqi')))
                result.append(entry)

        return result

    def mgmt_leave(self, short_addr, device_address=None, rejoin=False, children=False):
        """
        Send the zdo mgmt_leave request command

        Args:
            short_addr (int): Short address of target device
            device_address (int): Long address of device to remove from the network. If None, target device will remove itself
            rejoin (bool): value of Rejoin flag
            children (bool): value of Remove Children flag

        Raises:
            CommandError: if CLI returns error
            TimeoutError: if timeout occurred
        """
        cmd = Commands.MGMT_LEAVE.format(short_addr=short_addr, device_address=device_address)
        if device_address is not None:
            cmd += f" {device_address:016X}"
        if rejoin:
            cmd += " --rejoin"
        if children:
            cmd += " --children"
        self.cli.write_command(cmd)