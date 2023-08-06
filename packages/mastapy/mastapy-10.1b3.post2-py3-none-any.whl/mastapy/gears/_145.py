'''_145.py

PocketingPowerLossCoefficientsDatabase
'''


from typing import Iterable

from mastapy.gears import _144
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_POCKETING_POWER_LOSS_COEFFICIENTS_DATABASE = python_net_import('SMT.MastaAPI.Gears', 'PocketingPowerLossCoefficientsDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('PocketingPowerLossCoefficientsDatabase',)


class PocketingPowerLossCoefficientsDatabase(_0.APIBase):
    '''PocketingPowerLossCoefficientsDatabase

    This is a mastapy class.
    '''

    TYPE = _POCKETING_POWER_LOSS_COEFFICIENTS_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PocketingPowerLossCoefficientsDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_144.PocketingPowerLossCoefficients':
        '''PocketingPowerLossCoefficients: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_144.PocketingPowerLossCoefficients)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_144.PocketingPowerLossCoefficients':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.PocketingPowerLossCoefficients
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_144.PocketingPowerLossCoefficients)(method_result) if method_result else None

    def can_be_removed(self, pocketing_power_loss_coefficients: '_144.PocketingPowerLossCoefficients') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            pocketing_power_loss_coefficients (mastapy.gears.PocketingPowerLossCoefficients)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(pocketing_power_loss_coefficients.wrapped if pocketing_power_loss_coefficients else None)
        return method_result

    def rename(self, pocketing_power_loss_coefficients: '_144.PocketingPowerLossCoefficients', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            pocketing_power_loss_coefficients (mastapy.gears.PocketingPowerLossCoefficients)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(pocketing_power_loss_coefficients.wrapped if pocketing_power_loss_coefficients else None, new_name if new_name else None)
        return method_result

    def remove(self, pocketing_power_loss_coefficients: '_144.PocketingPowerLossCoefficients'):
        ''' 'Remove' is the original name of this method.

        Args:
            pocketing_power_loss_coefficients (mastapy.gears.PocketingPowerLossCoefficients)
        '''

        self.wrapped.Remove(pocketing_power_loss_coefficients.wrapped if pocketing_power_loss_coefficients else None)

    def get_all_items(self) -> 'Iterable[_144.PocketingPowerLossCoefficients]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.PocketingPowerLossCoefficients]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_144.PocketingPowerLossCoefficients))

    def save_changes(self, pocketing_power_loss_coefficients: '_144.PocketingPowerLossCoefficients'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            pocketing_power_loss_coefficients (mastapy.gears.PocketingPowerLossCoefficients)
        '''

        self.wrapped.SaveChanges(pocketing_power_loss_coefficients.wrapped if pocketing_power_loss_coefficients else None)
