'''_3465.py

AssemblyParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model import _1977
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6050
from mastapy.system_model.analyses_and_results.parametric_study_tools import (
    _3508, _3466, _3468, _3471,
    _3478, _3477, _3481, _3486,
    _3489, _3499, _3503, _3515,
    _3516, _3523, _3524, _3531,
    _3534, _3535, _3536, _3539,
    _3552, _3555, _3556, _3557,
    _3563, _3559, _3564, _3569,
    _3572, _3575, _3578, _3582,
    _3586, _3589, _3593, _3596,
    _3460
)
from mastapy.system_model.analyses_and_results.system_deflections import _2209
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'AssemblyParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyParametricStudyTool',)


class AssemblyParametricStudyTool(_3460.AbstractAssemblyParametricStudyTool):
    '''AssemblyParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1977.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1977.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6050.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6050.AssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def all_duty_cycle_results(self) -> 'List[_3508.DutyCycleResultsForAllComponents]':
        '''List[DutyCycleResultsForAllComponents]: 'AllDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AllDutyCycleResults, constructor.new(_3508.DutyCycleResultsForAllComponents))
        return value

    @property
    def bearings(self) -> 'List[_3466.BearingParametricStudyTool]':
        '''List[BearingParametricStudyTool]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3466.BearingParametricStudyTool))
        return value

    @property
    def belt_drives(self) -> 'List[_3468.BeltDriveParametricStudyTool]':
        '''List[BeltDriveParametricStudyTool]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3468.BeltDriveParametricStudyTool))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3471.BevelDifferentialGearSetParametricStudyTool]':
        '''List[BevelDifferentialGearSetParametricStudyTool]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3471.BevelDifferentialGearSetParametricStudyTool))
        return value

    @property
    def bolts(self) -> 'List[_3478.BoltParametricStudyTool]':
        '''List[BoltParametricStudyTool]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3478.BoltParametricStudyTool))
        return value

    @property
    def bolted_joints(self) -> 'List[_3477.BoltedJointParametricStudyTool]':
        '''List[BoltedJointParametricStudyTool]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3477.BoltedJointParametricStudyTool))
        return value

    @property
    def clutches(self) -> 'List[_3481.ClutchParametricStudyTool]':
        '''List[ClutchParametricStudyTool]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3481.ClutchParametricStudyTool))
        return value

    @property
    def concept_couplings(self) -> 'List[_3486.ConceptCouplingParametricStudyTool]':
        '''List[ConceptCouplingParametricStudyTool]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3486.ConceptCouplingParametricStudyTool))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3489.ConceptGearSetParametricStudyTool]':
        '''List[ConceptGearSetParametricStudyTool]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3489.ConceptGearSetParametricStudyTool))
        return value

    @property
    def cv_ts(self) -> 'List[_3499.CVTParametricStudyTool]':
        '''List[CVTParametricStudyTool]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3499.CVTParametricStudyTool))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3503.CylindricalGearSetParametricStudyTool]':
        '''List[CylindricalGearSetParametricStudyTool]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3503.CylindricalGearSetParametricStudyTool))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3515.FaceGearSetParametricStudyTool]':
        '''List[FaceGearSetParametricStudyTool]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3515.FaceGearSetParametricStudyTool))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3516.FlexiblePinAssemblyParametricStudyTool]':
        '''List[FlexiblePinAssemblyParametricStudyTool]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3516.FlexiblePinAssemblyParametricStudyTool))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3523.HypoidGearSetParametricStudyTool]':
        '''List[HypoidGearSetParametricStudyTool]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3523.HypoidGearSetParametricStudyTool))
        return value

    @property
    def imported_fe_components(self) -> 'List[_3524.ImportedFEComponentParametricStudyTool]':
        '''List[ImportedFEComponentParametricStudyTool]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_3524.ImportedFEComponentParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3531.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3531.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3534.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3534.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool))
        return value

    @property
    def mass_discs(self) -> 'List[_3535.MassDiscParametricStudyTool]':
        '''List[MassDiscParametricStudyTool]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3535.MassDiscParametricStudyTool))
        return value

    @property
    def measurement_components(self) -> 'List[_3536.MeasurementComponentParametricStudyTool]':
        '''List[MeasurementComponentParametricStudyTool]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3536.MeasurementComponentParametricStudyTool))
        return value

    @property
    def oil_seals(self) -> 'List[_3539.OilSealParametricStudyTool]':
        '''List[OilSealParametricStudyTool]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3539.OilSealParametricStudyTool))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3552.PartToPartShearCouplingParametricStudyTool]':
        '''List[PartToPartShearCouplingParametricStudyTool]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3552.PartToPartShearCouplingParametricStudyTool))
        return value

    @property
    def planet_carriers(self) -> 'List[_3555.PlanetCarrierParametricStudyTool]':
        '''List[PlanetCarrierParametricStudyTool]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3555.PlanetCarrierParametricStudyTool))
        return value

    @property
    def point_loads(self) -> 'List[_3556.PointLoadParametricStudyTool]':
        '''List[PointLoadParametricStudyTool]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3556.PointLoadParametricStudyTool))
        return value

    @property
    def power_loads(self) -> 'List[_3557.PowerLoadParametricStudyTool]':
        '''List[PowerLoadParametricStudyTool]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3557.PowerLoadParametricStudyTool))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3563.ShaftHubConnectionParametricStudyTool]':
        '''List[ShaftHubConnectionParametricStudyTool]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3563.ShaftHubConnectionParametricStudyTool))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3559.RollingRingAssemblyParametricStudyTool]':
        '''List[RollingRingAssemblyParametricStudyTool]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3559.RollingRingAssemblyParametricStudyTool))
        return value

    @property
    def shafts(self) -> 'List[_3564.ShaftParametricStudyTool]':
        '''List[ShaftParametricStudyTool]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3564.ShaftParametricStudyTool))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3569.SpiralBevelGearSetParametricStudyTool]':
        '''List[SpiralBevelGearSetParametricStudyTool]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3569.SpiralBevelGearSetParametricStudyTool))
        return value

    @property
    def spring_dampers(self) -> 'List[_3572.SpringDamperParametricStudyTool]':
        '''List[SpringDamperParametricStudyTool]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3572.SpringDamperParametricStudyTool))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3575.StraightBevelDiffGearSetParametricStudyTool]':
        '''List[StraightBevelDiffGearSetParametricStudyTool]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3575.StraightBevelDiffGearSetParametricStudyTool))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3578.StraightBevelGearSetParametricStudyTool]':
        '''List[StraightBevelGearSetParametricStudyTool]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3578.StraightBevelGearSetParametricStudyTool))
        return value

    @property
    def synchronisers(self) -> 'List[_3582.SynchroniserParametricStudyTool]':
        '''List[SynchroniserParametricStudyTool]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3582.SynchroniserParametricStudyTool))
        return value

    @property
    def torque_converters(self) -> 'List[_3586.TorqueConverterParametricStudyTool]':
        '''List[TorqueConverterParametricStudyTool]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3586.TorqueConverterParametricStudyTool))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3589.UnbalancedMassParametricStudyTool]':
        '''List[UnbalancedMassParametricStudyTool]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3589.UnbalancedMassParametricStudyTool))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3593.WormGearSetParametricStudyTool]':
        '''List[WormGearSetParametricStudyTool]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3593.WormGearSetParametricStudyTool))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3596.ZerolBevelGearSetParametricStudyTool]':
        '''List[ZerolBevelGearSetParametricStudyTool]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3596.ZerolBevelGearSetParametricStudyTool))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2209.AssemblySystemDeflection]':
        '''List[AssemblySystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2209.AssemblySystemDeflection))
        return value
