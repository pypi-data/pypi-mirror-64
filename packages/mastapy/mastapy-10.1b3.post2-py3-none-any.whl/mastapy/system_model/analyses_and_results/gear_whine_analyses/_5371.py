'''_5371.py

WormGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2068
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6188
from mastapy.system_model.analyses_and_results.system_deflections import _2318
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5369, _5370, _5298
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'WormGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetGearWhineAnalysis',)


class WormGearSetGearWhineAnalysis(_5298.GearSetGearWhineAnalysis):
    '''WormGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2068.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2068.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6188.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6188.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2318.WormGearSetSystemDeflection':
        '''WormGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2318.WormGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_gear_whine_analysis(self) -> 'List[_5369.WormGearGearWhineAnalysis]':
        '''List[WormGearGearWhineAnalysis]: 'GearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsGearWhineAnalysis, constructor.new(_5369.WormGearGearWhineAnalysis))
        return value

    @property
    def worm_gears_gear_whine_analysis(self) -> 'List[_5369.WormGearGearWhineAnalysis]':
        '''List[WormGearGearWhineAnalysis]: 'WormGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsGearWhineAnalysis, constructor.new(_5369.WormGearGearWhineAnalysis))
        return value

    @property
    def meshes_gear_whine_analysis(self) -> 'List[_5370.WormGearMeshGearWhineAnalysis]':
        '''List[WormGearMeshGearWhineAnalysis]: 'MeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesGearWhineAnalysis, constructor.new(_5370.WormGearMeshGearWhineAnalysis))
        return value

    @property
    def worm_meshes_gear_whine_analysis(self) -> 'List[_5370.WormGearMeshGearWhineAnalysis]':
        '''List[WormGearMeshGearWhineAnalysis]: 'WormMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesGearWhineAnalysis, constructor.new(_5370.WormGearMeshGearWhineAnalysis))
        return value
