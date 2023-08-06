'''_2337.py

WormGearMeshSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.gears import _1888
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6207
from mastapy.system_model.analyses_and_results.power_flows import _3332
from mastapy.gears.rating.worm import _176
from mastapy.system_model.analyses_and_results.system_deflections import _2264
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'WormGearMeshSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshSystemDeflection',)


class WormGearMeshSystemDeflection(_2264.GearMeshSystemDeflection):
    '''WormGearMeshSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshSystemDeflection.TYPE'):
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
    def power_flow_results(self) -> '_3332.WormGearMeshPowerFlow':
        '''WormGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3332.WormGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def rating(self) -> '_176.WormGearMeshRating':
        '''WormGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_176.WormGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_176.WormGearMeshRating':
        '''WormGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_176.WormGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
