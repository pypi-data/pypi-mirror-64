'''_4057.py

SpiralBevelGearMeshModalAnalysesAtSpeeds
'''


from mastapy.system_model.connections_and_sockets.gears import _1882
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6176
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3977
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MESH_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'SpiralBevelGearMeshModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearMeshModalAnalysesAtSpeeds',)


class SpiralBevelGearMeshModalAnalysesAtSpeeds(_3977.BevelGearMeshModalAnalysesAtSpeeds):
    '''SpiralBevelGearMeshModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_MESH_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearMeshModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1882.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1882.SpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6176.SpiralBevelGearMeshLoadCase':
        '''SpiralBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6176.SpiralBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
