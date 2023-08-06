﻿'''_3273.py

PlanetCarrierPowerFlow
'''


from mastapy.system_model.part_model import _1987
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6139
from mastapy.system_model.analyses_and_results.power_flows import _3265
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'PlanetCarrierPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierPowerFlow',)


class PlanetCarrierPowerFlow(_3265.MountableComponentPowerFlow):
    '''PlanetCarrierPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1987.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6139.PlanetCarrierLoadCase':
        '''PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6139.PlanetCarrierLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
