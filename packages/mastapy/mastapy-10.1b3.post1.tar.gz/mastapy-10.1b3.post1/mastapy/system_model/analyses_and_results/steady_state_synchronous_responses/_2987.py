'''_2987.py

ConceptCouplingSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.couplings import _2113
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6071
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2998
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'ConceptCouplingSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingSteadyStateSynchronousResponse',)


class ConceptCouplingSteadyStateSynchronousResponse(_2998.CouplingSteadyStateSynchronousResponse):
    '''ConceptCouplingSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2113.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2113.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6071.ConceptCouplingLoadCase':
        '''ConceptCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6071.ConceptCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
