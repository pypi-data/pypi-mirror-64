'''list_with_selected_item.py

Implementations of 'ListWithSelectedItem' in Python.
As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
'''


from typing import List, Generic, TypeVar

from mastapy._internal import mixins, constructor, conversion
from mastapy._internal.python_net import python_net_import
from mastapy.gears.ltca.cylindrical import _623, _622
from mastapy.gears.manufacturing.cylindrical import _403
from mastapy.gears.manufacturing.bevel import _568
from mastapy.utility import _1131
from mastapy.utility.units_and_measurements import _1141, _1136
from mastapy.utility.units_and_measurements.measurements import (
    _1143, _1144, _1145, _1146,
    _1147, _1148, _1149, _1150,
    _1151, _1152, _1153, _1154,
    _1155, _1156, _1157, _1158,
    _1159, _1160, _1161, _1162,
    _1163, _1164, _1165, _1166,
    _1167, _1168, _1169, _1170,
    _1171, _1172, _1173, _1174,
    _1175, _1176, _1177, _1178,
    _1179, _1180, _1181, _1182,
    _1183, _1184, _1185, _1186,
    _1187, _1188, _1189, _1190,
    _1191, _1192, _1193, _1194,
    _1195, _1196, _1197, _1198,
    _1199, _1200, _1201, _1202,
    _1203, _1204, _1205, _1206,
    _1207, _1208, _1209, _1210,
    _1211, _1212, _1213, _1214,
    _1215, _1216, _1217, _1218,
    _1219, _1220, _1221, _1222,
    _1223, _1224, _1225, _1226,
    _1227, _1228, _1229, _1230,
    _1231, _1232, _1233, _1234,
    _1235, _1236, _1237, _1238,
    _1239, _1240, _1241, _1242,
    _1243, _1244, _1245, _1246,
    _1247, _1248, _1249
)
from mastapy._internal.cast_exception import CastException
from mastapy.utility.file_access_helpers import _1316
from mastapy.system_model.part_model import (
    _1990, _1970, _1966, _1959,
    _1962, _1964, _1969, _1973,
    _1975, _1978, _1981, _1982,
    _1983, _1985, _1987, _1989,
    _1995, _1996
)
from mastapy.system_model.imported_fes import (
    _1885, _1913, _1914, _1915,
    _1917, _1918, _1919, _1920,
    _1921, _1922, _1923, _1935,
    _1946, _1947, _1924, _1912,
    _1902
)
from mastapy.system_model.part_model.shaft_model import _1999
from mastapy.system_model.part_model.gears import (
    _2029, _2031, _2033, _2034,
    _2035, _2037, _2039, _2041,
    _2043, _2044, _2046, _2050,
    _2052, _2054, _2056, _2059,
    _2061, _2063, _2065, _2066,
    _2067, _2069, _2042, _2048,
    _2030, _2032, _2036, _2038,
    _2040, _2045, _2051, _2053,
    _2055, _2057, _2058, _2060,
    _2062, _2064, _2068, _2070
)
from mastapy.system_model.part_model.couplings import (
    _2091, _2094, _2096, _2098,
    _2100, _2101, _2107, _2109,
    _2111, _2114, _2115, _2116,
    _2118, _2120
)
from mastapy.system_model.part_model.part_groups import _2004
from mastapy.gears.gear_designs import _705
from mastapy.gears.gear_designs.zerol_bevel import _709
from mastapy.gears.gear_designs.worm import _714
from mastapy.gears.gear_designs.straight_bevel_diff import _718
from mastapy.gears.gear_designs.straight_bevel import _722
from mastapy.gears.gear_designs.spiral_bevel import _726
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _730
from mastapy.gears.gear_designs.klingelnberg_hypoid import _734
from mastapy.gears.gear_designs.klingelnberg_conical import _738
from mastapy.gears.gear_designs.hypoid import _742
from mastapy.gears.gear_designs.face import _750
from mastapy.gears.gear_designs.cylindrical import _777, _786
from mastapy.gears.gear_designs.conical import _880
from mastapy.gears.gear_designs.concept import _902
from mastapy.gears.gear_designs.bevel import _906
from mastapy.gears.gear_designs.agma_gleason_conical import _919
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2233, _2234, _2235, _2236
)
from mastapy.system_model.analyses_and_results.load_case_groups import _5214, _5215
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5308
from mastapy.system_model.analyses_and_results.gear_whine_analyses.whine_analyses_results import _5382
from mastapy.system_model.analyses_and_results.static_loads import _6161

_LIST_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.Utility.Property', 'ListWithSelectedItem')


__docformat__ = 'restructuredtext en'
__all__ = (
    'ListWithSelectedItem_str', 'ListWithSelectedItem_T',
    'ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis', 'ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis',
    'ListWithSelectedItem_CylindricalSetManufacturingConfig', 'ListWithSelectedItem_ConicalSetManufacturingConfig',
    'ListWithSelectedItem_SystemDirectory', 'ListWithSelectedItem_Unit',
    'ListWithSelectedItem_MeasurementBase', 'ListWithSelectedItem_int',
    'ListWithSelectedItem_ColumnTitle', 'ListWithSelectedItem_PowerLoad',
    'ListWithSelectedItem_ImportedFELink', 'ListWithSelectedItem_ImportedFEStiffnessNode',
    'ListWithSelectedItem_Datum', 'ListWithSelectedItem_Component',
    'ListWithSelectedItem_ImportedFE', 'ListWithSelectedItem_GuideDxfModel',
    'ListWithSelectedItem_ConcentricPartGroup', 'ListWithSelectedItem_GearSetDesign',
    'ListWithSelectedItem_ShaftHubConnection', 'ListWithSelectedItem_TSelectableItem',
    'ListWithSelectedItem_CylindricalGearSystemDeflection', 'ListWithSelectedItem_DesignState',
    'ListWithSelectedItem_ImportedFEComponent', 'ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis',
    'ListWithSelectedItem_ResultLocationSelectionGroup', 'ListWithSelectedItem_StaticLoadCase',
    'ListWithSelectedItem_DutyCycle', 'ListWithSelectedItem_float',
    'ListWithSelectedItem_ElectricMachineDataSet', 'ListWithSelectedItem_CylindricalGearSet',
    'ListWithSelectedItem_PointLoad', 'ListWithSelectedItem_GearSet'
)


T = TypeVar('T')
TSelectableItem = TypeVar('TSelectableItem')


class ListWithSelectedItem_str(str, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_str

    A specific implementation of 'ListWithSelectedItem' for 'str' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'str'

    def __new__(cls, instance_to_wrap: 'ListWithSelectedItem_str.TYPE'):
        return str.__new__(cls, instance_to_wrap.SelectedValue) if instance_to_wrap.SelectedValue else None

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_str.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> 'str':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return str

    @property
    def selected_value(self) -> 'str':
        '''str: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[str]':
        '''List[str]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, str)
        return value


class ListWithSelectedItem_T(Generic[T], mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_T

    A specific implementation of 'ListWithSelectedItem' for 'T' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'T'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_T.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> 'T':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return T

    @property
    def selected_value(self) -> 'T':
        '''T: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(T)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[T]':
        '''List[T]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(T))
        return value


class ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis(_623.CylindricalGearMeshLoadDistributionAnalysis, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearMeshLoadDistributionAnalysis' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'CylindricalGearMeshLoadDistributionAnalysis'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_623.CylindricalGearMeshLoadDistributionAnalysis.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _623.CylindricalGearMeshLoadDistributionAnalysis.TYPE

    @property
    def selected_value(self) -> '_623.CylindricalGearMeshLoadDistributionAnalysis':
        '''CylindricalGearMeshLoadDistributionAnalysis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_623.CylindricalGearMeshLoadDistributionAnalysis)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_623.CylindricalGearMeshLoadDistributionAnalysis]':
        '''List[CylindricalGearMeshLoadDistributionAnalysis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_623.CylindricalGearMeshLoadDistributionAnalysis))
        return value


class ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis(_622.CylindricalGearLoadDistributionAnalysis, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearLoadDistributionAnalysis' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'CylindricalGearLoadDistributionAnalysis'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_622.CylindricalGearLoadDistributionAnalysis.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _622.CylindricalGearLoadDistributionAnalysis.TYPE

    @property
    def selected_value(self) -> '_622.CylindricalGearLoadDistributionAnalysis':
        '''CylindricalGearLoadDistributionAnalysis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_622.CylindricalGearLoadDistributionAnalysis)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_622.CylindricalGearLoadDistributionAnalysis]':
        '''List[CylindricalGearLoadDistributionAnalysis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_622.CylindricalGearLoadDistributionAnalysis))
        return value


class ListWithSelectedItem_CylindricalSetManufacturingConfig(_403.CylindricalSetManufacturingConfig, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalSetManufacturingConfig

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalSetManufacturingConfig' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'CylindricalSetManufacturingConfig'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalSetManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_403.CylindricalSetManufacturingConfig.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _403.CylindricalSetManufacturingConfig.TYPE

    @property
    def selected_value(self) -> '_403.CylindricalSetManufacturingConfig':
        '''CylindricalSetManufacturingConfig: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_403.CylindricalSetManufacturingConfig)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_403.CylindricalSetManufacturingConfig]':
        '''List[CylindricalSetManufacturingConfig]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_403.CylindricalSetManufacturingConfig))
        return value


class ListWithSelectedItem_ConicalSetManufacturingConfig(_568.ConicalSetManufacturingConfig, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ConicalSetManufacturingConfig

    A specific implementation of 'ListWithSelectedItem' for 'ConicalSetManufacturingConfig' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'ConicalSetManufacturingConfig'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ConicalSetManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_568.ConicalSetManufacturingConfig.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _568.ConicalSetManufacturingConfig.TYPE

    @property
    def selected_value(self) -> '_568.ConicalSetManufacturingConfig':
        '''ConicalSetManufacturingConfig: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_568.ConicalSetManufacturingConfig)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_568.ConicalSetManufacturingConfig]':
        '''List[ConicalSetManufacturingConfig]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_568.ConicalSetManufacturingConfig))
        return value


class ListWithSelectedItem_SystemDirectory(_1131.SystemDirectory, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_SystemDirectory

    A specific implementation of 'ListWithSelectedItem' for 'SystemDirectory' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'SystemDirectory'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_SystemDirectory.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_1131.SystemDirectory.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1131.SystemDirectory.TYPE

    @property
    def selected_value(self) -> '_1131.SystemDirectory':
        '''SystemDirectory: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1131.SystemDirectory)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1131.SystemDirectory]':
        '''List[SystemDirectory]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1131.SystemDirectory))
        return value


class ListWithSelectedItem_Unit(_1141.Unit, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_Unit

    A specific implementation of 'ListWithSelectedItem' for 'Unit' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'Unit'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_Unit.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_1141.Unit.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1141.Unit.TYPE

    @property
    def selected_value(self) -> '_1141.Unit':
        '''Unit: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1141.Unit)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1141.Unit]':
        '''List[Unit]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1141.Unit))
        return value


