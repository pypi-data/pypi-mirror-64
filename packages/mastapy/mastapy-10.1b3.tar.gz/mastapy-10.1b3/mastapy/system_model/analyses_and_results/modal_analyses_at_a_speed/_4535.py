﻿'''_4535.py

StraightBevelGearModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.gears import _2063
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6165
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4448
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'StraightBevelGearModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearModalAnalysisAtASpeed',)


class StraightBevelGearModalAnalysisAtASpeed(_4448.BevelGearModalAnalysisAtASpeed):
    '''StraightBevelGearModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2063.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2063.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6165.StraightBevelGearLoadCase':
        '''StraightBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6165.StraightBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
