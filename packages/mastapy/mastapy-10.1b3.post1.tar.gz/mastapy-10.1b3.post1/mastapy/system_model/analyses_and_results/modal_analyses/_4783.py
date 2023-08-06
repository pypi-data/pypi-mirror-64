'''_4783.py

PointLoadModalAnalysis
'''


from mastapy.system_model.part_model import _2009
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6162
from mastapy.system_model.analyses_and_results.system_deflections import _2295
from mastapy.system_model.analyses_and_results.modal_analyses import _4818
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'PointLoadModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadModalAnalysis',)


class PointLoadModalAnalysis(_4818.VirtualComponentModalAnalysis):
    '''PointLoadModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2009.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2009.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6162.PointLoadLoadCase':
        '''PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6162.PointLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2295.PointLoadSystemDeflection':
        '''PointLoadSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2295.PointLoadSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