class ListWithSelectedItem_MeasurementBase(_1136.MeasurementBase, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_MeasurementBase

    A specific implementation of 'ListWithSelectedItem' for 'MeasurementBase' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'MeasurementBase'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_MeasurementBase.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_1136.MeasurementBase.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1136.MeasurementBase.TYPE

    @property
    def selected_value(self) -> '_1136.MeasurementBase':
        '''MeasurementBase: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1136.MeasurementBase)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_acceleration(self) -> '_1143.Acceleration':
        '''Acceleration: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1143.Acceleration.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Acceleration. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1143.Acceleration)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angle(self) -> '_1144.Angle':
        '''Angle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1144.Angle.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Angle. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1144.Angle)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angle_per_unit_temperature(self) -> '_1145.AnglePerUnitTemperature':
        '''AnglePerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1145.AnglePerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AnglePerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1145.AnglePerUnitTemperature)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angle_small(self) -> '_1146.AngleSmall':
        '''AngleSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1146.AngleSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngleSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1146.AngleSmall)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angle_very_small(self) -> '_1147.AngleVerySmall':
        '''AngleVerySmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1147.AngleVerySmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngleVerySmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1147.AngleVerySmall)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angular_acceleration(self) -> '_1148.AngularAcceleration':
        '''AngularAcceleration: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1148.AngularAcceleration.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularAcceleration. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1148.AngularAcceleration)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angular_compliance(self) -> '_1149.AngularCompliance':
        '''AngularCompliance: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1149.AngularCompliance.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularCompliance. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1149.AngularCompliance)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angular_jerk(self) -> '_1150.AngularJerk':
        '''AngularJerk: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1150.AngularJerk.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularJerk. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1150.AngularJerk)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angular_stiffness(self) -> '_1151.AngularStiffness':
        '''AngularStiffness: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1151.AngularStiffness.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularStiffness. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1151.AngularStiffness)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angular_velocity(self) -> '_1152.AngularVelocity':
        '''AngularVelocity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1152.AngularVelocity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularVelocity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1152.AngularVelocity)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_area(self) -> '_1153.Area':
        '''Area: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1153.Area.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Area. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1153.Area)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_area_small(self) -> '_1154.AreaSmall':
        '''AreaSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1154.AreaSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AreaSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1154.AreaSmall)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cycles(self) -> '_1155.Cycles':
        '''Cycles: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1155.Cycles.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Cycles. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1155.Cycles)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_damage(self) -> '_1156.Damage':
        '''Damage: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1156.Damage.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Damage. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1156.Damage)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_damage_rate(self) -> '_1157.DamageRate':
        '''DamageRate: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1157.DamageRate.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to DamageRate. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1157.DamageRate)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_decibel(self) -> '_1158.Decibel':
        '''Decibel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1158.Decibel.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Decibel. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1158.Decibel)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_density(self) -> '_1159.Density':
        '''Density: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1159.Density.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Density. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1159.Density)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_energy(self) -> '_1160.Energy':
        '''Energy: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1160.Energy.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Energy. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1160.Energy)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_energy_per_unit_area(self) -> '_1161.EnergyPerUnitArea':
        '''EnergyPerUnitArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1161.EnergyPerUnitArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to EnergyPerUnitArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1161.EnergyPerUnitArea)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_energy_per_unit_area_small(self) -> '_1162.EnergyPerUnitAreaSmall':
        '''EnergyPerUnitAreaSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1162.EnergyPerUnitAreaSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to EnergyPerUnitAreaSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1162.EnergyPerUnitAreaSmall)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_energy_small(self) -> '_1163.EnergySmall':
        '''EnergySmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1163.EnergySmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to EnergySmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1163.EnergySmall)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_enum(self) -> '_1164.Enum':
        '''Enum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1164.Enum.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Enum. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1164.Enum)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_flow_rate(self) -> '_1165.FlowRate':
        '''FlowRate: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1165.FlowRate.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FlowRate. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1165.FlowRate)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_force(self) -> '_1166.Force':
        '''Force: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1166.Force.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Force. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1166.Force)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_force_per_unit_length(self) -> '_1167.ForcePerUnitLength':
        '''ForcePerUnitLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1167.ForcePerUnitLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ForcePerUnitLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1167.ForcePerUnitLength)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_force_per_unit_pressure(self) -> '_1168.ForcePerUnitPressure':
        '''ForcePerUnitPressure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1168.ForcePerUnitPressure.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ForcePerUnitPressure. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1168.ForcePerUnitPressure)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_force_per_unit_temperature(self) -> '_1169.ForcePerUnitTemperature':
        '''ForcePerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1169.ForcePerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ForcePerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1169.ForcePerUnitTemperature)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_fraction_measurement_base(self) -> '_1170.FractionMeasurementBase':
        '''FractionMeasurementBase: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1170.FractionMeasurementBase.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FractionMeasurementBase. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1170.FractionMeasurementBase)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_frequency(self) -> '_1171.Frequency':
        '''Frequency: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1171.Frequency.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Frequency. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1171.Frequency)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_fuel_consumption_engine(self) -> '_1172.FuelConsumptionEngine':
        '''FuelConsumptionEngine: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1172.FuelConsumptionEngine.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FuelConsumptionEngine. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1172.FuelConsumptionEngine)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_fuel_efficiency_vehicle(self) -> '_1173.FuelEfficiencyVehicle':
        '''FuelEfficiencyVehicle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1173.FuelEfficiencyVehicle.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FuelEfficiencyVehicle. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1173.FuelEfficiencyVehicle)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_gradient(self) -> '_1174.Gradient':
        '''Gradient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1174.Gradient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Gradient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1174.Gradient)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_heat_conductivity(self) -> '_1175.HeatConductivity':
        '''HeatConductivity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1175.HeatConductivity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatConductivity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1175.HeatConductivity)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_heat_transfer(self) -> '_1176.HeatTransfer':
        '''HeatTransfer: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1176.HeatTransfer.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatTransfer. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1176.HeatTransfer)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_heat_transfer_coefficient_for_plastic_gear_tooth(self) -> '_1177.HeatTransferCoefficientForPlasticGearTooth':
        '''HeatTransferCoefficientForPlasticGearTooth: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1177.HeatTransferCoefficientForPlasticGearTooth.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatTransferCoefficientForPlasticGearTooth. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1177.HeatTransferCoefficientForPlasticGearTooth)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_heat_transfer_resistance(self) -> '_1178.HeatTransferResistance':
        '''HeatTransferResistance: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1178.HeatTransferResistance.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatTransferResistance. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1178.HeatTransferResistance)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_impulse(self) -> '_1179.Impulse':
        '''Impulse: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1179.Impulse.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Impulse. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1179.Impulse)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_index(self) -> '_1180.Index':
        '''Index: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1180.Index.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Index. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1180.Index)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_integer(self) -> '_1181.Integer':
        '''Integer: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1181.Integer.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Integer. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1181.Integer)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_inverse_short_length(self) -> '_1182.InverseShortLength':
        '''InverseShortLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1182.InverseShortLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to InverseShortLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1182.InverseShortLength)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_inverse_short_time(self) -> '_1183.InverseShortTime':
        '''InverseShortTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1183.InverseShortTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to InverseShortTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1183.InverseShortTime)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_jerk(self) -> '_1184.Jerk':
        '''Jerk: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1184.Jerk.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Jerk. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1184.Jerk)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_kinematic_viscosity(self) -> '_1185.KinematicViscosity':
        '''KinematicViscosity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1185.KinematicViscosity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KinematicViscosity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1185.KinematicViscosity)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_long(self) -> '_1186.LengthLong':
        '''LengthLong: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1186.LengthLong.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthLong. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1186.LengthLong)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_medium(self) -> '_1187.LengthMedium':
        '''LengthMedium: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1187.LengthMedium.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthMedium. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1187.LengthMedium)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_per_unit_temperature(self) -> '_1188.LengthPerUnitTemperature':
        '''LengthPerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1188.LengthPerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthPerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1188.LengthPerUnitTemperature)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_short(self) -> '_1189.LengthShort':
        '''LengthShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1189.LengthShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1189.LengthShort)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_to_the_fourth(self) -> '_1190.LengthToTheFourth':
        '''LengthToTheFourth: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1190.LengthToTheFourth.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthToTheFourth. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1190.LengthToTheFourth)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_very_long(self) -> '_1191.LengthVeryLong':
        '''LengthVeryLong: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1191.LengthVeryLong.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthVeryLong. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1191.LengthVeryLong)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_very_short(self) -> '_1192.LengthVeryShort':
        '''LengthVeryShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1192.LengthVeryShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthVeryShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1192.LengthVeryShort)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_very_short_per_length_short(self) -> '_1193.LengthVeryShortPerLengthShort':
        '''LengthVeryShortPerLengthShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1193.LengthVeryShortPerLengthShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthVeryShortPerLengthShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1193.LengthVeryShortPerLengthShort)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_linear_angular_damping(self) -> '_1194.LinearAngularDamping':
        '''LinearAngularDamping: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1194.LinearAngularDamping.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearAngularDamping. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1194.LinearAngularDamping)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_linear_angular_stiffness_cross_term(self) -> '_1195.LinearAngularStiffnessCrossTerm':
        '''LinearAngularStiffnessCrossTerm: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1195.LinearAngularStiffnessCrossTerm.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearAngularStiffnessCrossTerm. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1195.LinearAngularStiffnessCrossTerm)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_linear_damping(self) -> '_1196.LinearDamping':
        '''LinearDamping: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1196.LinearDamping.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearDamping. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1196.LinearDamping)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_linear_flexibility(self) -> '_1197.LinearFlexibility':
        '''LinearFlexibility: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1197.LinearFlexibility.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearFlexibility. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1197.LinearFlexibility)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_linear_stiffness(self) -> '_1198.LinearStiffness':
        '''LinearStiffness: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1198.LinearStiffness.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearStiffness. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1198.LinearStiffness)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_mass(self) -> '_1199.Mass':
        '''Mass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1199.Mass.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Mass. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1199.Mass)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_mass_per_unit_length(self) -> '_1200.MassPerUnitLength':
        '''MassPerUnitLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1200.MassPerUnitLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MassPerUnitLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1200.MassPerUnitLength)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_mass_per_unit_time(self) -> '_1201.MassPerUnitTime':
        '''MassPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1201.MassPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MassPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1201.MassPerUnitTime)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_moment_of_inertia(self) -> '_1202.MomentOfInertia':
        '''MomentOfInertia: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1202.MomentOfInertia.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MomentOfInertia. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1202.MomentOfInertia)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_moment_of_inertia_per_unit_length(self) -> '_1203.MomentOfInertiaPerUnitLength':
        '''MomentOfInertiaPerUnitLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1203.MomentOfInertiaPerUnitLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MomentOfInertiaPerUnitLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1203.MomentOfInertiaPerUnitLength)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_moment_per_unit_pressure(self) -> '_1204.MomentPerUnitPressure':
        '''MomentPerUnitPressure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1204.MomentPerUnitPressure.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MomentPerUnitPressure. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1204.MomentPerUnitPressure)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_number(self) -> '_1205.Number':
        '''Number: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1205.Number.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Number. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1205.Number)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_percentage(self) -> '_1206.Percentage':
        '''Percentage: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1206.Percentage.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Percentage. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1206.Percentage)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power(self) -> '_1207.Power':
        '''Power: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1207.Power.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Power. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1207.Power)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power_per_small_area(self) -> '_1208.PowerPerSmallArea':
        '''PowerPerSmallArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1208.PowerPerSmallArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerPerSmallArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1208.PowerPerSmallArea)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power_per_unit_time(self) -> '_1209.PowerPerUnitTime':
        '''PowerPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1209.PowerPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1209.PowerPerUnitTime)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power_small(self) -> '_1210.PowerSmall':
        '''PowerSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1210.PowerSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1210.PowerSmall)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power_small_per_area(self) -> '_1211.PowerSmallPerArea':
        '''PowerSmallPerArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1211.PowerSmallPerArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmallPerArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1211.PowerSmallPerArea)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power_small_per_unit_area_per_unit_time(self) -> '_1212.PowerSmallPerUnitAreaPerUnitTime':
        '''PowerSmallPerUnitAreaPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1212.PowerSmallPerUnitAreaPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmallPerUnitAreaPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1212.PowerSmallPerUnitAreaPerUnitTime)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power_small_per_unit_time(self) -> '_1213.PowerSmallPerUnitTime':
        '''PowerSmallPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1213.PowerSmallPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmallPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1213.PowerSmallPerUnitTime)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_pressure(self) -> '_1214.Pressure':
        '''Pressure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1214.Pressure.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Pressure. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1214.Pressure)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_pressure_per_unit_time(self) -> '_1215.PressurePerUnitTime':
        '''PressurePerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1215.PressurePerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PressurePerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1215.PressurePerUnitTime)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_pressure_velocity_product(self) -> '_1216.PressureVelocityProduct':
        '''PressureVelocityProduct: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1216.PressureVelocityProduct.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PressureVelocityProduct. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1216.PressureVelocityProduct)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_pressure_viscosity_coefficient(self) -> '_1217.PressureViscosityCoefficient':
        '''PressureViscosityCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1217.PressureViscosityCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PressureViscosityCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1217.PressureViscosityCoefficient)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_price(self) -> '_1218.Price':
        '''Price: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1218.Price.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Price. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1218.Price)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_quadratic_angular_damping(self) -> '_1219.QuadraticAngularDamping':
        '''QuadraticAngularDamping: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1219.QuadraticAngularDamping.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to QuadraticAngularDamping. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1219.QuadraticAngularDamping)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_quadratic_drag(self) -> '_1220.QuadraticDrag':
        '''QuadraticDrag: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1220.QuadraticDrag.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to QuadraticDrag. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1220.QuadraticDrag)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_rescaled_measurement(self) -> '_1221.RescaledMeasurement':
        '''RescaledMeasurement: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1221.RescaledMeasurement.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RescaledMeasurement. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1221.RescaledMeasurement)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_rotatum(self) -> '_1222.Rotatum':
        '''Rotatum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1222.Rotatum.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Rotatum. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1222.Rotatum)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_safety_factor(self) -> '_1223.SafetyFactor':
        '''SafetyFactor: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1223.SafetyFactor.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SafetyFactor. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1223.SafetyFactor)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_specific_acoustic_impedance(self) -> '_1224.SpecificAcousticImpedance':
        '''SpecificAcousticImpedance: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1224.SpecificAcousticImpedance.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpecificAcousticImpedance. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1224.SpecificAcousticImpedance)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_specific_heat(self) -> '_1225.SpecificHeat':
        '''SpecificHeat: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1225.SpecificHeat.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpecificHeat. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1225.SpecificHeat)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_square_root_of_unit_force_per_unit_area(self) -> '_1226.SquareRootOfUnitForcePerUnitArea':
        '''SquareRootOfUnitForcePerUnitArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1226.SquareRootOfUnitForcePerUnitArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SquareRootOfUnitForcePerUnitArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1226.SquareRootOfUnitForcePerUnitArea)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_stiffness_per_unit_face_width(self) -> '_1227.StiffnessPerUnitFaceWidth':
        '''StiffnessPerUnitFaceWidth: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1227.StiffnessPerUnitFaceWidth.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StiffnessPerUnitFaceWidth. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1227.StiffnessPerUnitFaceWidth)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_stress(self) -> '_1228.Stress':
        '''Stress: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1228.Stress.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Stress. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1228.Stress)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_temperature(self) -> '_1229.Temperature':
        '''Temperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1229.Temperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Temperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1229.Temperature)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_temperature_difference(self) -> '_1230.TemperatureDifference':
        '''TemperatureDifference: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1230.TemperatureDifference.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TemperatureDifference. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1230.TemperatureDifference)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_temperature_per_unit_time(self) -> '_1231.TemperaturePerUnitTime':
        '''TemperaturePerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1231.TemperaturePerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TemperaturePerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1231.TemperaturePerUnitTime)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_text(self) -> '_1232.Text':
        '''Text: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1232.Text.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Text. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1232.Text)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_thermal_contact_coefficient(self) -> '_1233.ThermalContactCoefficient':
        '''ThermalContactCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1233.ThermalContactCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ThermalContactCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1233.ThermalContactCoefficient)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_thermal_expansion_coefficient(self) -> '_1234.ThermalExpansionCoefficient':
        '''ThermalExpansionCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1234.ThermalExpansionCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ThermalExpansionCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1234.ThermalExpansionCoefficient)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_thermo_elastic_factor(self) -> '_1235.ThermoElasticFactor':
        '''ThermoElasticFactor: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1235.ThermoElasticFactor.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ThermoElasticFactor. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1235.ThermoElasticFactor)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_time(self) -> '_1236.Time':
        '''Time: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1236.Time.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Time. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1236.Time)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_time_short(self) -> '_1237.TimeShort':
        '''TimeShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1237.TimeShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TimeShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1237.TimeShort)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_time_very_short(self) -> '_1238.TimeVeryShort':
        '''TimeVeryShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1238.TimeVeryShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TimeVeryShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1238.TimeVeryShort)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_torque(self) -> '_1239.Torque':
        '''Torque: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1239.Torque.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Torque. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1239.Torque)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_torque_converter_inverse_k(self) -> '_1240.TorqueConverterInverseK':
        '''TorqueConverterInverseK: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1240.TorqueConverterInverseK.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterInverseK. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1240.TorqueConverterInverseK)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_torque_converter_k(self) -> '_1241.TorqueConverterK':
        '''TorqueConverterK: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1241.TorqueConverterK.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterK. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1241.TorqueConverterK)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_torque_per_unit_temperature(self) -> '_1242.TorquePerUnitTemperature':
        '''TorquePerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1242.TorquePerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorquePerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1242.TorquePerUnitTemperature)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_velocity(self) -> '_1243.Velocity':
        '''Velocity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1243.Velocity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Velocity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1243.Velocity)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_velocity_small(self) -> '_1244.VelocitySmall':
        '''VelocitySmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1244.VelocitySmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to VelocitySmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1244.VelocitySmall)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_viscosity(self) -> '_1245.Viscosity':
        '''Viscosity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1245.Viscosity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Viscosity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1245.Viscosity)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_voltage(self) -> '_1246.Voltage':
        '''Voltage: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1246.Voltage.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Voltage. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1246.Voltage)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_volume(self) -> '_1247.Volume':
        '''Volume: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1247.Volume.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Volume. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1247.Volume)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_wear_coefficient(self) -> '_1248.WearCoefficient':
        '''WearCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1248.WearCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WearCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1248.WearCoefficient)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_yank(self) -> '_1249.Yank':
        '''Yank: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1249.Yank.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Yank. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1249.Yank)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1136.MeasurementBase]':
        '''List[MeasurementBase]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1136.MeasurementBase))
        return value


class ListWithSelectedItem_int(int, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_int

    A specific implementation of 'ListWithSelectedItem' for 'int' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'int'

    def __new__(cls, instance_to_wrap: 'ListWithSelectedItem_int.TYPE'):
        return int.__new__(cls, instance_to_wrap.SelectedValue) if instance_to_wrap.SelectedValue else 0

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_int.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> 'int':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return int

    @property
    def selected_value(self) -> 'int':
        '''int: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[int]':
        '''List[int]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, int)
        return value


class ListWithSelectedItem_ColumnTitle(_1316.ColumnTitle, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ColumnTitle

    A specific implementation of 'ListWithSelectedItem' for 'ColumnTitle' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'ColumnTitle'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ColumnTitle.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_1316.ColumnTitle.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1316.ColumnTitle.TYPE

    @property
    def selected_value(self) -> '_1316.ColumnTitle':
        '''ColumnTitle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1316.ColumnTitle)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1316.ColumnTitle]':
        '''List[ColumnTitle]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1316.ColumnTitle))
        return value


class ListWithSelectedItem_PowerLoad(_1990.PowerLoad, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_PowerLoad

    A specific implementation of 'ListWithSelectedItem' for 'PowerLoad' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'PowerLoad'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_PowerLoad.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_1990.PowerLoad.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1990.PowerLoad.TYPE

    @property
    def selected_value(self) -> '_1990.PowerLoad':
        '''PowerLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1990.PowerLoad)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1990.PowerLoad]':
        '''List[PowerLoad]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1990.PowerLoad))
        return value


class ListWithSelectedItem_ImportedFELink(_1885.ImportedFELink, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ImportedFELink

    A specific implementation of 'ListWithSelectedItem' for 'ImportedFELink' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'ImportedFELink'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ImportedFELink.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_1885.ImportedFELink.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1885.ImportedFELink.TYPE

    @property
    def selected_value(self) -> '_1885.ImportedFELink':
        '''ImportedFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1885.ImportedFELink)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_imported_fe_electric_machine_stator_link(self) -> '_1913.ImportedFEElectricMachineStatorLink':
        '''ImportedFEElectricMachineStatorLink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1913.ImportedFEElectricMachineStatorLink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ImportedFEElectricMachineStatorLink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1913.ImportedFEElectricMachineStatorLink)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_imported_fe_gear_mesh_link(self) -> '_1914.ImportedFEGearMeshLink':
        '''ImportedFEGearMeshLink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1914.ImportedFEGearMeshLink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ImportedFEGearMeshLink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1914.ImportedFEGearMeshLink)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_imported_fe_gear_with_duplicated_meshes_link(self) -> '_1915.ImportedFEGearWithDuplicatedMeshesLink':
        '''ImportedFEGearWithDuplicatedMeshesLink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1915.ImportedFEGearWithDuplicatedMeshesLink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ImportedFEGearWithDuplicatedMeshesLink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1915.ImportedFEGearWithDuplicatedMeshesLink)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_imported_fe_multi_node_connector_link(self) -> '_1917.ImportedFEMultiNodeConnectorLink':
        '''ImportedFEMultiNodeConnectorLink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1917.ImportedFEMultiNodeConnectorLink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ImportedFEMultiNodeConnectorLink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1917.ImportedFEMultiNodeConnectorLink)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_imported_fe_multi_node_link(self) -> '_1918.ImportedFEMultiNodeLink':
        '''ImportedFEMultiNodeLink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1918.ImportedFEMultiNodeLink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ImportedFEMultiNodeLink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1918.ImportedFEMultiNodeLink)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_imported_fe_node_link(self) -> '_1919.ImportedFENodeLink':
        '''ImportedFENodeLink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1919.ImportedFENodeLink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ImportedFENodeLink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1919.ImportedFENodeLink)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_imported_fe_planetary_connector_multi_node_link(self) -> '_1920.ImportedFEPlanetaryConnectorMultiNodeLink':
        '''ImportedFEPlanetaryConnectorMultiNodeLink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1920.ImportedFEPlanetaryConnectorMultiNodeLink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ImportedFEPlanetaryConnectorMultiNodeLink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1920.ImportedFEPlanetaryConnectorMultiNodeLink)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_imported_fe_planet_based_link(self) -> '_1921.ImportedFEPlanetBasedLink':
        '''ImportedFEPlanetBasedLink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1921.ImportedFEPlanetBasedLink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ImportedFEPlanetBasedLink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1921.ImportedFEPlanetBasedLink)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_imported_fe_planet_carrier_link(self) -> '_1922.ImportedFEPlanetCarrierLink':
        '''ImportedFEPlanetCarrierLink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1922.ImportedFEPlanetCarrierLink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ImportedFEPlanetCarrierLink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1922.ImportedFEPlanetCarrierLink)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_imported_fe_point_load_link(self) -> '_1923.ImportedFEPointLoadLink':
        '''ImportedFEPointLoadLink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1923.ImportedFEPointLoadLink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ImportedFEPointLoadLink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1923.ImportedFEPointLoadLink)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_multi_angle_connection_link(self) -> '_1935.MultiAngleConnectionLink':
        '''MultiAngleConnectionLink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1935.MultiAngleConnectionLink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MultiAngleConnectionLink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1935.MultiAngleConnectionLink)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_rolling_ring_connection_link(self) -> '_1946.RollingRingConnectionLink':
        '''RollingRingConnectionLink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1946.RollingRingConnectionLink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RollingRingConnectionLink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1946.RollingRingConnectionLink)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_shaft_hub_connection_fe_link(self) -> '_1947.ShaftHubConnectionFELink':
        '''ShaftHubConnectionFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1947.ShaftHubConnectionFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ShaftHubConnectionFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1947.ShaftHubConnectionFELink)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1885.ImportedFELink]':
        '''List[ImportedFELink]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1885.ImportedFELink))
        return value


