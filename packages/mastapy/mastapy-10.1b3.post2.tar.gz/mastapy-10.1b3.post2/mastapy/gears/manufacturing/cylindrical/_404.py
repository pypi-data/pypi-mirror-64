﻿'''_404.py

CylindricalShaperDatabase
'''


from typing import Iterable

from mastapy.gears.manufacturing.cylindrical.cutters import _509
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_SHAPER_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalShaperDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalShaperDatabase',)


class CylindricalShaperDatabase(_0.APIBase):
    '''CylindricalShaperDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_SHAPER_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalShaperDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_509.CylindricalGearShaper':
        '''CylindricalGearShaper: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_509.CylindricalGearShaper)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_509.CylindricalGearShaper':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearShaper
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_509.CylindricalGearShaper)(method_result) if method_result else None

    def can_be_removed(self, cylindrical_gear_shaper: '_509.CylindricalGearShaper') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            cylindrical_gear_shaper (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearShaper)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(cylindrical_gear_shaper.wrapped if cylindrical_gear_shaper else None)
        return method_result

    def rename(self, cylindrical_gear_shaper: '_509.CylindricalGearShaper', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            cylindrical_gear_shaper (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearShaper)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(cylindrical_gear_shaper.wrapped if cylindrical_gear_shaper else None, new_name if new_name else None)
        return method_result

    def remove(self, cylindrical_gear_shaper: '_509.CylindricalGearShaper'):
        ''' 'Remove' is the original name of this method.

        Args:
            cylindrical_gear_shaper (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearShaper)
        '''

        self.wrapped.Remove(cylindrical_gear_shaper.wrapped if cylindrical_gear_shaper else None)

    def get_all_items(self) -> 'Iterable[_509.CylindricalGearShaper]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearShaper]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_509.CylindricalGearShaper))

    def save_changes(self, cylindrical_gear_shaper: '_509.CylindricalGearShaper'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            cylindrical_gear_shaper (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearShaper)
        '''

        self.wrapped.SaveChanges(cylindrical_gear_shaper.wrapped if cylindrical_gear_shaper else None)
