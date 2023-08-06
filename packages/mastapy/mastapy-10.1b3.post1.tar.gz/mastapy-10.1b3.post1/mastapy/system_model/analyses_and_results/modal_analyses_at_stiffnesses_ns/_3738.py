'''_3738.py

ClutchHalfModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.couplings import _2111
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6065
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3754
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'ClutchHalfModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfModalAnalysesAtStiffnesses',)


class ClutchHalfModalAnalysesAtStiffnesses(_3754.CouplingHalfModalAnalysesAtStiffnesses):
    '''ClutchHalfModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2111.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2111.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6065.ClutchHalfLoadCase':
        '''ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6065.ClutchHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