class ListWithSelectedItem_ImportedFEStiffnessNode(_1924.ImportedFEStiffnessNode, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ImportedFEStiffnessNode

    A specific implementation of 'ListWithSelectedItem' for 'ImportedFEStiffnessNode' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'ImportedFEStiffnessNode'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ImportedFEStiffnessNode.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_1924.ImportedFEStiffnessNode.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1924.ImportedFEStiffnessNode.TYPE

    @property
    def selected_value(self) -> '_1924.ImportedFEStiffnessNode':
        '''ImportedFEStiffnessNode: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1924.ImportedFEStiffnessNode)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1924.ImportedFEStiffnessNode]':
        '''List[ImportedFEStiffnessNode]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1924.ImportedFEStiffnessNode))
        return value


class ListWithSelectedItem_Datum(_1970.Datum, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_Datum

    A specific implementation of 'ListWithSelectedItem' for 'Datum' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'Datum'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_Datum.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_1970.Datum.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1970.Datum.TYPE

    @property
    def selected_value(self) -> '_1970.Datum':
        '''Datum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1970.Datum)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1970.Datum]':
        '''List[Datum]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1970.Datum))
        return value


class ListWithSelectedItem_Component(_1966.Component, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_Component

    A specific implementation of 'ListWithSelectedItem' for 'Component' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'Component'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_Component.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_1966.Component.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1966.Component.TYPE

    @property
    def selected_value(self) -> '_1966.Component':
        '''Component: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1966.Component)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_abstract_shaft_or_housing(self) -> '_1959.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1959.AbstractShaftOrHousing.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AbstractShaftOrHousing. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1959.AbstractShaftOrHousing)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bearing(self) -> '_1962.Bearing':
        '''Bearing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1962.Bearing.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Bearing. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1962.Bearing)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bolt(self) -> '_1964.Bolt':
        '''Bolt: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1964.Bolt.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Bolt. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1964.Bolt)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_connector(self) -> '_1969.Connector':
        '''Connector: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1969.Connector.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Connector. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1969.Connector)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_datum(self) -> '_1970.Datum':
        '''Datum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1970.Datum.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Datum. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1970.Datum)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_external_cad_model(self) -> '_1973.ExternalCADModel':
        '''ExternalCADModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1973.ExternalCADModel.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ExternalCADModel. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1973.ExternalCADModel)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_guide_dxf_model(self) -> '_1975.GuideDxfModel':
        '''GuideDxfModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1975.GuideDxfModel.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GuideDxfModel. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1975.GuideDxfModel)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_imported_fe_component(self) -> '_1978.ImportedFEComponent':
        '''ImportedFEComponent: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1978.ImportedFEComponent.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ImportedFEComponent. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1978.ImportedFEComponent)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_mass_disc(self) -> '_1981.MassDisc':
        '''MassDisc: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1981.MassDisc.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MassDisc. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1981.MassDisc)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_measurement_component(self) -> '_1982.MeasurementComponent':
        '''MeasurementComponent: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.MeasurementComponent.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MeasurementComponent. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1982.MeasurementComponent)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_mountable_component(self) -> '_1983.MountableComponent':
        '''MountableComponent: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.MountableComponent.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MountableComponent. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1983.MountableComponent)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_oil_seal(self) -> '_1985.OilSeal':
        '''OilSeal: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1985.OilSeal.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to OilSeal. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1985.OilSeal)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_planet_carrier(self) -> '_1987.PlanetCarrier':
        '''PlanetCarrier: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.PlanetCarrier.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetCarrier. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1987.PlanetCarrier)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_point_load(self) -> '_1989.PointLoad':
        '''PointLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.PointLoad.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PointLoad. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1989.PointLoad)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power_load(self) -> '_1990.PowerLoad':
        '''PowerLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.PowerLoad.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerLoad. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1990.PowerLoad)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_unbalanced_mass(self) -> '_1995.UnbalancedMass':
        '''UnbalancedMass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1995.UnbalancedMass.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to UnbalancedMass. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1995.UnbalancedMass)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_virtual_component(self) -> '_1996.VirtualComponent':
        '''VirtualComponent: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.VirtualComponent.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to VirtualComponent. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1996.VirtualComponent)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_shaft(self) -> '_1999.Shaft':
        '''Shaft: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.Shaft.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Shaft. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_1999.Shaft)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_agma_gleason_conical_gear(self) -> '_2029.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2029.AGMAGleasonConicalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AGMAGleasonConicalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2029.AGMAGleasonConicalGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bevel_differential_gear(self) -> '_2031.BevelDifferentialGear':
        '''BevelDifferentialGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.BevelDifferentialGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2031.BevelDifferentialGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bevel_differential_planet_gear(self) -> '_2033.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.BevelDifferentialPlanetGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialPlanetGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2033.BevelDifferentialPlanetGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bevel_differential_sun_gear(self) -> '_2034.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2034.BevelDifferentialSunGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialSunGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2034.BevelDifferentialSunGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bevel_gear(self) -> '_2035.BevelGear':
        '''BevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.BevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2035.BevelGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_concept_gear(self) -> '_2037.ConceptGear':
        '''ConceptGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2037.ConceptGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2037.ConceptGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_conical_gear(self) -> '_2039.ConicalGear':
        '''ConicalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2039.ConicalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConicalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2039.ConicalGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_gear(self) -> '_2041.CylindricalGear':
        '''CylindricalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2041.CylindricalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2041.CylindricalGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_planet_gear(self) -> '_2043.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2043.CylindricalPlanetGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalPlanetGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2043.CylindricalPlanetGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_face_gear(self) -> '_2044.FaceGear':
        '''FaceGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2044.FaceGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FaceGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2044.FaceGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_gear(self) -> '_2046.Gear':
        '''Gear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2046.Gear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Gear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2046.Gear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_hypoid_gear(self) -> '_2050.HypoidGear':
        '''HypoidGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2050.HypoidGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HypoidGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2050.HypoidGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2052.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2052.KlingelnbergCycloPalloidConicalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2052.KlingelnbergCycloPalloidConicalGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2054.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2054.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2054.KlingelnbergCycloPalloidHypoidGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2056.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2056.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2056.KlingelnbergCycloPalloidSpiralBevelGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_spiral_bevel_gear(self) -> '_2059.SpiralBevelGear':
        '''SpiralBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2059.SpiralBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpiralBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2059.SpiralBevelGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_diff_gear(self) -> '_2061.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2061.StraightBevelDiffGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelDiffGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2061.StraightBevelDiffGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_gear(self) -> '_2063.StraightBevelGear':
        '''StraightBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2063.StraightBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2063.StraightBevelGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_planet_gear(self) -> '_2065.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2065.StraightBevelPlanetGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelPlanetGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2065.StraightBevelPlanetGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_sun_gear(self) -> '_2066.StraightBevelSunGear':
        '''StraightBevelSunGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.StraightBevelSunGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelSunGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2066.StraightBevelSunGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_worm_gear(self) -> '_2067.WormGear':
        '''WormGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.WormGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WormGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2067.WormGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_zerol_bevel_gear(self) -> '_2069.ZerolBevelGear':
        '''ZerolBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2069.ZerolBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ZerolBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2069.ZerolBevelGear)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_clutch_half(self) -> '_2091.ClutchHalf':
        '''ClutchHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2091.ClutchHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ClutchHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2091.ClutchHalf)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_concept_coupling_half(self) -> '_2094.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2094.ConceptCouplingHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptCouplingHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2094.ConceptCouplingHalf)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_coupling_half(self) -> '_2096.CouplingHalf':
        '''CouplingHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2096.CouplingHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CouplingHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2096.CouplingHalf)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cvt_pulley(self) -> '_2098.CVTPulley':
        '''CVTPulley: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2098.CVTPulley.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CVTPulley. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2098.CVTPulley)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_part_to_part_shear_coupling_half(self) -> '_2100.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2100.PartToPartShearCouplingHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PartToPartShearCouplingHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2100.PartToPartShearCouplingHalf)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_pulley(self) -> '_2101.Pulley':
        '''Pulley: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2101.Pulley.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Pulley. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2101.Pulley)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_rolling_ring(self) -> '_2107.RollingRing':
        '''RollingRing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2107.RollingRing.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RollingRing. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2107.RollingRing)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_shaft_hub_connection(self) -> '_2109.ShaftHubConnection':
        '''ShaftHubConnection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2109.ShaftHubConnection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ShaftHubConnection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2109.ShaftHubConnection)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_spring_damper_half(self) -> '_2111.SpringDamperHalf':
        '''SpringDamperHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2111.SpringDamperHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpringDamperHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2111.SpringDamperHalf)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_synchroniser_half(self) -> '_2114.SynchroniserHalf':
        '''SynchroniserHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.SynchroniserHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SynchroniserHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2114.SynchroniserHalf)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_synchroniser_part(self) -> '_2115.SynchroniserPart':
        '''SynchroniserPart: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2115.SynchroniserPart.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SynchroniserPart. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2115.SynchroniserPart)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_synchroniser_sleeve(self) -> '_2116.SynchroniserSleeve':
        '''SynchroniserSleeve: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2116.SynchroniserSleeve.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SynchroniserSleeve. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2116.SynchroniserSleeve)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_torque_converter_pump(self) -> '_2118.TorqueConverterPump':
        '''TorqueConverterPump: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2118.TorqueConverterPump.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterPump. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2118.TorqueConverterPump)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_torque_converter_turbine(self) -> '_2120.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2120.TorqueConverterTurbine.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterTurbine. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2120.TorqueConverterTurbine)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1966.Component]':
        '''List[Component]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1966.Component))
        return value


class ListWithSelectedItem_ImportedFE(_1912.ImportedFE, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ImportedFE

    A specific implementation of 'ListWithSelectedItem' for 'ImportedFE' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'ImportedFE'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ImportedFE.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_1912.ImportedFE.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1912.ImportedFE.TYPE

    @property
    def selected_value(self) -> '_1912.ImportedFE':
        '''ImportedFE: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1912.ImportedFE)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1912.ImportedFE]':
        '''List[ImportedFE]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1912.ImportedFE))
        return value


class ListWithSelectedItem_GuideDxfModel(_1975.GuideDxfModel, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_GuideDxfModel

    A specific implementation of 'ListWithSelectedItem' for 'GuideDxfModel' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'GuideDxfModel'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_GuideDxfModel.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_1975.GuideDxfModel.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1975.GuideDxfModel.TYPE

    @property
    def selected_value(self) -> '_1975.GuideDxfModel':
        '''GuideDxfModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1975.GuideDxfModel)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1975.GuideDxfModel]':
        '''List[GuideDxfModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1975.GuideDxfModel))
        return value


class ListWithSelectedItem_ConcentricPartGroup(_2004.ConcentricPartGroup, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ConcentricPartGroup

    A specific implementation of 'ListWithSelectedItem' for 'ConcentricPartGroup' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'ConcentricPartGroup'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ConcentricPartGroup.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_2004.ConcentricPartGroup.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2004.ConcentricPartGroup.TYPE

    @property
    def selected_value(self) -> '_2004.ConcentricPartGroup':
        '''ConcentricPartGroup: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2004.ConcentricPartGroup)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2004.ConcentricPartGroup]':
        '''List[ConcentricPartGroup]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2004.ConcentricPartGroup))
        return value


class ListWithSelectedItem_GearSetDesign(_705.GearSetDesign, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_GearSetDesign

    A specific implementation of 'ListWithSelectedItem' for 'GearSetDesign' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'GearSetDesign'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_GearSetDesign.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_705.GearSetDesign.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _705.GearSetDesign.TYPE

    @property
    def selected_value(self) -> '_705.GearSetDesign':
        '''GearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_705.GearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_zerol_bevel_gear_set_design(self) -> '_709.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _709.ZerolBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ZerolBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_709.ZerolBevelGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_worm_gear_set_design(self) -> '_714.WormGearSetDesign':
        '''WormGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _714.WormGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WormGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_714.WormGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_diff_gear_set_design(self) -> '_718.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _718.StraightBevelDiffGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_718.StraightBevelDiffGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_gear_set_design(self) -> '_722.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _722.StraightBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_722.StraightBevelGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_spiral_bevel_gear_set_design(self) -> '_726.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _726.SpiralBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpiralBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_726.SpiralBevelGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_730.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _730.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_730.KlingelnbergCycloPalloidSpiralBevelGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_734.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _734.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_734.KlingelnbergCycloPalloidHypoidGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_conical_gear_set_design(self) -> '_738.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _738.KlingelnbergConicalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_738.KlingelnbergConicalGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_hypoid_gear_set_design(self) -> '_742.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _742.HypoidGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HypoidGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_742.HypoidGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_face_gear_set_design(self) -> '_750.FaceGearSetDesign':
        '''FaceGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _750.FaceGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FaceGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_750.FaceGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_gear_set_design(self) -> '_777.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _777.CylindricalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_777.CylindricalGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_planetary_gear_set_design(self) -> '_786.CylindricalPlanetaryGearSetDesign':
        '''CylindricalPlanetaryGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _786.CylindricalPlanetaryGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalPlanetaryGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_786.CylindricalPlanetaryGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_conical_gear_set_design(self) -> '_880.ConicalGearSetDesign':
        '''ConicalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _880.ConicalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConicalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_880.ConicalGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_concept_gear_set_design(self) -> '_902.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _902.ConceptGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_902.ConceptGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bevel_gear_set_design(self) -> '_906.BevelGearSetDesign':
        '''BevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _906.BevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_906.BevelGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_agma_gleason_conical_gear_set_design(self) -> '_919.AGMAGleasonConicalGearSetDesign':
        '''AGMAGleasonConicalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _919.AGMAGleasonConicalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_919.AGMAGleasonConicalGearSetDesign)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_705.GearSetDesign]':
        '''List[GearSetDesign]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_705.GearSetDesign))
        return value


class ListWithSelectedItem_ShaftHubConnection(_2109.ShaftHubConnection, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ShaftHubConnection

    A specific implementation of 'ListWithSelectedItem' for 'ShaftHubConnection' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'ShaftHubConnection'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ShaftHubConnection.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_2109.ShaftHubConnection.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2109.ShaftHubConnection.TYPE

    @property
    def selected_value(self) -> '_2109.ShaftHubConnection':
        '''ShaftHubConnection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2109.ShaftHubConnection)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2109.ShaftHubConnection]':
        '''List[ShaftHubConnection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2109.ShaftHubConnection))
        return value


class ListWithSelectedItem_TSelectableItem(Generic[TSelectableItem], mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_TSelectableItem

    A specific implementation of 'ListWithSelectedItem' for 'TSelectableItem' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'TSelectableItem'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_TSelectableItem.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> 'TSelectableItem':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return TSelectableItem

    @property
    def selected_value(self) -> 'TSelectableItem':
        '''TSelectableItem: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(TSelectableItem)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[TSelectableItem]':
        '''List[TSelectableItem]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(TSelectableItem))
        return value


class ListWithSelectedItem_CylindricalGearSystemDeflection(_2233.CylindricalGearSystemDeflection, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearSystemDeflection

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearSystemDeflection' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'CylindricalGearSystemDeflection'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_2233.CylindricalGearSystemDeflection.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2233.CylindricalGearSystemDeflection.TYPE

    @property
    def selected_value(self) -> '_2233.CylindricalGearSystemDeflection':
        '''CylindricalGearSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2233.CylindricalGearSystemDeflection)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_gear_system_deflection_timestep(self) -> '_2234.CylindricalGearSystemDeflectionTimestep':
        '''CylindricalGearSystemDeflectionTimestep: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2234.CylindricalGearSystemDeflectionTimestep.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSystemDeflectionTimestep. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2234.CylindricalGearSystemDeflectionTimestep)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_gear_system_deflection_with_ltca_results(self) -> '_2235.CylindricalGearSystemDeflectionWithLTCAResults':
        '''CylindricalGearSystemDeflectionWithLTCAResults: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2235.CylindricalGearSystemDeflectionWithLTCAResults.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2235.CylindricalGearSystemDeflectionWithLTCAResults)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_planet_gear_system_deflection(self) -> '_2236.CylindricalPlanetGearSystemDeflection':
        '''CylindricalPlanetGearSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2236.CylindricalPlanetGearSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalPlanetGearSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2236.CylindricalPlanetGearSystemDeflection)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2233.CylindricalGearSystemDeflection]':
        '''List[CylindricalGearSystemDeflection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2233.CylindricalGearSystemDeflection))
        return value


