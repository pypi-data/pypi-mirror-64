'''_5096.py

WormGearMeshMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1888
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6207
from mastapy.system_model.analyses_and_results.mbd_analyses import _5017
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'WormGearMeshMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshMultiBodyDynamicsAnalysis',)


class WormGearMeshMultiBodyDynamicsAnalysis(_5017.GearMeshMultiBodyDynamicsAnalysis):
    '''WormGearMeshMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshMultiBodyDynamicsAnalysis.TYPE'):
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
