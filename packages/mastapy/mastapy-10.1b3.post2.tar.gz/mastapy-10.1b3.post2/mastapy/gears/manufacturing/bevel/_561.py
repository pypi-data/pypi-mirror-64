'''_561.py

ConicalMeshManufacturingAnalysis
'''


from typing import List

from mastapy.gears.load_case.conical import _653
from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.bevel import _572, _556
from mastapy.gears.analysis import _944
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_MANUFACTURING_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalMeshManufacturingAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshManufacturingAnalysis',)


class ConicalMeshManufacturingAnalysis(_944.GearMeshImplementationAnalysis):
    '''ConicalMeshManufacturingAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONICAL_MESH_MANUFACTURING_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalMeshManufacturingAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def conical_mesh_load_case(self) -> '_653.ConicalMeshLoadCase':
        '''ConicalMeshLoadCase: 'ConicalMeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_653.ConicalMeshLoadCase)(self.wrapped.ConicalMeshLoadCase) if self.wrapped.ConicalMeshLoadCase else None

    @property
    def tca(self) -> '_572.EaseOffBasedTCA':
        '''EaseOffBasedTCA: 'TCA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_572.EaseOffBasedTCA)(self.wrapped.TCA) if self.wrapped.TCA else None

    @property
    def meshed_gears(self) -> 'List[_556.ConicalMeshedGearManufacturingAnalysis]':
        '''List[ConicalMeshedGearManufacturingAnalysis]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshedGears, constructor.new(_556.ConicalMeshedGearManufacturingAnalysis))
        return value
