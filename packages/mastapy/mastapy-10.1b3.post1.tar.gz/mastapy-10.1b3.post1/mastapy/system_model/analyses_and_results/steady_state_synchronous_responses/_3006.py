'''_3006.py

DatumSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model import _1990
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6096
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2984
from mastapy._internal.python_net import python_net_import

_DATUM_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'DatumSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumSteadyStateSynchronousResponse',)


class DatumSteadyStateSynchronousResponse(_2984.ComponentSteadyStateSynchronousResponse):
    '''DatumSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _DATUM_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1990.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1990.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6096.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6096.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
