'''_1288.py

DynamicCustomReportItem
'''


from mastapy._internal import constructor
from mastapy.utility.report import (
    _1270, _1253, _1258, _1259,
    _1260, _1261, _1262, _1263,
    _1265, _1266, _1267, _1268,
    _1269, _1271, _1273, _1274,
    _1276, _1277, _1278, _1280,
    _1281, _1282, _1283, _1285,
    _1286
)
from mastapy.shafts import _20
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical import _781
from mastapy.utility_gui.charts import _1480, _1481
from mastapy.bearings.bearing_results import _1547, _1550, _1558
from mastapy.system_model.analyses_and_results.system_deflections.reporting import _2330
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3523
from mastapy.system_model.analyses_and_results.modal_analyses.reporting import _4811, _4815
from mastapy._internal.python_net import python_net_import

_DYNAMIC_CUSTOM_REPORT_ITEM = python_net_import('SMT.MastaAPI.Utility.Report', 'DynamicCustomReportItem')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicCustomReportItem',)


class DynamicCustomReportItem(_1277.CustomReportNameableItem):
    '''DynamicCustomReportItem

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_CUSTOM_REPORT_ITEM

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicCustomReportItem.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def is_main_report_item(self) -> 'bool':
        '''bool: 'IsMainReportItem' is the original name of this property.'''

        return self.wrapped.IsMainReportItem

    @is_main_report_item.setter
    def is_main_report_item(self, value: 'bool'):
        self.wrapped.IsMainReportItem = bool(value) if value else False

    @property
    def inner_item(self) -> '_1270.CustomReportItem':
        '''CustomReportItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1270.CustomReportItem)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_shaft_damage_results_table_and_chart(self) -> '_20.ShaftDamageResultsTableAndChart':
        '''ShaftDamageResultsTableAndChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _20.ShaftDamageResultsTableAndChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to ShaftDamageResultsTableAndChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_20.ShaftDamageResultsTableAndChart)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_cylindrical_gear_table_with_mg_charts(self) -> '_781.CylindricalGearTableWithMGCharts':
        '''CylindricalGearTableWithMGCharts: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _781.CylindricalGearTableWithMGCharts.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CylindricalGearTableWithMGCharts. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_781.CylindricalGearTableWithMGCharts)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_ad_hoc_custom_table(self) -> '_1253.AdHocCustomTable':
        '''AdHocCustomTable: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1253.AdHocCustomTable.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to AdHocCustomTable. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1253.AdHocCustomTable)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_chart(self) -> '_1258.CustomChart':
        '''CustomChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1258.CustomChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1258.CustomChart)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_graphic(self) -> '_1259.CustomGraphic':
        '''CustomGraphic: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1259.CustomGraphic.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomGraphic. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1259.CustomGraphic)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_image(self) -> '_1260.CustomImage':
        '''CustomImage: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1260.CustomImage.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomImage. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1260.CustomImage)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report(self) -> '_1261.CustomReport':
        '''CustomReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1261.CustomReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1261.CustomReport)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_cad_drawing(self) -> '_1262.CustomReportCadDrawing':
        '''CustomReportCadDrawing: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1262.CustomReportCadDrawing.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportCadDrawing. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1262.CustomReportCadDrawing)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_chart(self) -> '_1263.CustomReportChart':
        '''CustomReportChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1263.CustomReportChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1263.CustomReportChart)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_column(self) -> '_1265.CustomReportColumn':
        '''CustomReportColumn: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1265.CustomReportColumn.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportColumn. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1265.CustomReportColumn)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_columns(self) -> '_1266.CustomReportColumns':
        '''CustomReportColumns: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1266.CustomReportColumns.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportColumns. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1266.CustomReportColumns)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_definition_item(self) -> '_1267.CustomReportDefinitionItem':
        '''CustomReportDefinitionItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1267.CustomReportDefinitionItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportDefinitionItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1267.CustomReportDefinitionItem)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_horizontal_line(self) -> '_1268.CustomReportHorizontalLine':
        '''CustomReportHorizontalLine: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1268.CustomReportHorizontalLine.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportHorizontalLine. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1268.CustomReportHorizontalLine)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_html_item(self) -> '_1269.CustomReportHtmlItem':
        '''CustomReportHtmlItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1269.CustomReportHtmlItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportHtmlItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1269.CustomReportHtmlItem)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_item_container(self) -> '_1271.CustomReportItemContainer':
        '''CustomReportItemContainer: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1271.CustomReportItemContainer.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItemContainer. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1271.CustomReportItemContainer)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_item_container_collection_base(self) -> '_1273.CustomReportItemContainerCollectionBase':
        '''CustomReportItemContainerCollectionBase: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1273.CustomReportItemContainerCollectionBase.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItemContainerCollectionBase. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1273.CustomReportItemContainerCollectionBase)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_item_container_collection_item(self) -> '_1274.CustomReportItemContainerCollectionItem':
        '''CustomReportItemContainerCollectionItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1274.CustomReportItemContainerCollectionItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportItemContainerCollectionItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1274.CustomReportItemContainerCollectionItem)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_multi_property_item_base(self) -> '_1276.CustomReportMultiPropertyItemBase':
        '''CustomReportMultiPropertyItemBase: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1276.CustomReportMultiPropertyItemBase.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportMultiPropertyItemBase. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1276.CustomReportMultiPropertyItemBase)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_nameable_item(self) -> '_1277.CustomReportNameableItem':
        '''CustomReportNameableItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1277.CustomReportNameableItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportNameableItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1277.CustomReportNameableItem)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_named_item(self) -> '_1278.CustomReportNamedItem':
        '''CustomReportNamedItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1278.CustomReportNamedItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportNamedItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1278.CustomReportNamedItem)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_status_item(self) -> '_1280.CustomReportStatusItem':
        '''CustomReportStatusItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1280.CustomReportStatusItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportStatusItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1280.CustomReportStatusItem)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_tab(self) -> '_1281.CustomReportTab':
        '''CustomReportTab: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1281.CustomReportTab.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportTab. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1281.CustomReportTab)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_tabs(self) -> '_1282.CustomReportTabs':
        '''CustomReportTabs: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1282.CustomReportTabs.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportTabs. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1282.CustomReportTabs)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_report_text(self) -> '_1283.CustomReportText':
        '''CustomReportText: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1283.CustomReportText.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomReportText. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1283.CustomReportText)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_sub_report(self) -> '_1285.CustomSubReport':
        '''CustomSubReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1285.CustomSubReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomSubReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1285.CustomSubReport)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_table(self) -> '_1286.CustomTable':
        '''CustomTable: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1286.CustomTable.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomTable. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1286.CustomTable)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_dynamic_custom_report_item(self) -> 'DynamicCustomReportItem':
        '''DynamicCustomReportItem: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if DynamicCustomReportItem.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to DynamicCustomReportItem. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(DynamicCustomReportItem)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_line_chart(self) -> '_1480.CustomLineChart':
        '''CustomLineChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1480.CustomLineChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomLineChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1480.CustomLineChart)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_custom_table_and_chart(self) -> '_1481.CustomTableAndChart':
        '''CustomTableAndChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1481.CustomTableAndChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CustomTableAndChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1481.CustomTableAndChart)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_loaded_bearing_chart_reporter(self) -> '_1547.LoadedBearingChartReporter':
        '''LoadedBearingChartReporter: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1547.LoadedBearingChartReporter.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedBearingChartReporter. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1547.LoadedBearingChartReporter)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_loaded_bearing_temperature_chart(self) -> '_1550.LoadedBearingTemperatureChart':
        '''LoadedBearingTemperatureChart: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1550.LoadedBearingTemperatureChart.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedBearingTemperatureChart. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1550.LoadedBearingTemperatureChart)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_loaded_roller_element_chart_reporter(self) -> '_1558.LoadedRollerElementChartReporter':
        '''LoadedRollerElementChartReporter: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1558.LoadedRollerElementChartReporter.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to LoadedRollerElementChartReporter. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_1558.LoadedRollerElementChartReporter)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_shaft_system_deflection_sections_report(self) -> '_2330.ShaftSystemDeflectionSectionsReport':
        '''ShaftSystemDeflectionSectionsReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2330.ShaftSystemDeflectionSectionsReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to ShaftSystemDeflectionSectionsReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_2330.ShaftSystemDeflectionSectionsReport)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_parametric_study_histogram(self) -> '_3523.ParametricStudyHistogram':
        '''ParametricStudyHistogram: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3523.ParametricStudyHistogram.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to ParametricStudyHistogram. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_3523.ParametricStudyHistogram)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_campbell_diagram_report(self) -> '_4811.CampbellDiagramReport':
        '''CampbellDiagramReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4811.CampbellDiagramReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to CampbellDiagramReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_4811.CampbellDiagramReport)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None

    @property
    def inner_item_of_type_per_mode_results_report(self) -> '_4815.PerModeResultsReport':
        '''PerModeResultsReport: 'InnerItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _4815.PerModeResultsReport.TYPE not in self.wrapped.InnerItem.__class__.__mro__:
            raise CastException('Failed to cast inner_item to PerModeResultsReport. Expected: {}.'.format(self.wrapped.InnerItem.__class__.__qualname__))

        return constructor.new(_4815.PerModeResultsReport)(self.wrapped.InnerItem) if self.wrapped.InnerItem else None
