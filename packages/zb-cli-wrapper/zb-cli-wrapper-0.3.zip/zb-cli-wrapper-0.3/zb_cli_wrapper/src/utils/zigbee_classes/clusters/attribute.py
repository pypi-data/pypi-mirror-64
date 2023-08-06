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

from binascii import hexlify

import numpy as np

from zb_cli_wrapper.src.utils.cmd_wrappers.zigbee import constants


TYPE_MAP = {
    constants.TYPES.UINT8: lambda value: hexlify(np.uint8(value)).decode(),
    constants.TYPES.UINT16: lambda value: hexlify(np.uint16(value)).decode(),
    constants.TYPES.UINT32: lambda value: hexlify(np.uint32(value)).decode(),
    constants.TYPES.UINT64: lambda value: hexlify(np.uint64(value)).decode(),
    constants.TYPES.SINT8: lambda value: hexlify(np.int8(value)).decode(),
    constants.TYPES.SINT16: lambda value: hexlify(np.int16(value)).decode(),
    constants.TYPES.SINT64: lambda value: hexlify(np.int64(value)).decode(),
    constants.TYPES.ENUM8: lambda value: hexlify(np.uint8(value)).decode(),
    constants.TYPES.STRING: lambda value: f"{len(value):02X}" + hexlify(value.encode("ascii")).decode(),
}


class Attribute(object):
    def __init__(self, cluster, id, type, value=0, name="unknown"):
        self.cluster = cluster
        self.id = id
        self.type = type
        # If value is unsigned or signed int type
        if self.type in range(constants.TYPES.UINT8, constants.TYPES.ENUM8+1):
            self.value = int(value)
        # If value is bool type
        elif self.type is constants.TYPES.BOOL:
            self.value = self.to_bool(value)
        else:
            # Other types than ints or bool types are not parsed
            self.value = value
        self.name = name

    @property
    def formatted_id(self) -> str:
        return hexlify(np.uint16(self.id)).decode()

    @property
    def formatted_value(self) -> str:
        to_call = TYPE_MAP.get(self.type)
        if to_call:
            return to_call(self.value)
        raise NotImplementedError(f"Formatting type {self.type} is not implemented")

    def __repr__(self):
        return "Attribute {}: {}".format(self.name, self.value)

    @staticmethod
    def to_bool(bool_to_parse):
        if str(bool_to_parse).lower() in ['true', 'yes', 'y', '1']:
            return True
        elif str(bool_to_parse).lower() in ['false', 'no', 'n', '0']:
            return False
        else:
            return bool_to_parse


class StatusRecord:
    SUCCESS = 0x00
    INSUFFICIENT_SPACE = 0x89

    def __init__(self, attribute: Attribute, status_code):
        self.attribute = attribute
        self.status_code = status_code

    def to_hex(self) -> str:
        hex_ = f"{self.attribute.formatted_id}{self.status_code:02X}"

        if self.status_code == self.SUCCESS:
            hex_ += f"{self.attribute.type:02X}{self.attribute.formatted_value}"

        return hex_
