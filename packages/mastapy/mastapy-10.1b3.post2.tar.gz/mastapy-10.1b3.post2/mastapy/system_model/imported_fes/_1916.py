﻿'''_1916.py

ImportedFeLinkWithSelection
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.system_model.imported_fes import (
    _1885, _1913, _1914, _1915,
    _1917, _1918, _1919, _1920,
    _1921, _1922, _1923, _1935,
    _1946, _1947
)
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_LINK_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFeLinkWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFeLinkWithSelection',)


class ImportedFeLinkWithSelection(_0.APIBase):
    '''ImportedFeLinkWithSelection

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_LINK_WITH_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFeLinkWithSelection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def add_selected_nodes(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddSelectedNodes

    @property
    def delete_all_nodes(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'DeleteAllNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeleteAllNodes

    @property
    def select_component(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SelectComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectComponent

    @property
    def link(self) -> '_1885.ImportedFELink':
        '''ImportedFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1885.ImportedFELink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_electric_machine_stator_link(self) -> '_1913.ImportedFEElectricMachineStatorLink':
        '''ImportedFEElectricMachineStatorLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1913.ImportedFEElectricMachineStatorLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEElectricMachineStatorLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1913.ImportedFEElectricMachineStatorLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_gear_mesh_link(self) -> '_1914.ImportedFEGearMeshLink':
        '''ImportedFEGearMeshLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1914.ImportedFEGearMeshLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEGearMeshLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1914.ImportedFEGearMeshLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_gear_with_duplicated_meshes_link(self) -> '_1915.ImportedFEGearWithDuplicatedMeshesLink':
        '''ImportedFEGearWithDuplicatedMeshesLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1915.ImportedFEGearWithDuplicatedMeshesLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEGearWithDuplicatedMeshesLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1915.ImportedFEGearWithDuplicatedMeshesLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_multi_node_connector_link(self) -> '_1917.ImportedFEMultiNodeConnectorLink':
        '''ImportedFEMultiNodeConnectorLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1917.ImportedFEMultiNodeConnectorLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEMultiNodeConnectorLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1917.ImportedFEMultiNodeConnectorLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_multi_node_link(self) -> '_1918.ImportedFEMultiNodeLink':
        '''ImportedFEMultiNodeLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1918.ImportedFEMultiNodeLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEMultiNodeLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1918.ImportedFEMultiNodeLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_node_link(self) -> '_1919.ImportedFENodeLink':
        '''ImportedFENodeLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1919.ImportedFENodeLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFENodeLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1919.ImportedFENodeLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_planetary_connector_multi_node_link(self) -> '_1920.ImportedFEPlanetaryConnectorMultiNodeLink':
        '''ImportedFEPlanetaryConnectorMultiNodeLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1920.ImportedFEPlanetaryConnectorMultiNodeLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEPlanetaryConnectorMultiNodeLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1920.ImportedFEPlanetaryConnectorMultiNodeLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_planet_based_link(self) -> '_1921.ImportedFEPlanetBasedLink':
        '''ImportedFEPlanetBasedLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1921.ImportedFEPlanetBasedLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEPlanetBasedLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1921.ImportedFEPlanetBasedLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_planet_carrier_link(self) -> '_1922.ImportedFEPlanetCarrierLink':
        '''ImportedFEPlanetCarrierLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1922.ImportedFEPlanetCarrierLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEPlanetCarrierLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1922.ImportedFEPlanetCarrierLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_point_load_link(self) -> '_1923.ImportedFEPointLoadLink':
        '''ImportedFEPointLoadLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1923.ImportedFEPointLoadLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ImportedFEPointLoadLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1923.ImportedFEPointLoadLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_multi_angle_connection_link(self) -> '_1935.MultiAngleConnectionLink':
        '''MultiAngleConnectionLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1935.MultiAngleConnectionLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to MultiAngleConnectionLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1935.MultiAngleConnectionLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_rolling_ring_connection_link(self) -> '_1946.RollingRingConnectionLink':
        '''RollingRingConnectionLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1946.RollingRingConnectionLink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to RollingRingConnectionLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1946.RollingRingConnectionLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_shaft_hub_connection_fe_link(self) -> '_1947.ShaftHubConnectionFELink':
        '''ShaftHubConnectionFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1947.ShaftHubConnectionFELink.TYPE not in self.wrapped.Link.__class__.__mro__:
            raise CastException('Failed to cast link to ShaftHubConnectionFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1947.ShaftHubConnectionFELink)(self.wrapped.Link) if self.wrapped.Link else None
