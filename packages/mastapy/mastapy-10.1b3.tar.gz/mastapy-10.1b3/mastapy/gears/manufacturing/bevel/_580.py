'''_580.py

PinionConcave
'''


from mastapy.gears.manufacturing.bevel import (
    _583, _578, _579, _581,
    _584, _585, _586
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel.basic_machine_settings import _600
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PINION_CONCAVE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'PinionConcave')


__docformat__ = 'restructuredtext en'
__all__ = ('PinionConcave',)


class PinionConcave(_0.APIBase):
    '''PinionConcave

    This is a mastapy class.
    '''

    TYPE = _PINION_CONCAVE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PinionConcave.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def pinion_cutter_parameters_concave(self) -> '_583.PinionFinishMachineSettings':
        '''PinionFinishMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_583.PinionFinishMachineSettings)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_bevel_generating_modified_roll_machine_settings(self) -> '_578.PinionBevelGeneratingModifiedRollMachineSettings':
        '''PinionBevelGeneratingModifiedRollMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _578.PinionBevelGeneratingModifiedRollMachineSettings.TYPE not in self.wrapped.PinionCutterParametersConcave.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionBevelGeneratingModifiedRollMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new(_578.PinionBevelGeneratingModifiedRollMachineSettings)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_bevel_generating_tilt_machine_settings(self) -> '_579.PinionBevelGeneratingTiltMachineSettings':
        '''PinionBevelGeneratingTiltMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _579.PinionBevelGeneratingTiltMachineSettings.TYPE not in self.wrapped.PinionCutterParametersConcave.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionBevelGeneratingTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new(_579.PinionBevelGeneratingTiltMachineSettings)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_conical_machine_settings_specified(self) -> '_581.PinionConicalMachineSettingsSpecified':
        '''PinionConicalMachineSettingsSpecified: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _581.PinionConicalMachineSettingsSpecified.TYPE not in self.wrapped.PinionCutterParametersConcave.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionConicalMachineSettingsSpecified. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new(_581.PinionConicalMachineSettingsSpecified)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_hypoid_formate_tilt_machine_settings(self) -> '_584.PinionHypoidFormateTiltMachineSettings':
        '''PinionHypoidFormateTiltMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _584.PinionHypoidFormateTiltMachineSettings.TYPE not in self.wrapped.PinionCutterParametersConcave.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionHypoidFormateTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new(_584.PinionHypoidFormateTiltMachineSettings)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_hypoid_generating_tilt_machine_settings(self) -> '_585.PinionHypoidGeneratingTiltMachineSettings':
        '''PinionHypoidGeneratingTiltMachineSettings: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _585.PinionHypoidGeneratingTiltMachineSettings.TYPE not in self.wrapped.PinionCutterParametersConcave.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionHypoidGeneratingTiltMachineSettings. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new(_585.PinionHypoidGeneratingTiltMachineSettings)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_cutter_parameters_concave_of_type_pinion_machine_settings_smt(self) -> '_586.PinionMachineSettingsSMT':
        '''PinionMachineSettingsSMT: 'PinionCutterParametersConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _586.PinionMachineSettingsSMT.TYPE not in self.wrapped.PinionCutterParametersConcave.__class__.__mro__:
            raise CastException('Failed to cast pinion_cutter_parameters_concave to PinionMachineSettingsSMT. Expected: {}.'.format(self.wrapped.PinionCutterParametersConcave.__class__.__qualname__))

        return constructor.new(_586.PinionMachineSettingsSMT)(self.wrapped.PinionCutterParametersConcave) if self.wrapped.PinionCutterParametersConcave else None

    @property
    def pinion_concave_ob_configuration(self) -> '_600.BasicConicalGearMachineSettingsGenerated':
        '''BasicConicalGearMachineSettingsGenerated: 'PinionConcaveOBConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_600.BasicConicalGearMachineSettingsGenerated)(self.wrapped.PinionConcaveOBConfiguration) if self.wrapped.PinionConcaveOBConfiguration else None