class ListWithSelectedItem_DesignState(_5214.DesignState, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_DesignState

    A specific implementation of 'ListWithSelectedItem' for 'DesignState' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'DesignState'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_DesignState.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_5214.DesignState.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5214.DesignState.TYPE

    @property
    def selected_value(self) -> '_5214.DesignState':
        '''DesignState: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5214.DesignState)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_5214.DesignState]':
        '''List[DesignState]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5214.DesignState))
        return value


class ListWithSelectedItem_ImportedFEComponent(_1978.ImportedFEComponent, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ImportedFEComponent

    A specific implementation of 'ListWithSelectedItem' for 'ImportedFEComponent' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'ImportedFEComponent'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ImportedFEComponent.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_1978.ImportedFEComponent.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1978.ImportedFEComponent.TYPE

    @property
    def selected_value(self) -> '_1978.ImportedFEComponent':
        '''ImportedFEComponent: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1978.ImportedFEComponent)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1978.ImportedFEComponent]':
        '''List[ImportedFEComponent]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1978.ImportedFEComponent))
        return value


class ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis(_5308.ImportedFEComponentGearWhineAnalysis, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis

    A specific implementation of 'ListWithSelectedItem' for 'ImportedFEComponentGearWhineAnalysis' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'ImportedFEComponentGearWhineAnalysis'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ImportedFEComponentGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_5308.ImportedFEComponentGearWhineAnalysis.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5308.ImportedFEComponentGearWhineAnalysis.TYPE

    @property
    def selected_value(self) -> '_5308.ImportedFEComponentGearWhineAnalysis':
        '''ImportedFEComponentGearWhineAnalysis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5308.ImportedFEComponentGearWhineAnalysis)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_5308.ImportedFEComponentGearWhineAnalysis]':
        '''List[ImportedFEComponentGearWhineAnalysis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5308.ImportedFEComponentGearWhineAnalysis))
        return value


