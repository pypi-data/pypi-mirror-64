'''_2302.py

SynchroniserHalfSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections import _2203, _2303
from mastapy._internal import constructor
from mastapy.system_model.part_model.couplings import _2114
from mastapy.system_model.analyses_and_results.static_loads import _6170
from mastapy.system_model.analyses_and_results.power_flows import _3301
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'SynchroniserHalfSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfSystemDeflection',)


class SynchroniserHalfSystemDeflection(_2303.SynchroniserPartSystemDeflection):
    '''SynchroniserHalfSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def clutch_connection(self) -> '_2203.ClutchConnectionSystemDeflection':
        '''ClutchConnectionSystemDeflection: 'ClutchConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2203.ClutchConnectionSystemDeflection)(self.wrapped.ClutchConnection) if self.wrapped.ClutchConnection else None

    @property
    def component_design(self) -> '_2114.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6170.SynchroniserHalfLoadCase':
        '''SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6170.SynchroniserHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3301.SynchroniserHalfPowerFlow':
        '''SynchroniserHalfPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3301.SynchroniserHalfPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
