'''_4011.py

FaceGearMeshModalAnalysesAtSpeeds
'''


from mastapy.system_model.connections_and_sockets.gears import _1870
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6111
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4015
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'FaceGearMeshModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshModalAnalysesAtSpeeds',)


class FaceGearMeshModalAnalysesAtSpeeds(_4015.GearMeshModalAnalysesAtSpeeds):
    '''FaceGearMeshModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1870.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1870.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6111.FaceGearMeshLoadCase':
        '''FaceGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6111.FaceGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
