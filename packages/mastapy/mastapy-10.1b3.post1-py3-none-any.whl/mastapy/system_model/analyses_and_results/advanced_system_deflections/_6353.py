﻿'''_6353.py

WormGearSetAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2088
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6208
from mastapy.gears.rating.worm import _179
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6351, _6352, _6286
from mastapy.system_model.analyses_and_results.system_deflections import _2338
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'WormGearSetAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetAdvancedSystemDeflection',)


class WormGearSetAdvancedSystemDeflection(_6286.GearSetAdvancedSystemDeflection):
    '''WormGearSetAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2088.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2088.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6208.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6208.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_179.WormGearSetRating':
        '''WormGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_179.WormGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_179.WormGearSetRating':
        '''WormGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_179.WormGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def worm_gears_advanced_system_deflection(self) -> 'List[_6351.WormGearAdvancedSystemDeflection]':
        '''List[WormGearAdvancedSystemDeflection]: 'WormGearsAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsAdvancedSystemDeflection, constructor.new(_6351.WormGearAdvancedSystemDeflection))
        return value

    @property
    def worm_meshes_advanced_system_deflection(self) -> 'List[_6352.WormGearMeshAdvancedSystemDeflection]':
        '''List[WormGearMeshAdvancedSystemDeflection]: 'WormMeshesAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesAdvancedSystemDeflection, constructor.new(_6352.WormGearMeshAdvancedSystemDeflection))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2338.WormGearSetSystemDeflection]':
        '''List[WormGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2338.WormGearSetSystemDeflection))
        return value
