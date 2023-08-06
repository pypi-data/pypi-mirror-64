'''_3767.py

FaceGearModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.gears import _2064
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6110
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3771
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'FaceGearModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearModalAnalysesAtStiffnesses',)


class FaceGearModalAnalysesAtStiffnesses(_3771.GearModalAnalysesAtStiffnesses):
    '''FaceGearModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2064.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2064.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6110.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6110.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
