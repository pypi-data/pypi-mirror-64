'''_2272.py

InterMountableComponentConnectionSystemDeflection
'''


from mastapy.system_model.connections_and_sockets import (
    _1843, _1830, _1835, _1850
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _1858, _1860, _1862, _1864,
    _1866, _1868, _1870, _1872,
    _1874, _1877, _1878, _1879,
    _1882, _1884, _1886, _1888,
    _1890
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1892, _1894, _1896, _1898,
    _1900, _1902
)
from mastapy.system_model.analyses_and_results.power_flows import (
    _3273, _3215, _3220, _3222,
    _3227, _3232, _3237, _3240,
    _3243, _3248, _3251, _3255,
    _3261, _3265, _3269, _3274,
    _3277, _3280, _3288, _3300,
    _3307, _3310, _3313, _3316,
    _3326, _3332, _3335
)
from mastapy.system_model.analyses_and_results.system_deflections import _2239
from mastapy._internal.python_net import python_net_import

_INTER_MOUNTABLE_COMPONENT_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'InterMountableComponentConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('InterMountableComponentConnectionSystemDeflection',)


class InterMountableComponentConnectionSystemDeflection(_2239.ConnectionSystemDeflection):
    '''InterMountableComponentConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _INTER_MOUNTABLE_COMPONENT_CONNECTION_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'InterMountableComponentConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1843.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1843.InterMountableComponentConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_belt_connection(self) -> '_1830.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1830.BeltConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BeltConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1830.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cvt_belt_connection(self) -> '_1835.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1835.CVTBeltConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CVTBeltConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1835.CVTBeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_rolling_ring_connection(self) -> '_1850.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1850.RollingRingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to RollingRingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1850.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_agma_gleason_conical_gear_mesh(self) -> '_1858.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1858.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1858.AGMAGleasonConicalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_differential_gear_mesh(self) -> '_1860.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1860.BevelDifferentialGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1860.BevelDifferentialGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_gear_mesh(self) -> '_1862.BevelGearMesh':
        '''BevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1862.BevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1862.BevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_concept_gear_mesh(self) -> '_1864.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1864.ConceptGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConceptGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1864.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_conical_gear_mesh(self) -> '_1866.ConicalGearMesh':
        '''ConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1866.ConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1866.ConicalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cylindrical_gear_mesh(self) -> '_1868.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1868.CylindricalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1868.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_face_gear_mesh(self) -> '_1870.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1870.FaceGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to FaceGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1870.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_gear_mesh(self) -> '_1872.GearMesh':
        '''GearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1872.GearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to GearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1872.GearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_hypoid_gear_mesh(self) -> '_1874.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1874.HypoidGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to HypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1874.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_1877.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1877.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

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
    def connection_design_of_type_spiral_bevel_gear_mesh(self) -> '_1882.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1882.SpiralBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1882.SpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_1884.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1884.StraightBevelDiffGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1884.StraightBevelDiffGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_gear_mesh(self) -> '_1886.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1886.StraightBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1886.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_worm_gear_mesh(self) -> '_1888.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1888.WormGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to WormGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1888.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_zerol_bevel_gear_mesh(self) -> '_1890.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1890.ZerolBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1890.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_clutch_connection(self) -> '_1892.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1892.ClutchConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ClutchConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1892.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_concept_coupling_connection(self) -> '_1894.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1894.ConceptCouplingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1894.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_coupling_connection(self) -> '_1896.CouplingConnection':
        '''CouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1896.CouplingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1896.CouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_part_to_part_shear_coupling_connection(self) -> '_1898.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1898.PartToPartShearCouplingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1898.PartToPartShearCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spring_damper_connection(self) -> '_1900.SpringDamperConnection':
        '''SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1900.SpringDamperConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to SpringDamperConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1900.SpringDamperConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_torque_converter_connection(self) -> '_1902.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1902.TorqueConverterConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1902.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def power_flow_results(self) -> '_3273.InterMountableComponentConnectionPowerFlow':
        '''InterMountableComponentConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3273.InterMountableComponentConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_agma_gleason_conical_gear_mesh_power_flow(self) -> '_3215.AGMAGleasonConicalGearMeshPowerFlow':
        '''AGMAGleasonConicalGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3215.AGMAGleasonConicalGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to AGMAGleasonConicalGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3215.AGMAGleasonConicalGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_belt_connection_power_flow(self) -> '_3220.BeltConnectionPowerFlow':
        '''BeltConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3220.BeltConnectionPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to BeltConnectionPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3220.BeltConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_bevel_differential_gear_mesh_power_flow(self) -> '_3222.BevelDifferentialGearMeshPowerFlow':
        '''BevelDifferentialGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3222.BevelDifferentialGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to BevelDifferentialGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3222.BevelDifferentialGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_bevel_gear_mesh_power_flow(self) -> '_3227.BevelGearMeshPowerFlow':
        '''BevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3227.BevelGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to BevelGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3227.BevelGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_clutch_connection_power_flow(self) -> '_3232.ClutchConnectionPowerFlow':
        '''ClutchConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3232.ClutchConnectionPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to ClutchConnectionPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3232.ClutchConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_concept_coupling_connection_power_flow(self) -> '_3237.ConceptCouplingConnectionPowerFlow':
        '''ConceptCouplingConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3237.ConceptCouplingConnectionPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to ConceptCouplingConnectionPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3237.ConceptCouplingConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_concept_gear_mesh_power_flow(self) -> '_3240.ConceptGearMeshPowerFlow':
        '''ConceptGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3240.ConceptGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to ConceptGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3240.ConceptGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_conical_gear_mesh_power_flow(self) -> '_3243.ConicalGearMeshPowerFlow':
        '''ConicalGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3243.ConicalGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to ConicalGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3243.ConicalGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_coupling_connection_power_flow(self) -> '_3248.CouplingConnectionPowerFlow':
        '''CouplingConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3248.CouplingConnectionPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to CouplingConnectionPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3248.CouplingConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_cvt_belt_connection_power_flow(self) -> '_3251.CVTBeltConnectionPowerFlow':
        '''CVTBeltConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3251.CVTBeltConnectionPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to CVTBeltConnectionPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3251.CVTBeltConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_cylindrical_gear_mesh_power_flow(self) -> '_3255.CylindricalGearMeshPowerFlow':
        '''CylindricalGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3255.CylindricalGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to CylindricalGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3255.CylindricalGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_face_gear_mesh_power_flow(self) -> '_3261.FaceGearMeshPowerFlow':
        '''FaceGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3261.FaceGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to FaceGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3261.FaceGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_gear_mesh_power_flow(self) -> '_3265.GearMeshPowerFlow':
        '''GearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3265.GearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to GearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3265.GearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_hypoid_gear_mesh_power_flow(self) -> '_3269.HypoidGearMeshPowerFlow':
        '''HypoidGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3269.HypoidGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to HypoidGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3269.HypoidGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh_power_flow(self) -> '_3274.KlingelnbergCycloPalloidConicalGearMeshPowerFlow':
        '''KlingelnbergCycloPalloidConicalGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3274.KlingelnbergCycloPalloidConicalGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to KlingelnbergCycloPalloidConicalGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

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

    @property
    def power_flow_results_of_type_part_to_part_shear_coupling_connection_power_flow(self) -> '_3288.PartToPartShearCouplingConnectionPowerFlow':
        '''PartToPartShearCouplingConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3288.PartToPartShearCouplingConnectionPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to PartToPartShearCouplingConnectionPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3288.PartToPartShearCouplingConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_rolling_ring_connection_power_flow(self) -> '_3300.RollingRingConnectionPowerFlow':
        '''RollingRingConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3300.RollingRingConnectionPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to RollingRingConnectionPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3300.RollingRingConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_spiral_bevel_gear_mesh_power_flow(self) -> '_3307.SpiralBevelGearMeshPowerFlow':
        '''SpiralBevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3307.SpiralBevelGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to SpiralBevelGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3307.SpiralBevelGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_spring_damper_connection_power_flow(self) -> '_3310.SpringDamperConnectionPowerFlow':
        '''SpringDamperConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3310.SpringDamperConnectionPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to SpringDamperConnectionPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3310.SpringDamperConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_straight_bevel_diff_gear_mesh_power_flow(self) -> '_3313.StraightBevelDiffGearMeshPowerFlow':
        '''StraightBevelDiffGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3313.StraightBevelDiffGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to StraightBevelDiffGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3313.StraightBevelDiffGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_straight_bevel_gear_mesh_power_flow(self) -> '_3316.StraightBevelGearMeshPowerFlow':
        '''StraightBevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3316.StraightBevelGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to StraightBevelGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3316.StraightBevelGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_torque_converter_connection_power_flow(self) -> '_3326.TorqueConverterConnectionPowerFlow':
        '''TorqueConverterConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3326.TorqueConverterConnectionPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to TorqueConverterConnectionPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3326.TorqueConverterConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_worm_gear_mesh_power_flow(self) -> '_3332.WormGearMeshPowerFlow':
        '''WormGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3332.WormGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to WormGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3332.WormGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_zerol_bevel_gear_mesh_power_flow(self) -> '_3335.ZerolBevelGearMeshPowerFlow':
        '''ZerolBevelGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3335.ZerolBevelGearMeshPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to ZerolBevelGearMeshPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3335.ZerolBevelGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
