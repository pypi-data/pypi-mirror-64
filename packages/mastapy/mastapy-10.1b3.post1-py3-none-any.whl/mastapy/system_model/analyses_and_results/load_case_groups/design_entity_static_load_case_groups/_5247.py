'''_5247.py

GearSetStaticLoadCaseGroup
'''


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import _5244, _5245, _5246
from mastapy.system_model.part_model.gears import _2068, _2066
from mastapy.system_model.analyses_and_results.static_loads import _6115, _6117, _6120
from mastapy.system_model.connections_and_sockets.gears import _1872
from mastapy._internal.python_net import python_net_import

_GEAR_SET_STATIC_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups', 'GearSetStaticLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetStaticLoadCaseGroup',)


TGearSet = TypeVar('TGearSet', bound='_2068.GearSet')
TGear = TypeVar('TGear', bound='_2066.Gear')
TGearStaticLoad = TypeVar('TGearStaticLoad', bound='_6115.GearLoadCase')
TGearMesh = TypeVar('TGearMesh', bound='_1872.GearMesh')
TGearMeshStaticLoad = TypeVar('TGearMeshStaticLoad', bound='_6117.GearMeshLoadCase')
TGearSetStaticLoad = TypeVar('TGearSetStaticLoad', bound='_6120.GearSetLoadCase')


class GearSetStaticLoadCaseGroup(_5246.DesignEntityStaticLoadCaseGroup, Generic[TGearSet, TGear, TGearStaticLoad, TGearMesh, TGearMeshStaticLoad, TGearSetStaticLoad]):
    '''GearSetStaticLoadCaseGroup

    This is a mastapy class.

    Generic Types:
        TGearSet
        TGear
        TGearStaticLoad
        TGearMesh
        TGearMeshStaticLoad
        TGearSetStaticLoad
    '''

    TYPE = _GEAR_SET_STATIC_LOAD_CASE_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetStaticLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_set(self) -> 'TGearSet':
        '''TGearSet: 'GearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(TGearSet)(self.wrapped.GearSet) if self.wrapped.GearSet else None

    @property
    def gears_load_cases(self) -> 'List[_5244.ComponentStaticLoadCaseGroup[TGear, TGearStaticLoad]]':
        '''List[ComponentStaticLoadCaseGroup[TGear, TGearStaticLoad]]: 'GearsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsLoadCases, constructor.new(_5244.ComponentStaticLoadCaseGroup)[TGear, TGearStaticLoad])
        return value

    @property
    def meshes_load_cases(self) -> 'List[_5245.ConnectionStaticLoadCaseGroup[TGearMesh, TGearMeshStaticLoad]]':
        '''List[ConnectionStaticLoadCaseGroup[TGearMesh, TGearMeshStaticLoad]]: 'MeshesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesLoadCases, constructor.new(_5245.ConnectionStaticLoadCaseGroup)[TGearMesh, TGearMeshStaticLoad])
        return value

    @property
    def gear_set_load_cases(self) -> 'List[TGearSetStaticLoad]':
        '''List[TGearSetStaticLoad]: 'GearSetLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearSetLoadCases, constructor.new(TGearSetStaticLoad))
        return value
