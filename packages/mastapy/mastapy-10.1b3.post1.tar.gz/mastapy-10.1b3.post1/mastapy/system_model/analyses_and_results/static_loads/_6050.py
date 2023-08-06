'''_6050.py

AssemblyLoadCase
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _1977
from mastapy.system_model.analyses_and_results.static_loads import (
    _6051, _6053, _6056, _6063,
    _6062, _6066, _6071, _6074,
    _6086, _6092, _6112, _6113,
    _6132, _6133, _6141, _6144,
    _6145, _6146, _6150, _6155,
    _6159, _6162, _6163, _6170,
    _6166, _6171, _6177, _6180,
    _6184, _6187, _6191, _6197,
    _6204, _6208, _6211, _6044,
    _6064, _6117, _6043
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'AssemblyLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyLoadCase',)


class AssemblyLoadCase(_6043.AbstractAssemblyLoadCase):
    '''AssemblyLoadCase

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def volume_of_oil_in_sump(self) -> 'float':
        '''float: 'VolumeOfOilInSump' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.VolumeOfOilInSump

    @property
    def assembly_design(self) -> '_1977.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1977.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bearings(self) -> 'List[_6051.BearingLoadCase]':
        '''List[BearingLoadCase]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6051.BearingLoadCase))
        return value

    @property
    def belt_drives(self) -> 'List[_6053.BeltDriveLoadCase]':
        '''List[BeltDriveLoadCase]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6053.BeltDriveLoadCase))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6056.BevelDifferentialGearSetLoadCase]':
        '''List[BevelDifferentialGearSetLoadCase]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6056.BevelDifferentialGearSetLoadCase))
        return value

    @property
    def bolts(self) -> 'List[_6063.BoltLoadCase]':
        '''List[BoltLoadCase]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6063.BoltLoadCase))
        return value

    @property
    def bolted_joints(self) -> 'List[_6062.BoltedJointLoadCase]':
        '''List[BoltedJointLoadCase]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6062.BoltedJointLoadCase))
        return value

    @property
    def clutches(self) -> 'List[_6066.ClutchLoadCase]':
        '''List[ClutchLoadCase]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6066.ClutchLoadCase))
        return value

    @property
    def concept_couplings(self) -> 'List[_6071.ConceptCouplingLoadCase]':
        '''List[ConceptCouplingLoadCase]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6071.ConceptCouplingLoadCase))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6074.ConceptGearSetLoadCase]':
        '''List[ConceptGearSetLoadCase]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6074.ConceptGearSetLoadCase))
        return value

    @property
    def cv_ts(self) -> 'List[_6086.CVTLoadCase]':
        '''List[CVTLoadCase]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6086.CVTLoadCase))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6092.CylindricalGearSetLoadCase]':
        '''List[CylindricalGearSetLoadCase]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6092.CylindricalGearSetLoadCase))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6112.FaceGearSetLoadCase]':
        '''List[FaceGearSetLoadCase]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6112.FaceGearSetLoadCase))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6113.FlexiblePinAssemblyLoadCase]':
        '''List[FlexiblePinAssemblyLoadCase]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6113.FlexiblePinAssemblyLoadCase))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6132.HypoidGearSetLoadCase]':
        '''List[HypoidGearSetLoadCase]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6132.HypoidGearSetLoadCase))
        return value

    @property
    def imported_fe_components(self) -> 'List[_6133.ImportedFEComponentLoadCase]':
        '''List[ImportedFEComponentLoadCase]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_6133.ImportedFEComponentLoadCase))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6141.KlingelnbergCycloPalloidHypoidGearSetLoadCase]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetLoadCase]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6141.KlingelnbergCycloPalloidHypoidGearSetLoadCase))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6144.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6144.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase))
        return value

    @property
    def mass_discs(self) -> 'List[_6145.MassDiscLoadCase]':
        '''List[MassDiscLoadCase]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6145.MassDiscLoadCase))
        return value

    @property
    def measurement_components(self) -> 'List[_6146.MeasurementComponentLoadCase]':
        '''List[MeasurementComponentLoadCase]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6146.MeasurementComponentLoadCase))
        return value

    @property
    def oil_seals(self) -> 'List[_6150.OilSealLoadCase]':
        '''List[OilSealLoadCase]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6150.OilSealLoadCase))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6155.PartToPartShearCouplingLoadCase]':
        '''List[PartToPartShearCouplingLoadCase]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6155.PartToPartShearCouplingLoadCase))
        return value

    @property
    def planet_carriers(self) -> 'List[_6159.PlanetCarrierLoadCase]':
        '''List[PlanetCarrierLoadCase]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6159.PlanetCarrierLoadCase))
        return value

    @property
    def point_loads(self) -> 'List[_6162.PointLoadLoadCase]':
        '''List[PointLoadLoadCase]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6162.PointLoadLoadCase))
        return value

    @property
    def power_loads(self) -> 'List[_6163.PowerLoadLoadCase]':
        '''List[PowerLoadLoadCase]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6163.PowerLoadLoadCase))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6170.ShaftHubConnectionLoadCase]':
        '''List[ShaftHubConnectionLoadCase]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6170.ShaftHubConnectionLoadCase))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6166.RollingRingAssemblyLoadCase]':
        '''List[RollingRingAssemblyLoadCase]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6166.RollingRingAssemblyLoadCase))
        return value

    @property
    def shafts(self) -> 'List[_6171.ShaftLoadCase]':
        '''List[ShaftLoadCase]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6171.ShaftLoadCase))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6177.SpiralBevelGearSetLoadCase]':
        '''List[SpiralBevelGearSetLoadCase]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6177.SpiralBevelGearSetLoadCase))
        return value

    @property
    def spring_dampers(self) -> 'List[_6180.SpringDamperLoadCase]':
        '''List[SpringDamperLoadCase]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6180.SpringDamperLoadCase))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6184.StraightBevelDiffGearSetLoadCase]':
        '''List[StraightBevelDiffGearSetLoadCase]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6184.StraightBevelDiffGearSetLoadCase))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6187.StraightBevelGearSetLoadCase]':
        '''List[StraightBevelGearSetLoadCase]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6187.StraightBevelGearSetLoadCase))
        return value

    @property
    def synchronisers(self) -> 'List[_6191.SynchroniserLoadCase]':
        '''List[SynchroniserLoadCase]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6191.SynchroniserLoadCase))
        return value

    @property
    def torque_converters(self) -> 'List[_6197.TorqueConverterLoadCase]':
        '''List[TorqueConverterLoadCase]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6197.TorqueConverterLoadCase))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6204.UnbalancedMassLoadCase]':
        '''List[UnbalancedMassLoadCase]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6204.UnbalancedMassLoadCase))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6208.WormGearSetLoadCase]':
        '''List[WormGearSetLoadCase]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6208.WormGearSetLoadCase))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6211.ZerolBevelGearSetLoadCase]':
        '''List[ZerolBevelGearSetLoadCase]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6211.ZerolBevelGearSetLoadCase))
        return value

    @property
    def shafts_and_housings(self) -> 'List[_6044.AbstractShaftOrHousingLoadCase]':
        '''List[AbstractShaftOrHousingLoadCase]: 'ShaftsAndHousings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftsAndHousings, constructor.new(_6044.AbstractShaftOrHousingLoadCase))
        return value

    @property
    def clutch_connections(self) -> 'List[_6064.ClutchConnectionLoadCase]':
        '''List[ClutchConnectionLoadCase]: 'ClutchConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ClutchConnections, constructor.new(_6064.ClutchConnectionLoadCase))
        return value

    @property
    def gear_meshes(self) -> 'List[_6117.GearMeshLoadCase]':
        '''List[GearMeshLoadCase]: 'GearMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearMeshes, constructor.new(_6117.GearMeshLoadCase))
        return value
