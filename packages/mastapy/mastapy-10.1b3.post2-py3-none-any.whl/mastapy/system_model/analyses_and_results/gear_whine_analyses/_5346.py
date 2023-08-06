'''_5346.py

SpiralBevelGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2060
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6157
from mastapy.system_model.analyses_and_results.system_deflections import _2289
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5344, _5345, _5246
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'SpiralBevelGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetGearWhineAnalysis',)


class SpiralBevelGearSetGearWhineAnalysis(_5246.BevelGearSetGearWhineAnalysis):
    '''SpiralBevelGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2060.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2060.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6157.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6157.SpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2289.SpiralBevelGearSetSystemDeflection':
        '''SpiralBevelGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2289.SpiralBevelGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_gear_whine_analysis(self) -> 'List[_5344.SpiralBevelGearGearWhineAnalysis]':
        '''List[SpiralBevelGearGearWhineAnalysis]: 'GearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsGearWhineAnalysis, constructor.new(_5344.SpiralBevelGearGearWhineAnalysis))
        return value

    @property
    def spiral_bevel_gears_gear_whine_analysis(self) -> 'List[_5344.SpiralBevelGearGearWhineAnalysis]':
        '''List[SpiralBevelGearGearWhineAnalysis]: 'SpiralBevelGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsGearWhineAnalysis, constructor.new(_5344.SpiralBevelGearGearWhineAnalysis))
        return value

    @property
    def meshes_gear_whine_analysis(self) -> 'List[_5345.SpiralBevelGearMeshGearWhineAnalysis]':
        '''List[SpiralBevelGearMeshGearWhineAnalysis]: 'MeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesGearWhineAnalysis, constructor.new(_5345.SpiralBevelGearMeshGearWhineAnalysis))
        return value

    @property
    def spiral_bevel_meshes_gear_whine_analysis(self) -> 'List[_5345.SpiralBevelGearMeshGearWhineAnalysis]':
        '''List[SpiralBevelGearMeshGearWhineAnalysis]: 'SpiralBevelMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesGearWhineAnalysis, constructor.new(_5345.SpiralBevelGearMeshGearWhineAnalysis))
        return value
