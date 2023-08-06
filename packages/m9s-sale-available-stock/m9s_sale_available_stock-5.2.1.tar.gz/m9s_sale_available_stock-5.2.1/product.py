# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pyson import PYSONEncoder, PYSONDecoder
from trytond.modules.stock import ProductByLocation


class ProductByLocationExcludeAssigned(ProductByLocation):
    """
    Product by Locations Exclude Assigned Quantities
    """
    __name__ = 'product.by_location.exclude_assigned'

    def do_open(self, action):
        action, data = super(
            ProductByLocationExcludeAssigned, self
        ).do_open(action)
        # Decode pyson context
        context = PYSONDecoder().decode(action['pyson_context'])
        # Update context
        context['stock_assign'] = True
        # Encode the new context to create new pyson context
        action['pyson_context'] = PYSONEncoder().encode(context)
        return action, data
