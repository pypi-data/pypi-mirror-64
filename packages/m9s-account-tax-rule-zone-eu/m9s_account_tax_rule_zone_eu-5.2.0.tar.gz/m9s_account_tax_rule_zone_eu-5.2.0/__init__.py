# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import account
from . import party
from . import sale
from . import purchase
from . import purchase_request

__all__ = ['register']

def register():
    Pool.register(
        party.Party,
        account.TaxRuleLineTemplate,
        account.TaxRuleLine,
        account.InvoiceLine,
        sale.SaleLine,
        purchase.PurchaseLine,
        module='account_tax_rule_zone_eu', type_='model')
    Pool.register(
        purchase_request.CreatePurchase,
        module='account_tax_rule_zone', type_='wizard')
