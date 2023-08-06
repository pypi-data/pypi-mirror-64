'''_5331.py

PointLoadGearWhineAnalysis
'''


from mastapy.system_model.part_model import _1989
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6142
from mastapy.system_model.analyses_and_results.system_deflections import _2275
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5368
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'PointLoadGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadGearWhineAnalysis',)


class PointLoadGearWhineAnalysis(_5368.VirtualComponentGearWhineAnalysis):
    '''PointLoadGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1989.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1989.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6142.PointLoadLoadCase':
        '''PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6142.PointLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2275.PointLoadSystemDeflection':
        '''PointLoadSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2275.PointLoadSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
