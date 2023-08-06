'''_6352.py

WormGearMeshAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1888
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6207
from mastapy.gears.rating.worm import _176
from mastapy.system_model.analyses_and_results.system_deflections import _2337
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6285
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'WormGearMeshAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshAdvancedSystemDeflection',)


class WormGearMeshAdvancedSystemDeflection(_6285.GearMeshAdvancedSystemDeflection):
    '''WormGearMeshAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1888.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1888.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6207.WormGearMeshLoadCase':
        '''WormGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6207.WormGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_176.WormGearMeshRating':
        '''WormGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_176.WormGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2337.WormGearMeshSystemDeflection]':
        '''List[WormGearMeshSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2337.WormGearMeshSystemDeflection))
        return value
