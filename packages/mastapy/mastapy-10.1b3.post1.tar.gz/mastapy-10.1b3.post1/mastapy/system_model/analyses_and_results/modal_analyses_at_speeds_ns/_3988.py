'''_3988.py

ConceptCouplingHalfModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.couplings import _2114
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6070
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3999
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'ConceptCouplingHalfModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfModalAnalysesAtSpeeds',)


class ConceptCouplingHalfModalAnalysesAtSpeeds(_3999.CouplingHalfModalAnalysesAtSpeeds):
    '''ConceptCouplingHalfModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2114.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6070.ConceptCouplingHalfLoadCase':
        '''ConceptCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6070.ConceptCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
