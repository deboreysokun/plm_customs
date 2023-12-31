from odoo import models,api


class SaleByCustomer(models.AbstractModel):
    _name = "report.templates_report.report_a"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        customer_group = {}
        group_date = set()
        for account_move in docs:
            customer_name = account_move.partner_id.name
            group_date.add(str(account_move.invoice_date))
            for order in account_move.invoice_line_ids:
                if customer_name not in customer_group:
                    customer_group[customer_name] = [order]
                else:
                    customer_group[customer_name].append(order)
            # print(customer_group)
            # print(group_date)

        return {
            'doc_ids': docids,
            'docs': docs,
            'data': data,
            'customer': customer_group,
            'date': ", ".join(sorted(list(group_date))),
        }
