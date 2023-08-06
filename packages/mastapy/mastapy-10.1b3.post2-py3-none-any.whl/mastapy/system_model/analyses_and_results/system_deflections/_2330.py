'''_2330.py

TorqueConverterPumpSystemDeflection
'''


from mastapy.system_model.part_model.couplings import _2138
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6198
from mastapy.system_model.analyses_and_results.power_flows import _3328
from mastapy.system_model.analyses_and_results.system_deflections import _2242
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'TorqueConverterPumpSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpSystemDeflection',)


class TorqueConverterPumpSystemDeflection(_2242.CouplingHalfSystemDeflection):
    '''TorqueConverterPumpSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2138.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2138.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6198.TorqueConverterPumpLoadCase':
        '''TorqueConverterPumpLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6198.TorqueConverterPumpLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3328.TorqueConverterPumpPowerFlow':
        '''TorqueConverterPumpPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3328.TorqueConverterPumpPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
