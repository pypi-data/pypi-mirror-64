'''_2273.py

KlingelnbergCycloPalloidConicalGearMeshSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.gears import _1877, _1878, _1879
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.power_flows import _3274, _3277, _3280
from mastapy.system_model.analyses_and_results.system_deflections import _2236
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'KlingelnbergCycloPalloidConicalGearMeshSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearMeshSystemDeflection',)


class KlingelnbergCycloPalloidConicalGearMeshSystemDeflection(_2236.ConicalGearMeshSystemDeflection):
    '''KlingelnbergCycloPalloidConicalGearMeshSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearMeshSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1877.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1877.KlingelnbergCycloPalloidConicalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_1878.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1878.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1878.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_1879.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1879.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1879.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def power_flow_results(self) -> '_3274.KlingelnbergCycloPalloidConicalGearMeshPowerFlow':
        '''KlingelnbergCycloPalloidConicalGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3274.KlingelnbergCycloPalloidConicalGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_power_flow(self) -> '_3277.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow':
        '''KlingelnbergCycloPalloidHypoidGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3277.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to KlingelnbergCycloPalloidHypoidGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3277.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_power_flow(self) -> '_3280.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3280.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3280.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
