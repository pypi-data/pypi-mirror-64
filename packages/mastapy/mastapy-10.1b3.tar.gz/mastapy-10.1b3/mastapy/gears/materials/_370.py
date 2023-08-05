﻿'''_370.py

CylindricalGearAGMAMaterialDatabase
'''


from typing import Iterable

from mastapy.gears.materials import _365
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_AGMA_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Gears.Materials', 'CylindricalGearAGMAMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearAGMAMaterialDatabase',)


class CylindricalGearAGMAMaterialDatabase(_0.APIBase):
    '''CylindricalGearAGMAMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_AGMA_MATERIAL_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearAGMAMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_365.AGMACylindricalGearMaterial':
        '''AGMACylindricalGearMaterial: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_365.AGMACylindricalGearMaterial)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_365.AGMACylindricalGearMaterial':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.materials.AGMACylindricalGearMaterial
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_365.AGMACylindricalGearMaterial)(method_result) if method_result else None

    def can_be_removed(self, agma_cylindrical_gear_material: '_365.AGMACylindricalGearMaterial') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            agma_cylindrical_gear_material (mastapy.gears.materials.AGMACylindricalGearMaterial)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(agma_cylindrical_gear_material.wrapped if agma_cylindrical_gear_material else None)
        return method_result

    def rename(self, agma_cylindrical_gear_material: '_365.AGMACylindricalGearMaterial', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            agma_cylindrical_gear_material (mastapy.gears.materials.AGMACylindricalGearMaterial)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(agma_cylindrical_gear_material.wrapped if agma_cylindrical_gear_material else None, new_name if new_name else None)
        return method_result

    def remove(self, agma_cylindrical_gear_material: '_365.AGMACylindricalGearMaterial'):
        ''' 'Remove' is the original name of this method.

        Args:
            agma_cylindrical_gear_material (mastapy.gears.materials.AGMACylindricalGearMaterial)
        '''

        self.wrapped.Remove(agma_cylindrical_gear_material.wrapped if agma_cylindrical_gear_material else None)

    def get_all_items(self) -> 'Iterable[_365.AGMACylindricalGearMaterial]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.materials.AGMACylindricalGearMaterial]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_365.AGMACylindricalGearMaterial))

    def save_changes(self, agma_cylindrical_gear_material: '_365.AGMACylindricalGearMaterial'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            agma_cylindrical_gear_material (mastapy.gears.materials.AGMACylindricalGearMaterial)
        '''

        self.wrapped.SaveChanges(agma_cylindrical_gear_material.wrapped if agma_cylindrical_gear_material else None)
