'''_6082.py

CouplingConnectionLoadCase
'''


from mastapy.system_model.connections_and_sockets.couplings import (
    _1896, _1892, _1894, _1898,
    _1900, _1902
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6135
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'CouplingConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingConnectionLoadCase',)


class CouplingConnectionLoadCase(_6135.InterMountableComponentConnectionLoadCase):
    '''CouplingConnectionLoadCase

    This is a mastapy class.
    '''

    TYPE = _COUPLING_CONNECTION_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1896.CouplingConnection':
        '''CouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1896.CouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_clutch_connection(self) -> '_1892.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1892.ClutchConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ClutchConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1892.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_concept_coupling_connection(self) -> '_1894.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1894.ConceptCouplingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1894.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_part_to_part_shear_coupling_connection(self) -> '_1898.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1898.PartToPartShearCouplingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1898.PartToPartShearCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spring_damper_connection(self) -> '_1900.SpringDamperConnection':
        '''SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1900.SpringDamperConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to SpringDamperConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1900.SpringDamperConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_torque_converter_connection(self) -> '_1902.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1902.TorqueConverterConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1902.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
