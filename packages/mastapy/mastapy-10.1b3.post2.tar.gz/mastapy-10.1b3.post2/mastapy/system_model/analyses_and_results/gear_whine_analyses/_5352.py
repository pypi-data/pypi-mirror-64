'''_5352.py

StraightBevelDiffGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2062
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6164
from mastapy.system_model.analyses_and_results.system_deflections import _2295
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5350, _5351, _5246
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'StraightBevelDiffGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetGearWhineAnalysis',)


class StraightBevelDiffGearSetGearWhineAnalysis(_5246.BevelGearSetGearWhineAnalysis):
    '''StraightBevelDiffGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2062.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2062.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6164.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6164.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2295.StraightBevelDiffGearSetSystemDeflection':
        '''StraightBevelDiffGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2295.StraightBevelDiffGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_gear_whine_analysis(self) -> 'List[_5350.StraightBevelDiffGearGearWhineAnalysis]':
        '''List[StraightBevelDiffGearGearWhineAnalysis]: 'GearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsGearWhineAnalysis, constructor.new(_5350.StraightBevelDiffGearGearWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_gears_gear_whine_analysis(self) -> 'List[_5350.StraightBevelDiffGearGearWhineAnalysis]':
        '''List[StraightBevelDiffGearGearWhineAnalysis]: 'StraightBevelDiffGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsGearWhineAnalysis, constructor.new(_5350.StraightBevelDiffGearGearWhineAnalysis))
        return value

    @property
    def meshes_gear_whine_analysis(self) -> 'List[_5351.StraightBevelDiffGearMeshGearWhineAnalysis]':
        '''List[StraightBevelDiffGearMeshGearWhineAnalysis]: 'MeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesGearWhineAnalysis, constructor.new(_5351.StraightBevelDiffGearMeshGearWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_gear_whine_analysis(self) -> 'List[_5351.StraightBevelDiffGearMeshGearWhineAnalysis]':
        '''List[StraightBevelDiffGearMeshGearWhineAnalysis]: 'StraightBevelDiffMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesGearWhineAnalysis, constructor.new(_5351.StraightBevelDiffGearMeshGearWhineAnalysis))
        return value
