﻿'''_3418.py

PlanetCarrierCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model import _2007
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3293
from mastapy.system_model.analyses_and_results.power_flows.compound import _3410
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'PlanetCarrierCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCompoundPowerFlow',)


class PlanetCarrierCompoundPowerFlow(_3410.MountableComponentCompoundPowerFlow):
    '''PlanetCarrierCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2007.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2007.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3293.PlanetCarrierPowerFlow]':
        '''List[PlanetCarrierPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3293.PlanetCarrierPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3293.PlanetCarrierPowerFlow]':
        '''List[PlanetCarrierPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3293.PlanetCarrierPowerFlow))
        return value
