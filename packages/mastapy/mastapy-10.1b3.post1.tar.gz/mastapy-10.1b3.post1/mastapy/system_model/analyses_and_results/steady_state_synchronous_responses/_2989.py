'''_2989.py

ConceptGearSetSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2058
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6074
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2990, _2988, _3014
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'ConceptGearSetSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetSteadyStateSynchronousResponse',)


class ConceptGearSetSteadyStateSynchronousResponse(_3014.GearSetSteadyStateSynchronousResponse):
    '''ConceptGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2058.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2058.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6074.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6074.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def concept_gears_steady_state_synchronous_response(self) -> 'List[_2990.ConceptGearSteadyStateSynchronousResponse]':
        '''List[ConceptGearSteadyStateSynchronousResponse]: 'ConceptGearsSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsSteadyStateSynchronousResponse, constructor.new(_2990.ConceptGearSteadyStateSynchronousResponse))
        return value

    @property
    def concept_meshes_steady_state_synchronous_response(self) -> 'List[_2988.ConceptGearMeshSteadyStateSynchronousResponse]':
        '''List[ConceptGearMeshSteadyStateSynchronousResponse]: 'ConceptMeshesSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesSteadyStateSynchronousResponse, constructor.new(_2988.ConceptGearMeshSteadyStateSynchronousResponse))
        return value
