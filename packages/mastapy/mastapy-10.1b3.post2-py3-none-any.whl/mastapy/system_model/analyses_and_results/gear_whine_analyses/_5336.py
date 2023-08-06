﻿'''_5336.py

RollingRingGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2107
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6148
from mastapy.system_model.analyses_and_results.system_deflections import _2280
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5268
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'RollingRingGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingGearWhineAnalysis',)


class RollingRingGearWhineAnalysis(_5268.CouplingHalfGearWhineAnalysis):
    '''RollingRingGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2107.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2107.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6148.RollingRingLoadCase':
        '''RollingRingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6148.RollingRingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2280.RollingRingSystemDeflection':
        '''RollingRingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2280.RollingRingSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[RollingRingGearWhineAnalysis]':
        '''List[RollingRingGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingGearWhineAnalysis))
        return value
