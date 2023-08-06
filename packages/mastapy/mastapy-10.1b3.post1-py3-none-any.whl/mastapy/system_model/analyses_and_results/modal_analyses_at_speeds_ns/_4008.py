'''_4008.py

DatumModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model import _1990
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6096
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3986
from mastapy._internal.python_net import python_net_import

_DATUM_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'DatumModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumModalAnalysesAtSpeeds',)


class DatumModalAnalysesAtSpeeds(_3986.ComponentModalAnalysesAtSpeeds):
    '''DatumModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _DATUM_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumModalAnalysesAtSpeeds.TYPE'):
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
