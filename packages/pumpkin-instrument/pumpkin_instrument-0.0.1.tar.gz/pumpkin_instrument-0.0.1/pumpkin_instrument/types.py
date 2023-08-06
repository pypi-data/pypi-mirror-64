# coding: utf-8
# ##############################################################################
#  (C) Copyright 2020 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                              #
#  This file may be distributed under the terms of the License                 #
#  Agreement provided with this software.                                      #
#                                                                              #
#  THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
#  INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND                       #
#  FITNESS FOR A PARTICULAR PURPOSE.                                           #
# ##############################################################################
"""
Contains all of the protocols and types used throughout the pumpkin_instrument implementations
used for the BM2 Cycling system.
"""
from enum import Enum
from abc import abstractmethod, abstractstaticmethod
from typing import ContextManager, Union, List

from pumpkin_instrument.load import Load, LoadCapability, LoadChannelCapability
from pumpkin_instrument.dmm.types import MultimeterCapability, MultimeterChannelCapability, Multimeter
from pumpkin_instrument.psu.types import PowerSupplyCapability, PowerSupplyChannelCapability, PowerSupply

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol


class InstrumentType(Enum):
    """
    Represents the various types of lab instruments usable.
    """
    PowerSupply = 1,
    Load = 2,
    Multimeter = 3


Instruments = Union[Load, Multimeter, PowerSupply]
InstrumentChannelCapability = Union[LoadChannelCapability, MultimeterChannelCapability, PowerSupplyChannelCapability]
InstrumentCapability = Union[LoadCapability, MultimeterCapability, PowerSupplyCapability]


class Instrument(Protocol):
    @classmethod
    @abstractmethod
    def instrument_type(cls) -> InstrumentType:
        """
        What type of pumpkin_instrument is implemented. Currently there is:
            - PowerSupply
            - Load
            - Multimeter
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def instrument_capabilities(cls) -> InstrumentCapability:
        """
        Describes the capabilities of the pumpkin_instrument that apply to all channels. Currently this is only a placeholder
        for future API expansion.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def channel_capabilities(cls) -> List[InstrumentChannelCapability]:
        """

        """
        raise NotImplementedError()

    @abstractmethod
    def use(self) -> ContextManager[Instruments]:
        """
        Uses the pumpkin_instrument, taking control of it.
        """
        raise NotImplementedError()
