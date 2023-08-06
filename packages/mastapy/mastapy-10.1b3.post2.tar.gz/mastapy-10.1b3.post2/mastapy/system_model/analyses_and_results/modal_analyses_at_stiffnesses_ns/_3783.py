'''_3783.py

PulleyModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.couplings import _2101
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6144
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3734
from mastapy._internal.python_net import python_net_import

_PULLEY_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'PulleyModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyModalAnalysesAtStiffnesses',)


class PulleyModalAnalysesAtStiffnesses(_3734.CouplingHalfModalAnalysesAtStiffnesses):
    '''PulleyModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _PULLEY_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2101.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2101.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6144.PulleyLoadCase':
        '''PulleyLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6144.PulleyLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
