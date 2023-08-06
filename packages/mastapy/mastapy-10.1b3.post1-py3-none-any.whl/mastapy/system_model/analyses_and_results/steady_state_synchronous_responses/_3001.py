'''_3001.py

CVTSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.couplings import _2117
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2969
from mastapy._internal.python_net import python_net_import

_CVT_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'CVTSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTSteadyStateSynchronousResponse',)


class CVTSteadyStateSynchronousResponse(_2969.BeltDriveSteadyStateSynchronousResponse):
    '''CVTSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CVT_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2117.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2117.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
