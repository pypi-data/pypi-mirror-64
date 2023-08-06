'''_5317.py

GearMeshTEExcitationDetail
'''


from mastapy.system_model.analyses_and_results.system_deflections import (
    _2264, _2206, _2213, _2218,
    _2232, _2236, _2247, _2248,
    _2249, _2260, _2268, _2273,
    _2276, _2279, _2308, _2314,
    _2317, _2337, _2340
)
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6194
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5273, _5250
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_TE_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'GearMeshTEExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshTEExcitationDetail',)


class GearMeshTEExcitationDetail(_5250.AbstractPeriodicExcitationDetail):
    '''GearMeshTEExcitationDetail

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_TE_EXCITATION_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshTEExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_mesh(self) -> '_2264.GearMeshSystemDeflection':
        '''GearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2264.GearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_agma_gleason_conical_gear_mesh_system_deflection(self) -> '_2206.AGMAGleasonConicalGearMeshSystemDeflection':
        '''AGMAGleasonConicalGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2206.AGMAGleasonConicalGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to AGMAGleasonConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2206.AGMAGleasonConicalGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_bevel_differential_gear_mesh_system_deflection(self) -> '_2213.BevelDifferentialGearMeshSystemDeflection':
        '''BevelDifferentialGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2213.BevelDifferentialGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to BevelDifferentialGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2213.BevelDifferentialGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_bevel_gear_mesh_system_deflection(self) -> '_2218.BevelGearMeshSystemDeflection':
        '''BevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2218.BevelGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to BevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2218.BevelGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_concept_gear_mesh_system_deflection(self) -> '_2232.ConceptGearMeshSystemDeflection':
        '''ConceptGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2232.ConceptGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to ConceptGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2232.ConceptGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_conical_gear_mesh_system_deflection(self) -> '_2236.ConicalGearMeshSystemDeflection':
        '''ConicalGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2236.ConicalGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to ConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2236.ConicalGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_cylindrical_gear_mesh_system_deflection(self) -> '_2247.CylindricalGearMeshSystemDeflection':
        '''CylindricalGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2247.CylindricalGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to CylindricalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2247.CylindricalGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_cylindrical_gear_mesh_system_deflection_timestep(self) -> '_2248.CylindricalGearMeshSystemDeflectionTimestep':
        '''CylindricalGearMeshSystemDeflectionTimestep: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2248.CylindricalGearMeshSystemDeflectionTimestep.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to CylindricalGearMeshSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2248.CylindricalGearMeshSystemDeflectionTimestep)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_cylindrical_gear_mesh_system_deflection_with_ltca_results(self) -> '_2249.CylindricalGearMeshSystemDeflectionWithLTCAResults':
        '''CylindricalGearMeshSystemDeflectionWithLTCAResults: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2249.CylindricalGearMeshSystemDeflectionWithLTCAResults.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to CylindricalGearMeshSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2249.CylindricalGearMeshSystemDeflectionWithLTCAResults)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_face_gear_mesh_system_deflection(self) -> '_2260.FaceGearMeshSystemDeflection':
        '''FaceGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.FaceGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to FaceGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2260.FaceGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_hypoid_gear_mesh_system_deflection(self) -> '_2268.HypoidGearMeshSystemDeflection':
        '''HypoidGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2268.HypoidGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to HypoidGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2268.HypoidGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh_system_deflection(self) -> '_2273.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidConicalGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2273.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to KlingelnbergCycloPalloidConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2273.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(self) -> '_2276.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2276.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2276.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(self) -> '_2279.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2279.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2279.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_spiral_bevel_gear_mesh_system_deflection(self) -> '_2308.SpiralBevelGearMeshSystemDeflection':
        '''SpiralBevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2308.SpiralBevelGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to SpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2308.SpiralBevelGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_straight_bevel_diff_gear_mesh_system_deflection(self) -> '_2314.StraightBevelDiffGearMeshSystemDeflection':
        '''StraightBevelDiffGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2314.StraightBevelDiffGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to StraightBevelDiffGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2314.StraightBevelDiffGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_straight_bevel_gear_mesh_system_deflection(self) -> '_2317.StraightBevelGearMeshSystemDeflection':
        '''StraightBevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2317.StraightBevelGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to StraightBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2317.StraightBevelGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_worm_gear_mesh_system_deflection(self) -> '_2337.WormGearMeshSystemDeflection':
        '''WormGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2337.WormGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to WormGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2337.WormGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    @property
    def gear_mesh_of_type_zerol_bevel_gear_mesh_system_deflection(self) -> '_2340.ZerolBevelGearMeshSystemDeflection':
        '''ZerolBevelGearMeshSystemDeflection: 'GearMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2340.ZerolBevelGearMeshSystemDeflection.TYPE not in self.wrapped.GearMesh.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh to ZerolBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.GearMesh.__class__.__qualname__))

        return constructor.new(_2340.ZerolBevelGearMeshSystemDeflection)(self.wrapped.GearMesh) if self.wrapped.GearMesh else None

    def get_compliance_and_force_data(self, excitation_type: '_6194.TEExcitationType') -> '_5273.ComplianceAndForceData':
        ''' 'GetComplianceAndForceData' is the original name of this method.

        Args:
            excitation_type (mastapy.system_model.analyses_and_results.static_loads.TEExcitationType)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.ComplianceAndForceData
        '''

        excitation_type = conversion.mp_to_pn_enum(excitation_type)
        method_result = self.wrapped.GetComplianceAndForceData(excitation_type)
        return constructor.new(_5273.ComplianceAndForceData)(method_result) if method_result else None
