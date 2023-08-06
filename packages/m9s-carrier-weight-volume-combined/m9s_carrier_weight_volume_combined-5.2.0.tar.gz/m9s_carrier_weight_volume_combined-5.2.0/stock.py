# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from itertools import groupby
from functools import partial

from trytond.pool import PoolMeta

from ._parcel import parcel_weight, parcel_volume


class ShipmentIn(metaclass=PoolMeta):
    __name__ = 'stock.shipment.in'

    def _group_parcel_key(self, lines, line):
        """
        The key to group lines by parcel
        """
        return None

    def _get_carrier_context(self):
        context = super(ShipmentIn, self)._get_carrier_context()
        if not self.carrier:
            return context
        if self.carrier.carrier_cost_method != 'weight_volume':
            return context

        lines = self.incoming_moves or []

        keyfunc = partial(self._group_parcel_key, lines)
        lines = sorted(lines, key=keyfunc)

        weights = []
        volumes = []
        context = context.copy()
        context['weights'] = weights
        context['volumes'] = volumes
        for key, parcel in groupby(lines, key=keyfunc):
            # Store iterator as list for re-use
            parcel_group = list(parcel)
            weights.append(parcel_weight(
                    parcel_group, self.carrier.weight_uom, 'unit'))
            volumes.append(parcel_volume(
                    parcel_group, self.carrier.volume_uom, 'unit'))
        return context


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    def _group_parcel_key(self, lines, line):
        """
        The key to group lines by parcel
        """
        return None

    def _get_carrier_context(self):
        context = super(ShipmentOut, self)._get_carrier_context()
        if not self.carrier:
            return context
        if self.carrier.carrier_cost_method != 'weight_volume':
            return context

        lines = (getattr(self, 'inventory_moves', None)
            and self.inventory_moves or [])

        keyfunc = partial(self._group_parcel_key, lines)
        lines = sorted(lines, key=keyfunc)

        weights = []
        volumes = []
        context = context.copy()
        context['weights'] = weights
        context['volumes'] = volumes
        for key, parcel in groupby(lines, key=keyfunc):
            # Store iterator as list for re-use
            parcel_group = list(parcel)
            weights.append(parcel_weight(
                    parcel_group, self.carrier.weight_uom, 'unit'))
            volumes.append(parcel_volume(
                    parcel_group, self.carrier.volume_uom, 'unit'))
        return context
