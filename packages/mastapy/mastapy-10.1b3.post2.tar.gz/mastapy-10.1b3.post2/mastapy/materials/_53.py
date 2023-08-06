﻿'''_53.py

BearingMaterialDatabase
'''


from typing import Iterable

from mastapy.materials import _52
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BEARING_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Materials', 'BearingMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingMaterialDatabase',)


class BearingMaterialDatabase(_0.APIBase):
    '''BearingMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _BEARING_MATERIAL_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_52.BearingMaterial':
        '''BearingMaterial: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_52.BearingMaterial)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_52.BearingMaterial':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.materials.BearingMaterial
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_52.BearingMaterial)(method_result) if method_result else None

    def can_be_removed(self, bearing_material: '_52.BearingMaterial') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            bearing_material (mastapy.materials.BearingMaterial)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(bearing_material.wrapped if bearing_material else None)
        return method_result

    def rename(self, bearing_material: '_52.BearingMaterial', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            bearing_material (mastapy.materials.BearingMaterial)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(bearing_material.wrapped if bearing_material else None, new_name if new_name else None)
        return method_result

    def remove(self, bearing_material: '_52.BearingMaterial'):
        ''' 'Remove' is the original name of this method.

        Args:
            bearing_material (mastapy.materials.BearingMaterial)
        '''

        self.wrapped.Remove(bearing_material.wrapped if bearing_material else None)

    def get_all_items(self) -> 'Iterable[_52.BearingMaterial]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.materials.BearingMaterial]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_52.BearingMaterial))

    def save_changes(self, bearing_material: '_52.BearingMaterial'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            bearing_material (mastapy.materials.BearingMaterial)
        '''

        self.wrapped.SaveChanges(bearing_material.wrapped if bearing_material else None)
