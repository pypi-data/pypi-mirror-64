'''_2224.py

ClutchHalfSystemDeflection
'''


from mastapy.system_model.part_model.couplings import _2111
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6065
from mastapy.system_model.analyses_and_results.power_flows import _3233
from mastapy.system_model.analyses_and_results.system_deflections import _2242
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ClutchHalfSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfSystemDeflection',)


class ClutchHalfSystemDeflection(_2242.CouplingHalfSystemDeflection):
    '''ClutchHalfSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2111.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2111.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6065.ClutchHalfLoadCase':
        '''ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6065.ClutchHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3233.ClutchHalfPowerFlow':
        '''ClutchHalfPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3233.ClutchHalfPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
