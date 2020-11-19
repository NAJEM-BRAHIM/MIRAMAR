# -*- coding: utf-8 -*-

def set_sale_price_on_variant(cr, registry, template_id=None):
    sql = """
        UPDATE product_product pp
        SET fix_price = pt.list_price + (
            SELECT COALESCE(SUM(ptav.price_extra), 0)
            FROM product_variant_combination pvc_rel
            LEFT JOIN product_template_attribute_value ptav ON
                ptav.product_attribute_value_id =
                pvc_rel.product_attribute_value_id
            WHERE pvc_rel.product_product_id = pp.id
            AND ptav.product_tmpl_id = pt.id
        )
        FROM product_template pt
        WHERE pt.id = pp.product_tmpl_id
    """
    if template_id:
        sql += 'AND pt.id = %s'
        cr.execute(sql, (template_id,))
    else:
        cr.execute(sql)
