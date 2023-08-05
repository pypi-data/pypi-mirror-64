'''_4234.py

DatumModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model import _1970
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6076
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4212
from mastapy._internal.python_net import python_net_import

_DATUM_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'DatumModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumModalAnalysisAtAStiffness',)


class DatumModalAnalysisAtAStiffness(_4212.ComponentModalAnalysisAtAStiffness):
    '''DatumModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _DATUM_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1970.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1970.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6076.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6076.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
