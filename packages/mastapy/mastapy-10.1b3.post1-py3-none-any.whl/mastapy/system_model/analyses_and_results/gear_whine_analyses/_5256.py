'''_5256.py

BearingGearWhineAnalysis
'''


from typing import List

from mastapy.bearings.bearing_results.rolling import _1681
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _1982
from mastapy.system_model.analyses_and_results.static_loads import _6051
from mastapy.system_model.analyses_and_results.system_deflections import _2210
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5285
from mastapy._internal.python_net import python_net_import

_BEARING_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'BearingGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingGearWhineAnalysis',)


class BearingGearWhineAnalysis(_5285.ConnectorGearWhineAnalysis):
    '''BearingGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def rolling_bearing_speed_results(self) -> '_1681.RollingBearingSpeedResults':
        '''RollingBearingSpeedResults: 'RollingBearingSpeedResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1681.RollingBearingSpeedResults)(self.wrapped.RollingBearingSpeedResults) if self.wrapped.RollingBearingSpeedResults else None

    @property
    def component_design(self) -> '_1982.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1982.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6051.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6051.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2210.BearingSystemDeflection':
        '''BearingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2210.BearingSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def planetaries(self) -> 'List[BearingGearWhineAnalysis]':
        '''List[BearingGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingGearWhineAnalysis))
        return value
