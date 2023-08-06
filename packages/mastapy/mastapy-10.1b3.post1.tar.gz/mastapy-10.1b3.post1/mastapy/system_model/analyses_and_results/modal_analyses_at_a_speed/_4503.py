'''_4503.py

FlexiblePinAssemblyModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model import _1994
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6113
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4544
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'FlexiblePinAssemblyModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyModalAnalysisAtASpeed',)


class FlexiblePinAssemblyModalAnalysisAtASpeed(_4544.SpecialisedAssemblyModalAnalysisAtASpeed):
    '''FlexiblePinAssemblyModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1994.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1994.FlexiblePinAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6113.FlexiblePinAssemblyLoadCase':
        '''FlexiblePinAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6113.FlexiblePinAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
