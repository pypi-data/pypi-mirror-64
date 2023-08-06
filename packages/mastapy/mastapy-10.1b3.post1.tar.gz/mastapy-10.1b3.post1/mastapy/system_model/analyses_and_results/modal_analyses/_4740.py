'''_4740.py

CylindricalGearSetModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2062
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6092
from mastapy.system_model.analyses_and_results.system_deflections import _2250, _2251, _2252
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.modal_analyses import _4739, _4738, _4751
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'CylindricalGearSetModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetModalAnalysis',)


class CylindricalGearSetModalAnalysis(_4751.GearSetModalAnalysis):
    '''CylindricalGearSetModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2062.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2062.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6092.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6092.CylindricalGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2250.CylindricalGearSetSystemDeflection':
        '''CylindricalGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2250.CylindricalGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def system_deflection_results_of_type_cylindrical_gear_set_system_deflection_timestep(self) -> '_2251.CylindricalGearSetSystemDeflectionTimestep':
        '''CylindricalGearSetSystemDeflectionTimestep: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2251.CylindricalGearSetSystemDeflectionTimestep.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CylindricalGearSetSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new(_2251.CylindricalGearSetSystemDeflectionTimestep)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def system_deflection_results_of_type_cylindrical_gear_set_system_deflection_with_ltca_results(self) -> '_2252.CylindricalGearSetSystemDeflectionWithLTCAResults':
        '''CylindricalGearSetSystemDeflectionWithLTCAResults: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2252.CylindricalGearSetSystemDeflectionWithLTCAResults.TYPE not in self.wrapped.SystemDeflectionResults.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to CylindricalGearSetSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.SystemDeflectionResults.__class__.__qualname__))

        return constructor.new(_2252.CylindricalGearSetSystemDeflectionWithLTCAResults)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def cylindrical_gears_modal_analysis(self) -> 'List[_4739.CylindricalGearModalAnalysis]':
        '''List[CylindricalGearModalAnalysis]: 'CylindricalGearsModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsModalAnalysis, constructor.new(_4739.CylindricalGearModalAnalysis))
        return value

    @property
    def cylindrical_meshes_modal_analysis(self) -> 'List[_4738.CylindricalGearMeshModalAnalysis]':
        '''List[CylindricalGearMeshModalAnalysis]: 'CylindricalMeshesModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesModalAnalysis, constructor.new(_4738.CylindricalGearMeshModalAnalysis))
        return value
