'''_4014.py

MeasurementComponentModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model import _1982
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6126
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4061
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'MeasurementComponentModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentModalAnalysesAtSpeeds',)


class MeasurementComponentModalAnalysesAtSpeeds(_4061.VirtualComponentModalAnalysesAtSpeeds):
    '''MeasurementComponentModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1982.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1982.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6126.MeasurementComponentLoadCase':
        '''MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6126.MeasurementComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
