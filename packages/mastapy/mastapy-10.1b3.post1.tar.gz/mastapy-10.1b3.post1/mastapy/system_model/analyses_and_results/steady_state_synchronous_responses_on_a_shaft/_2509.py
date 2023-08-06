'''_2509.py

ConnectorSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model import _1989, _1982, _2005
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.couplings import _2129
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _2546
from mastapy._internal.python_net import python_net_import

_CONNECTOR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'ConnectorSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorSteadyStateSynchronousResponseOnAShaft',)


class ConnectorSteadyStateSynchronousResponseOnAShaft(_2546.MountableComponentSteadyStateSynchronousResponseOnAShaft):
    '''ConnectorSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectorSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1989.Connector':
        '''Connector: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1989.Connector)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bearing(self) -> '_1982.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.Bearing.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Bearing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1982.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_oil_seal(self) -> '_2005.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.OilSeal.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to OilSeal. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2005.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft_hub_connection(self) -> '_2129.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2129.ShaftHubConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ShaftHubConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2129.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