class ListWithSelectedItem_ResultLocationSelectionGroup(_5382.ResultLocationSelectionGroup, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ResultLocationSelectionGroup

    A specific implementation of 'ListWithSelectedItem' for 'ResultLocationSelectionGroup' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'ResultLocationSelectionGroup'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ResultLocationSelectionGroup.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_5382.ResultLocationSelectionGroup.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5382.ResultLocationSelectionGroup.TYPE

    @property
    def selected_value(self) -> '_5382.ResultLocationSelectionGroup':
        '''ResultLocationSelectionGroup: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5382.ResultLocationSelectionGroup)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_5382.ResultLocationSelectionGroup]':
        '''List[ResultLocationSelectionGroup]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5382.ResultLocationSelectionGroup))
        return value


class ListWithSelectedItem_StaticLoadCase(_6161.StaticLoadCase, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_StaticLoadCase

    A specific implementation of 'ListWithSelectedItem' for 'StaticLoadCase' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'StaticLoadCase'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_StaticLoadCase.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_6161.StaticLoadCase.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6161.StaticLoadCase.TYPE

    @property
    def selected_value(self) -> '_6161.StaticLoadCase':
        '''StaticLoadCase: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6161.StaticLoadCase)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_6161.StaticLoadCase]':
        '''List[StaticLoadCase]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_6161.StaticLoadCase))
        return value


