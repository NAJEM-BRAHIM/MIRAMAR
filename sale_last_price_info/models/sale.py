# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import fields, models
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date_order_sale_last_price_info = fields.Datetime(
        string="Order date", related="order_id.date_order", store=True, index=True
    )
    last_sale_price = fields.Float(
        string="Last Sale Price", related='product_id.last_sale_price', store=True)


class SaleReport(models.Model):
    _inherit = 'sale.report'

    last_sale_price = fields.Float('Last Sale Price', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['last_sale_price'] = ", l.last_sale_price as last_sale_price"

        groupby += ', l.last_sale_price'

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)

# class SaleReport(models.Model):
#     _inherit = "sale.report"

#     last_sale_price = fields.Float('Last Sale Price', readonly=True)

#     def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
#         with_ = ("WITH %s" % with_clause) if with_clause else ""

#         select_ = """
#             min(l.id) as id,
#             l.product_id as product_id,
#             t.uom_id as product_uom,
#             l.last_sale_price as last_sale_price,
#             sum(l.product_uom_qty / u.factor * u2.factor) as product_uom_qty,
#             sum(l.qty_delivered / u.factor * u2.factor) as qty_delivered,
#             sum(l.qty_invoiced / u.factor * u2.factor) as qty_invoiced,
#             sum(l.qty_to_invoice / u.factor * u2.factor) as qty_to_invoice,
#             sum(l.price_total / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as price_total,
#             sum(l.price_subtotal / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as price_subtotal,
#             sum(l.untaxed_amount_to_invoice / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as untaxed_amount_to_invoice,
#             sum(l.untaxed_amount_invoiced / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as untaxed_amount_invoiced,
#             count(*) as nbr,
#             s.name as name,
#             s.date_order as date,
#             s.state as state,
#             s.partner_id as partner_id,
#             s.user_id as user_id,
#             s.company_id as company_id,
#             s.campaign_id as campaign_id,
#             s.medium_id as medium_id,
#             s.source_id as source_id,
#             extract(epoch from avg(date_trunc('day',s.date_order)-date_trunc('day',s.create_date)))/(24*60*60)::decimal(16,2) as delay,
#             t.categ_id as categ_id,
#             s.pricelist_id as pricelist_id,
#             s.analytic_account_id as analytic_account_id,
#             s.team_id as team_id,
#             p.product_tmpl_id,
#             partner.country_id as country_id,
#             partner.industry_id as industry_id,
#             partner.commercial_partner_id as commercial_partner_id,
#             sum(p.weight * l.product_uom_qty / u.factor * u2.factor) as weight,
#             sum(p.volume * l.product_uom_qty / u.factor * u2.factor) as volume,
#             l.discount as discount,
#             sum((l.price_unit * l.product_uom_qty * l.discount / 100.0 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)) as discount_amount,
#             s.id as order_id
#         """

#         for field in fields.values():
#             select_ += field

#         from_ = """
#                 sale_order_line l
#                       join sale_order s on (l.order_id=s.id)
#                       join res_partner partner on s.partner_id = partner.id
#                         left join product_product p on (l.product_id=p.id)
#                             left join product_template t on (p.product_tmpl_id=t.id)
#                     left join uom_uom u on (u.id=l.product_uom)
#                     left join uom_uom u2 on (u2.id=t.uom_id)
#                     left join product_pricelist pp on (s.pricelist_id = pp.id)
#                 %s
#         """ % from_clause

#         groupby_ = """
#             l.product_id,
#             l.last_sale_price,
#             l.order_id,
#             t.uom_id,
#             t.categ_id,
#             s.name,
#             s.date_order,
#             s.partner_id,
#             s.user_id,
#             s.state,
#             s.company_id,
#             s.campaign_id,
#             s.medium_id,
#             s.source_id,
#             s.pricelist_id,
#             s.analytic_account_id,
#             s.team_id,
#             p.product_tmpl_id,
#             partner.country_id,
#             partner.industry_id,
#             partner.commercial_partner_id,
#             l.discount,
#             s.id %s
#         """ % (groupby)

#         return '%s (SELECT %s FROM %s WHERE l.product_id IS NOT NULL GROUP BY %s)' % (with_, select_, from_, groupby_)

#     def init(self):
#         # self._table = sale_report
#         tools.drop_view_if_exists(self.env.cr, self._table)
#         self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))
