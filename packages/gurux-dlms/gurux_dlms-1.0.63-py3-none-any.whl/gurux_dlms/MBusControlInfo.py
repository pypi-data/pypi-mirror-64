#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                   $Date$
#                   $Author$
#
#  Copyright (c) Gurux Ltd
#
# ---------------------------------------------------------------------------
#
#   DESCRIPTION
#
#  This file is a part of Gurux Device Framework.
#
#  Gurux Device Framework is Open Source software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
#pylint: disable=broad-except,no-name-in-module
try:
    from enum import IntEnum
    __base = IntEnum
except Exception:
    __base = object

class MBusControlInfo(__base):
    """M-Bus control info."""
    #pylint: disable=too-few-public-methods

    # Long M-Bus data header present, direction master to slave
    LONG_HEADER_MASTER = 0x60

    # Short M-Bus data header present, direction master to slave
    SHORT_HEADER_MASTER = 0x61

    # Long M-Bus data header present, direction slave to master
    LONG_HEADER_SLAVE = 0x7C

    # Short M-Bus data header present, direction slave to master
    SHORT_HEADER_SLAVE = 0x7D

    # M-Bus short Header.
    SHORT_HEADER = 0x7A

    # M-Bus long Header.
    LONG_HEADER = 0x72