class ListWithSelectedItem_DutyCycle(_5215.DutyCycle, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_DutyCycle

    A specific implementation of 'ListWithSelectedItem' for 'DutyCycle' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'DutyCycle'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_DutyCycle.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_5215.DutyCycle.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5215.DutyCycle.TYPE

    @property
    def selected_value(self) -> '_5215.DutyCycle':
        '''DutyCycle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5215.DutyCycle)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_5215.DutyCycle]':
        '''List[DutyCycle]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5215.DutyCycle))
        return value


class ListWithSelectedItem_float(float, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_float

    A specific implementation of 'ListWithSelectedItem' for 'float' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'float'

    def __new__(cls, instance_to_wrap: 'ListWithSelectedItem_float.TYPE'):
        return float.__new__(cls, instance_to_wrap.SelectedValue) if instance_to_wrap.SelectedValue else 0.0

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_float.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> 'float':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return float

    @property
    def selected_value(self) -> 'float':
        '''float: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[float]':
        '''List[float]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.enclosing.AvailableValues)
        return value


class ListWithSelectedItem_ElectricMachineDataSet(_1902.ElectricMachineDataSet, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ElectricMachineDataSet

    A specific implementation of 'ListWithSelectedItem' for 'ElectricMachineDataSet' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'ElectricMachineDataSet'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ElectricMachineDataSet.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_1902.ElectricMachineDataSet.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1902.ElectricMachineDataSet.TYPE

    @property
    def selected_value(self) -> '_1902.ElectricMachineDataSet':
        '''ElectricMachineDataSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1902.ElectricMachineDataSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1902.ElectricMachineDataSet]':
        '''List[ElectricMachineDataSet]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1902.ElectricMachineDataSet))
        return value


