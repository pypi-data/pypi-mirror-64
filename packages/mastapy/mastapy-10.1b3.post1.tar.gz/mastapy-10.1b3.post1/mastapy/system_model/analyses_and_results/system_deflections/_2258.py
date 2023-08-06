'''_2258.py

ExternalCADModelSystemDeflection
'''


from mastapy.system_model.part_model import _1993
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6109
from mastapy.system_model.analyses_and_results.power_flows import _3260
from mastapy.system_model.analyses_and_results.system_deflections import _2227
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ExternalCADModelSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelSystemDeflection',)


class ExternalCADModelSystemDeflection(_2227.ComponentSystemDeflection):
    '''ExternalCADModelSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1993.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1993.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6109.ExternalCADModelLoadCase':
        '''ExternalCADModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6109.ExternalCADModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3260.ExternalCADModelPowerFlow':
        '''ExternalCADModelPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3260.ExternalCADModelPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
