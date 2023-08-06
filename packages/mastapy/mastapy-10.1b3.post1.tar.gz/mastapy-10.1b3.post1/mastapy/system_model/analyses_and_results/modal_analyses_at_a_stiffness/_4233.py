'''_4233.py

ConceptCouplingConnectionModalAnalysisAtAStiffness
'''


from mastapy.system_model.connections_and_sockets.couplings import _1894
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6069
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4244
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'ConceptCouplingConnectionModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionModalAnalysisAtAStiffness',)


class ConceptCouplingConnectionModalAnalysisAtAStiffness(_4244.CouplingConnectionModalAnalysisAtAStiffness):
    '''ConceptCouplingConnectionModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_CONNECTION_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1894.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1894.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6069.ConceptCouplingConnectionLoadCase':
        '''ConceptCouplingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6069.ConceptCouplingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
