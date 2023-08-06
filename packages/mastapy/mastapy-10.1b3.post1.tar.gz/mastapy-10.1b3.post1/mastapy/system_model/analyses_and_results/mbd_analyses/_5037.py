'''_5037.py

KlingelnbergCycloPalloidSpiralBevelGearMeshMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1879
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6143
from mastapy.system_model.analyses_and_results.mbd_analyses import _5031
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearMeshMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearMeshMultiBodyDynamicsAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearMeshMultiBodyDynamicsAnalysis(_5031.KlingelnbergCycloPalloidConicalGearMeshMultiBodyDynamicsAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearMeshMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearMeshMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1879.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1879.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6143.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6143.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
