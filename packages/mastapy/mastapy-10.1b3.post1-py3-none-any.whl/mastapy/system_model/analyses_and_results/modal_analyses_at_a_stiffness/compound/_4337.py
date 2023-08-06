'''_4337.py

AssemblyCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model import _1977
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4214
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _4338, _4340, _4343, _4349,
    _4350, _4351, _4356, _4361,
    _4371, _4375, _4381, _4382,
    _4389, _4390, _4397, _4400,
    _4401, _4402, _4404, _4406,
    _4411, _4412, _4413, _4420,
    _4415, _4419, _4425, _4426,
    _4431, _4434, _4437, _4441,
    _4445, _4449, _4452, _4332
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'AssemblyCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundModalAnalysisAtAStiffness',)


class AssemblyCompoundModalAnalysisAtAStiffness(_4332.AbstractAssemblyCompoundModalAnalysisAtAStiffness):
    '''AssemblyCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1977.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1977.Assembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1977.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1977.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4214.AssemblyModalAnalysisAtAStiffness]':
        '''List[AssemblyModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4214.AssemblyModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4214.AssemblyModalAnalysisAtAStiffness]':
        '''List[AssemblyModalAnalysisAtAStiffness]: 'AssemblyModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtAStiffnessLoadCases, constructor.new(_4214.AssemblyModalAnalysisAtAStiffness))
        return value

    @property
    def bearings(self) -> 'List[_4338.BearingCompoundModalAnalysisAtAStiffness]':
        '''List[BearingCompoundModalAnalysisAtAStiffness]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4338.BearingCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def belt_drives(self) -> 'List[_4340.BeltDriveCompoundModalAnalysisAtAStiffness]':
        '''List[BeltDriveCompoundModalAnalysisAtAStiffness]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4340.BeltDriveCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4343.BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4343.BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def bolts(self) -> 'List[_4349.BoltCompoundModalAnalysisAtAStiffness]':
        '''List[BoltCompoundModalAnalysisAtAStiffness]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4349.BoltCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def bolted_joints(self) -> 'List[_4350.BoltedJointCompoundModalAnalysisAtAStiffness]':
        '''List[BoltedJointCompoundModalAnalysisAtAStiffness]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4350.BoltedJointCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def clutches(self) -> 'List[_4351.ClutchCompoundModalAnalysisAtAStiffness]':
        '''List[ClutchCompoundModalAnalysisAtAStiffness]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4351.ClutchCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def concept_couplings(self) -> 'List[_4356.ConceptCouplingCompoundModalAnalysisAtAStiffness]':
        '''List[ConceptCouplingCompoundModalAnalysisAtAStiffness]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4356.ConceptCouplingCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4361.ConceptGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[ConceptGearSetCompoundModalAnalysisAtAStiffness]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4361.ConceptGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def cv_ts(self) -> 'List[_4371.CVTCompoundModalAnalysisAtAStiffness]':
        '''List[CVTCompoundModalAnalysisAtAStiffness]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4371.CVTCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4375.CylindricalGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[CylindricalGearSetCompoundModalAnalysisAtAStiffness]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4375.CylindricalGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4381.FaceGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[FaceGearSetCompoundModalAnalysisAtAStiffness]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4381.FaceGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4382.FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness]':
        '''List[FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4382.FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4389.HypoidGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[HypoidGearSetCompoundModalAnalysisAtAStiffness]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4389.HypoidGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4390.ImportedFEComponentCompoundModalAnalysisAtAStiffness]':
        '''List[ImportedFEComponentCompoundModalAnalysisAtAStiffness]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4390.ImportedFEComponentCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4397.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4397.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4400.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4400.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def mass_discs(self) -> 'List[_4401.MassDiscCompoundModalAnalysisAtAStiffness]':
        '''List[MassDiscCompoundModalAnalysisAtAStiffness]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4401.MassDiscCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def measurement_components(self) -> 'List[_4402.MeasurementComponentCompoundModalAnalysisAtAStiffness]':
        '''List[MeasurementComponentCompoundModalAnalysisAtAStiffness]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4402.MeasurementComponentCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def oil_seals(self) -> 'List[_4404.OilSealCompoundModalAnalysisAtAStiffness]':
        '''List[OilSealCompoundModalAnalysisAtAStiffness]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4404.OilSealCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4406.PartToPartShearCouplingCompoundModalAnalysisAtAStiffness]':
        '''List[PartToPartShearCouplingCompoundModalAnalysisAtAStiffness]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4406.PartToPartShearCouplingCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def planet_carriers(self) -> 'List[_4411.PlanetCarrierCompoundModalAnalysisAtAStiffness]':
        '''List[PlanetCarrierCompoundModalAnalysisAtAStiffness]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4411.PlanetCarrierCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def point_loads(self) -> 'List[_4412.PointLoadCompoundModalAnalysisAtAStiffness]':
        '''List[PointLoadCompoundModalAnalysisAtAStiffness]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4412.PointLoadCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def power_loads(self) -> 'List[_4413.PowerLoadCompoundModalAnalysisAtAStiffness]':
        '''List[PowerLoadCompoundModalAnalysisAtAStiffness]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4413.PowerLoadCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4420.ShaftHubConnectionCompoundModalAnalysisAtAStiffness]':
        '''List[ShaftHubConnectionCompoundModalAnalysisAtAStiffness]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4420.ShaftHubConnectionCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4415.RollingRingAssemblyCompoundModalAnalysisAtAStiffness]':
        '''List[RollingRingAssemblyCompoundModalAnalysisAtAStiffness]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4415.RollingRingAssemblyCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def shafts(self) -> 'List[_4419.ShaftCompoundModalAnalysisAtAStiffness]':
        '''List[ShaftCompoundModalAnalysisAtAStiffness]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4419.ShaftCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4425.SpiralBevelGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[SpiralBevelGearSetCompoundModalAnalysisAtAStiffness]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4425.SpiralBevelGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def spring_dampers(self) -> 'List[_4426.SpringDamperCompoundModalAnalysisAtAStiffness]':
        '''List[SpringDamperCompoundModalAnalysisAtAStiffness]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4426.SpringDamperCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4431.StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4431.StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4434.StraightBevelGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[StraightBevelGearSetCompoundModalAnalysisAtAStiffness]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4434.StraightBevelGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def synchronisers(self) -> 'List[_4437.SynchroniserCompoundModalAnalysisAtAStiffness]':
        '''List[SynchroniserCompoundModalAnalysisAtAStiffness]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4437.SynchroniserCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def torque_converters(self) -> 'List[_4441.TorqueConverterCompoundModalAnalysisAtAStiffness]':
        '''List[TorqueConverterCompoundModalAnalysisAtAStiffness]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4441.TorqueConverterCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4445.UnbalancedMassCompoundModalAnalysisAtAStiffness]':
        '''List[UnbalancedMassCompoundModalAnalysisAtAStiffness]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4445.UnbalancedMassCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4449.WormGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[WormGearSetCompoundModalAnalysisAtAStiffness]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4449.WormGearSetCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4452.ZerolBevelGearSetCompoundModalAnalysisAtAStiffness]':
        '''List[ZerolBevelGearSetCompoundModalAnalysisAtAStiffness]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4452.ZerolBevelGearSetCompoundModalAnalysisAtAStiffness))
        return value