class ListWithSelectedItem_CylindricalGearSet(_2042.CylindricalGearSet, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearSet

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearSet' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'CylindricalGearSet'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearSet.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_2042.CylindricalGearSet.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2042.CylindricalGearSet.TYPE

    @property
    def selected_value(self) -> '_2042.CylindricalGearSet':
        '''CylindricalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2042.CylindricalGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2042.CylindricalGearSet]':
        '''List[CylindricalGearSet]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2042.CylindricalGearSet))
        return value


class ListWithSelectedItem_PointLoad(_1989.PointLoad, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_PointLoad

    A specific implementation of 'ListWithSelectedItem' for 'PointLoad' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'PointLoad'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_PointLoad.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_1989.PointLoad.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1989.PointLoad.TYPE

    @property
    def selected_value(self) -> '_1989.PointLoad':
        '''PointLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1989.PointLoad)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1989.PointLoad]':
        '''List[PointLoad]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1989.PointLoad))
        return value


class ListWithSelectedItem_GearSet(_2048.GearSet, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_GearSet

    A specific implementation of 'ListWithSelectedItem' for 'GearSet' types.
    '''

    TYPE = _LIST_WITH_SELECTED_ITEM

    __hash__ = None
    __qualname__ = 'GearSet'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_GearSet.TYPE'):
        super().__init__(instance_to_wrap.SelectedValue)
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass

    @classmethod
    def implicit_type(cls) -> '_2048.GearSet.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2048.GearSet.TYPE

    @property
    def selected_value(self) -> '_2048.GearSet':
        '''GearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2048.GearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_agma_gleason_conical_gear_set(self) -> '_2030.AGMAGleasonConicalGearSet':
        '''AGMAGleasonConicalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2030.AGMAGleasonConicalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AGMAGleasonConicalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2030.AGMAGleasonConicalGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bevel_differential_gear_set(self) -> '_2032.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2032.BevelDifferentialGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2032.BevelDifferentialGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bevel_gear_set(self) -> '_2036.BevelGearSet':
        '''BevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2036.BevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2036.BevelGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_concept_gear_set(self) -> '_2038.ConceptGearSet':
        '''ConceptGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2038.ConceptGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2038.ConceptGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_conical_gear_set(self) -> '_2040.ConicalGearSet':
        '''ConicalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2040.ConicalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConicalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2040.ConicalGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_gear_set(self) -> '_2042.CylindricalGearSet':
        '''CylindricalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2042.CylindricalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2042.CylindricalGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_face_gear_set(self) -> '_2045.FaceGearSet':
        '''FaceGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2045.FaceGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FaceGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2045.FaceGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_hypoid_gear_set(self) -> '_2051.HypoidGearSet':
        '''HypoidGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2051.HypoidGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HypoidGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2051.HypoidGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2053.KlingelnbergCycloPalloidConicalGearSet':
        '''KlingelnbergCycloPalloidConicalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2053.KlingelnbergCycloPalloidConicalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2053.KlingelnbergCycloPalloidConicalGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2055.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2055.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2055.KlingelnbergCycloPalloidHypoidGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2057.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2057.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2057.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_planetary_gear_set(self) -> '_2058.PlanetaryGearSet':
        '''PlanetaryGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2058.PlanetaryGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetaryGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2058.PlanetaryGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_spiral_bevel_gear_set(self) -> '_2060.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2060.SpiralBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpiralBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2060.SpiralBevelGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_diff_gear_set(self) -> '_2062.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2062.StraightBevelDiffGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelDiffGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2062.StraightBevelDiffGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_gear_set(self) -> '_2064.StraightBevelGearSet':
        '''StraightBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2064.StraightBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2064.StraightBevelGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_worm_gear_set(self) -> '_2068.WormGearSet':
        '''WormGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2068.WormGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WormGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2068.WormGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_zerol_bevel_gear_set(self) -> '_2070.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2070.ZerolBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ZerolBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new(_2070.ZerolBevelGearSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2048.GearSet]':
        '''List[GearSet]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2048.GearSet))
        return value
