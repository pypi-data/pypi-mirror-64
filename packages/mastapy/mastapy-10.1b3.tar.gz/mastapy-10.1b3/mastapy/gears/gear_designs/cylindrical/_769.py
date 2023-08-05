'''_769.py

CylindricalGearDesignConstraintsDatabase
'''


from typing import Iterable

from mastapy.gears.gear_designs.cylindrical import _768
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearDesignConstraintsDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearDesignConstraintsDatabase',)


class CylindricalGearDesignConstraintsDatabase(_0.APIBase):
    '''CylindricalGearDesignConstraintsDatabase

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_DESIGN_CONSTRAINTS_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearDesignConstraintsDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_768.CylindricalGearDesignConstraints':
        '''CylindricalGearDesignConstraints: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_768.CylindricalGearDesignConstraints)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_768.CylindricalGearDesignConstraints':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraints
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_768.CylindricalGearDesignConstraints)(method_result) if method_result else None

    def can_be_removed(self, cylindrical_gear_design_constraints: '_768.CylindricalGearDesignConstraints') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            cylindrical_gear_design_constraints (mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraints)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(cylindrical_gear_design_constraints.wrapped if cylindrical_gear_design_constraints else None)
        return method_result

    def rename(self, cylindrical_gear_design_constraints: '_768.CylindricalGearDesignConstraints', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            cylindrical_gear_design_constraints (mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraints)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(cylindrical_gear_design_constraints.wrapped if cylindrical_gear_design_constraints else None, new_name if new_name else None)
        return method_result

    def remove(self, cylindrical_gear_design_constraints: '_768.CylindricalGearDesignConstraints'):
        ''' 'Remove' is the original name of this method.

        Args:
            cylindrical_gear_design_constraints (mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraints)
        '''

        self.wrapped.Remove(cylindrical_gear_design_constraints.wrapped if cylindrical_gear_design_constraints else None)

    def get_all_items(self) -> 'Iterable[_768.CylindricalGearDesignConstraints]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraints]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_768.CylindricalGearDesignConstraints))

    def save_changes(self, cylindrical_gear_design_constraints: '_768.CylindricalGearDesignConstraints'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            cylindrical_gear_design_constraints (mastapy.gears.gear_designs.cylindrical.CylindricalGearDesignConstraints)
        '''

        self.wrapped.SaveChanges(cylindrical_gear_design_constraints.wrapped if cylindrical_gear_design_constraints else None)
