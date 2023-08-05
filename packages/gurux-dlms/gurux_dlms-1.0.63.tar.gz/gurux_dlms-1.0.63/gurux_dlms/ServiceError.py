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
import sys
if sys.version_info < (3, 0):
    __base = object
else:
    from enum import IntEnum
    __base = IntEnum

class ServiceError(__base):
    """
    ServiceError enumerates service errors.
    """

     # Application error.
    APPLICATION_REFERENCE = 0

     # Hardware error.
    HARDWARE_RESOURCE = 1

     # Vde state error.
    VDE_STATE_ERROR = 2

     # Service error.
    SERVICE = 3

     # Definition error.
    DEFINITION = 4

     # Access error.
    ACCESS = 5

     # Initiate error.
    INITIATE = 6

     # LoadDataSet error.
    LOAD_DATASET = 7

     # Task error.
    TASK = 8

     # Other error describes manufacturer specific error code.
    OTHER_ERROR = 9
