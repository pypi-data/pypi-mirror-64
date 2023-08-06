'''_3.py

MastaSettings
'''


from mastapy.bearings import _1493
from mastapy._internal import constructor
from mastapy.gears import _118, _119
from mastapy.gears.gear_designs.cylindrical import _765, _770, _771
from mastapy.gears.gear_designs import _706
from mastapy.gears.ltca.cylindrical import _621
from mastapy.gears.materials import _375
from mastapy.gears.rating.cylindrical import _261, _268
from mastapy.materials import _77
from mastapy.nodal_analysis import _1338, _1354
from mastapy.shafts import _37
from mastapy.system_model.part_model import _1988
from mastapy.utility.cad_export import _1324
from mastapy.utility.databases import _1321
from mastapy.utility import _1127, _1128
from mastapy.utility.scripting import _1250
from mastapy.utility.units_and_measurements import _1137
from mastapy._internal.python_net import python_net_import

_MASTA_SETTINGS = python_net_import('SMT.MastaAPI', 'MastaSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('MastaSettings',)


class MastaSettings:
    '''MastaSettings

    This is a mastapy class.
    '''

    TYPE = _MASTA_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MastaSettings.TYPE'):
        self.wrapped = instance_to_wrap

    @property
    def bearing_settings(self) -> '_1493.BearingSettings':
        '''BearingSettings: 'BearingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1493.BearingSettings)(self.wrapped.BearingSettings) if self.wrapped.BearingSettings else None

    @property
    def bevel_hypoid_gear_design_settings(self) -> '_118.BevelHypoidGearDesignSettings':
        '''BevelHypoidGearDesignSettings: 'BevelHypoidGearDesignSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_118.BevelHypoidGearDesignSettings)(self.wrapped.BevelHypoidGearDesignSettings) if self.wrapped.BevelHypoidGearDesignSettings else None

    @property
    def bevel_hypoid_gear_rating_settings(self) -> '_119.BevelHypoidGearRatingSettings':
        '''BevelHypoidGearRatingSettings: 'BevelHypoidGearRatingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_119.BevelHypoidGearRatingSettings)(self.wrapped.BevelHypoidGearRatingSettings) if self.wrapped.BevelHypoidGearRatingSettings else None

    @property
    def cylindrical_gear_defaults(self) -> '_765.CylindricalGearDefaults':
        '''CylindricalGearDefaults: 'CylindricalGearDefaults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_765.CylindricalGearDefaults)(self.wrapped.CylindricalGearDefaults) if self.wrapped.CylindricalGearDefaults else None

    @property
    def cylindrical_gear_design_constraint_settings(self) -> '_770.CylindricalGearDesignConstraintSettings':
        '''CylindricalGearDesignConstraintSettings: 'CylindricalGearDesignConstraintSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_770.CylindricalGearDesignConstraintSettings)(self.wrapped.CylindricalGearDesignConstraintSettings) if self.wrapped.CylindricalGearDesignConstraintSettings else None

    @property
    def cylindrical_gear_design_settings(self) -> '_771.CylindricalGearDesignSettings':
        '''CylindricalGearDesignSettings: 'CylindricalGearDesignSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_771.CylindricalGearDesignSettings)(self.wrapped.CylindricalGearDesignSettings) if self.wrapped.CylindricalGearDesignSettings else None

    @property
    def selected_design_constraints_collection(self) -> '_706.SelectedDesignConstraintsCollection':
        '''SelectedDesignConstraintsCollection: 'SelectedDesignConstraintsCollection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_706.SelectedDesignConstraintsCollection)(self.wrapped.SelectedDesignConstraintsCollection) if self.wrapped.SelectedDesignConstraintsCollection else None

    @property
    def cylindrical_gear_fe_settings(self) -> '_621.CylindricalGearFESettings':
        '''CylindricalGearFESettings: 'CylindricalGearFESettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_621.CylindricalGearFESettings)(self.wrapped.CylindricalGearFESettings) if self.wrapped.CylindricalGearFESettings else None

    @property
    def gear_material_expert_system_factor_settings(self) -> '_375.GearMaterialExpertSystemFactorSettings':
        '''GearMaterialExpertSystemFactorSettings: 'GearMaterialExpertSystemFactorSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_375.GearMaterialExpertSystemFactorSettings)(self.wrapped.GearMaterialExpertSystemFactorSettings) if self.wrapped.GearMaterialExpertSystemFactorSettings else None

    @property
    def cylindrical_gear_rating_settings(self) -> '_261.CylindricalGearRatingSettings':
        '''CylindricalGearRatingSettings: 'CylindricalGearRatingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_261.CylindricalGearRatingSettings)(self.wrapped.CylindricalGearRatingSettings) if self.wrapped.CylindricalGearRatingSettings else None

    @property
    def cylindrical_plastic_gear_rating_settings(self) -> '_268.CylindricalPlasticGearRatingSettings':
        '''CylindricalPlasticGearRatingSettings: 'CylindricalPlasticGearRatingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_268.CylindricalPlasticGearRatingSettings)(self.wrapped.CylindricalPlasticGearRatingSettings) if self.wrapped.CylindricalPlasticGearRatingSettings else None

    @property
    def materials_settings(self) -> '_77.MaterialsSettings':
        '''MaterialsSettings: 'MaterialsSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_77.MaterialsSettings)(self.wrapped.MaterialsSettings) if self.wrapped.MaterialsSettings else None

    @property
    def analysis_settings(self) -> '_1338.AnalysisSettings':
        '''AnalysisSettings: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1338.AnalysisSettings)(self.wrapped.AnalysisSettings) if self.wrapped.AnalysisSettings else None

    @property
    def fe_user_settings(self) -> '_1354.FEUserSettings':
        '''FEUserSettings: 'FEUserSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1354.FEUserSettings)(self.wrapped.FEUserSettings) if self.wrapped.FEUserSettings else None

    @property
    def shaft_settings(self) -> '_37.ShaftSettings':
        '''ShaftSettings: 'ShaftSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_37.ShaftSettings)(self.wrapped.ShaftSettings) if self.wrapped.ShaftSettings else None

    @property
    def planet_carrier_settings(self) -> '_1988.PlanetCarrierSettings':
        '''PlanetCarrierSettings: 'PlanetCarrierSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.PlanetCarrierSettings)(self.wrapped.PlanetCarrierSettings) if self.wrapped.PlanetCarrierSettings else None

    @property
    def cad_export_settings(self) -> '_1324.CADExportSettings':
        '''CADExportSettings: 'CADExportSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1324.CADExportSettings)(self.wrapped.CADExportSettings) if self.wrapped.CADExportSettings else None

    @property
    def database_settings(self) -> '_1321.DatabaseSettings':
        '''DatabaseSettings: 'DatabaseSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1321.DatabaseSettings)(self.wrapped.DatabaseSettings) if self.wrapped.DatabaseSettings else None

    @property
    def program_settings(self) -> '_1127.ProgramSettings':
        '''ProgramSettings: 'ProgramSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1127.ProgramSettings)(self.wrapped.ProgramSettings) if self.wrapped.ProgramSettings else None

    @property
    def pushbullet_settings(self) -> '_1128.PushbulletSettings':
        '''PushbulletSettings: 'PushbulletSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1128.PushbulletSettings)(self.wrapped.PushbulletSettings) if self.wrapped.PushbulletSettings else None

    @property
    def scripting_setup(self) -> '_1250.ScriptingSetup':
        '''ScriptingSetup: 'ScriptingSetup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1250.ScriptingSetup)(self.wrapped.ScriptingSetup) if self.wrapped.ScriptingSetup else None

    @property
    def measurement_settings(self) -> '_1137.MeasurementSettings':
        '''MeasurementSettings: 'MeasurementSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1137.MeasurementSettings)(self.wrapped.MeasurementSettings) if self.wrapped.MeasurementSettings else None
