﻿'''_3992.py

FaceGearModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.gears import _2044
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6090
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3996
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'FaceGearModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearModalAnalysesAtSpeeds',)


class FaceGearModalAnalysesAtSpeeds(_3996.GearModalAnalysesAtSpeeds):
    '''FaceGearModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2044.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2044.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6090.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6090.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
