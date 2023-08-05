'''_5476.py

SingleMeshWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses import (
    _5230, _5278, _5279, _5280,
    _5281, _5282, _5283, _5284,
    _5285, _5286, _5287, _5288,
    _5297, _5302, _5327, _5341,
    _5366
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.analysis_cases import _6473
from mastapy._internal.python_net import python_net_import

_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'SingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SingleMeshWhineAnalysis',)


class SingleMeshWhineAnalysis(_6473.StaticLoadAnalysisCase):
    '''SingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def excitation_detail(self) -> '_5230.AbstractPeriodicExcitationDetail':
        '''AbstractPeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5230.AbstractPeriodicExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_periodic_excitation_detail(self) -> '_5278.ElectricMachinePeriodicExcitationDetail':
        '''ElectricMachinePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5278.ElectricMachinePeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachinePeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5278.ElectricMachinePeriodicExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_x_force_periodic_excitation_detail(self) -> '_5279.ElectricMachineRotorXForcePeriodicExcitationDetail':
        '''ElectricMachineRotorXForcePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5279.ElectricMachineRotorXForcePeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorXForcePeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5279.ElectricMachineRotorXForcePeriodicExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_x_moment_periodic_excitation_detail(self) -> '_5280.ElectricMachineRotorXMomentPeriodicExcitationDetail':
        '''ElectricMachineRotorXMomentPeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5280.ElectricMachineRotorXMomentPeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorXMomentPeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5280.ElectricMachineRotorXMomentPeriodicExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_y_force_periodic_excitation_detail(self) -> '_5281.ElectricMachineRotorYForcePeriodicExcitationDetail':
        '''ElectricMachineRotorYForcePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5281.ElectricMachineRotorYForcePeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorYForcePeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5281.ElectricMachineRotorYForcePeriodicExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_y_moment_periodic_excitation_detail(self) -> '_5282.ElectricMachineRotorYMomentPeriodicExcitationDetail':
        '''ElectricMachineRotorYMomentPeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5282.ElectricMachineRotorYMomentPeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorYMomentPeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5282.ElectricMachineRotorYMomentPeriodicExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_rotor_z_force_periodic_excitation_detail(self) -> '_5283.ElectricMachineRotorZForcePeriodicExcitationDetail':
        '''ElectricMachineRotorZForcePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5283.ElectricMachineRotorZForcePeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineRotorZForcePeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5283.ElectricMachineRotorZForcePeriodicExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_stator_tooth_axial_loads_excitation_detail(self) -> '_5284.ElectricMachineStatorToothAxialLoadsExcitationDetail':
        '''ElectricMachineStatorToothAxialLoadsExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5284.ElectricMachineStatorToothAxialLoadsExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineStatorToothAxialLoadsExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5284.ElectricMachineStatorToothAxialLoadsExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_stator_tooth_loads_excitation_detail(self) -> '_5285.ElectricMachineStatorToothLoadsExcitationDetail':
        '''ElectricMachineStatorToothLoadsExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5285.ElectricMachineStatorToothLoadsExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineStatorToothLoadsExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5285.ElectricMachineStatorToothLoadsExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_stator_tooth_radial_loads_excitation_detail(self) -> '_5286.ElectricMachineStatorToothRadialLoadsExcitationDetail':
        '''ElectricMachineStatorToothRadialLoadsExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5286.ElectricMachineStatorToothRadialLoadsExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineStatorToothRadialLoadsExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5286.ElectricMachineStatorToothRadialLoadsExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_stator_tooth_tangential_loads_excitation_detail(self) -> '_5287.ElectricMachineStatorToothTangentialLoadsExcitationDetail':
        '''ElectricMachineStatorToothTangentialLoadsExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5287.ElectricMachineStatorToothTangentialLoadsExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineStatorToothTangentialLoadsExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5287.ElectricMachineStatorToothTangentialLoadsExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_electric_machine_torque_ripple_periodic_excitation_detail(self) -> '_5288.ElectricMachineTorqueRipplePeriodicExcitationDetail':
        '''ElectricMachineTorqueRipplePeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5288.ElectricMachineTorqueRipplePeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to ElectricMachineTorqueRipplePeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5288.ElectricMachineTorqueRipplePeriodicExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_gear_mesh_te_excitation_detail(self) -> '_5297.GearMeshTEExcitationDetail':
        '''GearMeshTEExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5297.GearMeshTEExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to GearMeshTEExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5297.GearMeshTEExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_general_periodic_excitation_detail(self) -> '_5302.GeneralPeriodicExcitationDetail':
        '''GeneralPeriodicExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5302.GeneralPeriodicExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to GeneralPeriodicExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5302.GeneralPeriodicExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_periodic_excitation_with_reference_shaft(self) -> '_5327.PeriodicExcitationWithReferenceShaft':
        '''PeriodicExcitationWithReferenceShaft: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5327.PeriodicExcitationWithReferenceShaft.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to PeriodicExcitationWithReferenceShaft. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5327.PeriodicExcitationWithReferenceShaft)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_single_node_periodic_excitation_with_reference_shaft(self) -> '_5341.SingleNodePeriodicExcitationWithReferenceShaft':
        '''SingleNodePeriodicExcitationWithReferenceShaft: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5341.SingleNodePeriodicExcitationWithReferenceShaft.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to SingleNodePeriodicExcitationWithReferenceShaft. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5341.SingleNodePeriodicExcitationWithReferenceShaft)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None

    @property
    def excitation_detail_of_type_unbalanced_mass_excitation_detail(self) -> '_5366.UnbalancedMassExcitationDetail':
        '''UnbalancedMassExcitationDetail: 'ExcitationDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5366.UnbalancedMassExcitationDetail.TYPE not in self.wrapped.ExcitationDetail.__class__.__mro__:
            raise CastException('Failed to cast excitation_detail to UnbalancedMassExcitationDetail. Expected: {}.'.format(self.wrapped.ExcitationDetail.__class__.__qualname__))

        return constructor.new(_5366.UnbalancedMassExcitationDetail)(self.wrapped.ExcitationDetail) if self.wrapped.ExcitationDetail else None
