'''_5858.py

KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1878
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6140
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5855
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis',)


class KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis(_5855.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1878.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1878.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6140.KlingelnbergCycloPalloidHypoidGearMeshLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6140.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
