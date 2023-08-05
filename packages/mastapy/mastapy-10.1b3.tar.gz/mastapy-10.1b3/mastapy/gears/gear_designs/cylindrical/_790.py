﻿'''_790.py

FinishStockSpecification
'''


from mastapy.gears.gear_designs.cylindrical.thickness_stock_and_backlash import _827
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _822, _809
from mastapy._internal.python_net import python_net_import

_FINISH_STOCK_SPECIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'FinishStockSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('FinishStockSpecification',)


class FinishStockSpecification(_809.RelativeValuesSpecification['FinishStockSpecification']):
    '''FinishStockSpecification

    This is a mastapy class.
    '''

    TYPE = _FINISH_STOCK_SPECIFICATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FinishStockSpecification.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def finish_stock_rough_thickness_specification_method(self) -> '_827.FinishStockType':
        '''FinishStockType: 'FinishStockRoughThicknessSpecificationMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.FinishStockRoughThicknessSpecificationMethod)
        return constructor.new(_827.FinishStockType)(value) if value else None

    @finish_stock_rough_thickness_specification_method.setter
    def finish_stock_rough_thickness_specification_method(self, value: '_827.FinishStockType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FinishStockRoughThicknessSpecificationMethod = value

    @property
    def normal(self) -> '_822.TolerancedValueSpecification[FinishStockSpecification]':
        '''TolerancedValueSpecification[FinishStockSpecification]: 'Normal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_822.TolerancedValueSpecification)[FinishStockSpecification](self.wrapped.Normal) if self.wrapped.Normal else None

    @property
    def tangent_to_reference_circle(self) -> '_822.TolerancedValueSpecification[FinishStockSpecification]':
        '''TolerancedValueSpecification[FinishStockSpecification]: 'TangentToReferenceCircle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_822.TolerancedValueSpecification)[FinishStockSpecification](self.wrapped.TangentToReferenceCircle) if self.wrapped.TangentToReferenceCircle else None
