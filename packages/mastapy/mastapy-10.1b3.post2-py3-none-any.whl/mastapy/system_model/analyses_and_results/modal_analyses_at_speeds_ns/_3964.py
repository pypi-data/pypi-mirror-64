'''_3964.py

ClutchModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.couplings import _2090
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6046
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3980
from mastapy._internal.python_net import python_net_import

_CLUTCH_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'ClutchModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchModalAnalysesAtSpeeds',)


class ClutchModalAnalysesAtSpeeds(_3980.CouplingModalAnalysesAtSpeeds):
    '''ClutchModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2090.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2090.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6046.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6046.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
