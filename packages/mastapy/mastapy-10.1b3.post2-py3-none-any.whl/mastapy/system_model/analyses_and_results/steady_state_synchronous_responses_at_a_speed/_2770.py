'''_2770.py

OilSealSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.part_model import _1985
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6130
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2732
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'OilSealSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealSteadyStateSynchronousResponseAtASpeed',)


class OilSealSteadyStateSynchronousResponseAtASpeed(_2732.ConnectorSteadyStateSynchronousResponseAtASpeed):
    '''OilSealSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1985.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6130.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6130.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
