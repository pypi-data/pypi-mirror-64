﻿'''_506.py

CylindricalGearPlungeShaverDatabase
'''


from typing import Iterable

from mastapy.gears.manufacturing.cylindrical.cutters import _505
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_PLUNGE_SHAVER_DATABASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalGearPlungeShaverDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearPlungeShaverDatabase',)


class CylindricalGearPlungeShaverDatabase(_0.APIBase):
    '''CylindricalGearPlungeShaverDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_PLUNGE_SHAVER_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearPlungeShaverDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_505.CylindricalGearPlungeShaver':
        '''CylindricalGearPlungeShaver: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_505.CylindricalGearPlungeShaver)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_505.CylindricalGearPlungeShaver':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearPlungeShaver
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_505.CylindricalGearPlungeShaver)(method_result) if method_result else None

    def can_be_removed(self, cylindrical_gear_plunge_shaver: '_505.CylindricalGearPlungeShaver') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            cylindrical_gear_plunge_shaver (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearPlungeShaver)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(cylindrical_gear_plunge_shaver.wrapped if cylindrical_gear_plunge_shaver else None)
        return method_result

    def rename(self, cylindrical_gear_plunge_shaver: '_505.CylindricalGearPlungeShaver', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            cylindrical_gear_plunge_shaver (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearPlungeShaver)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(cylindrical_gear_plunge_shaver.wrapped if cylindrical_gear_plunge_shaver else None, new_name if new_name else None)
        return method_result

    def remove(self, cylindrical_gear_plunge_shaver: '_505.CylindricalGearPlungeShaver'):
        ''' 'Remove' is the original name of this method.

        Args:
            cylindrical_gear_plunge_shaver (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearPlungeShaver)
        '''

        self.wrapped.Remove(cylindrical_gear_plunge_shaver.wrapped if cylindrical_gear_plunge_shaver else None)

    def get_all_items(self) -> 'Iterable[_505.CylindricalGearPlungeShaver]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearPlungeShaver]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_505.CylindricalGearPlungeShaver))

    def save_changes(self, cylindrical_gear_plunge_shaver: '_505.CylindricalGearPlungeShaver'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            cylindrical_gear_plunge_shaver (mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearPlungeShaver)
        '''

        self.wrapped.SaveChanges(cylindrical_gear_plunge_shaver.wrapped if cylindrical_gear_plunge_shaver else None)
