'''_2381.py

FaceGearSetCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2045
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2379, _2380, _2385
from mastapy.system_model.analyses_and_results.system_deflections import _2241
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'FaceGearSetCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundSystemDeflection',)


class FaceGearSetCompoundSystemDeflection(_2385.GearSetCompoundSystemDeflection):
    '''FaceGearSetCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2045.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2045.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2045.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2045.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_system_deflection(self) -> 'List[_2379.FaceGearCompoundSystemDeflection]':
        '''List[FaceGearCompoundSystemDeflection]: 'FaceGearsCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundSystemDeflection, constructor.new(_2379.FaceGearCompoundSystemDeflection))
        return value

    @property
    def face_meshes_compound_system_deflection(self) -> 'List[_2380.FaceGearMeshCompoundSystemDeflection]':
        '''List[FaceGearMeshCompoundSystemDeflection]: 'FaceMeshesCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundSystemDeflection, constructor.new(_2380.FaceGearMeshCompoundSystemDeflection))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_2241.FaceGearSetSystemDeflection]':
        '''List[FaceGearSetSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2241.FaceGearSetSystemDeflection))
        return value

    @property
    def assembly_system_deflection_load_cases(self) -> 'List[_2241.FaceGearSetSystemDeflection]':
        '''List[FaceGearSetSystemDeflection]: 'AssemblySystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionLoadCases, constructor.new(_2241.FaceGearSetSystemDeflection))
        return value
