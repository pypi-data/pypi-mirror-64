'''_3366.py

FaceGearCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2044
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3242
from mastapy.system_model.analyses_and_results.power_flows.compound import _3370
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'FaceGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearCompoundPowerFlow',)


class FaceGearCompoundPowerFlow(_3370.GearCompoundPowerFlow):
    '''FaceGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2044.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2044.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3242.FaceGearPowerFlow]':
        '''List[FaceGearPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3242.FaceGearPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3242.FaceGearPowerFlow]':
        '''List[FaceGearPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3242.FaceGearPowerFlow))
        return value
