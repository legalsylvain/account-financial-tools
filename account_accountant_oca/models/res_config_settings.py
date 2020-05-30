# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    fiscalyear_last_day = fields.Integer(
        related="company_id.fiscalyear_last_day",
        readonly=False,
        required=True,
    )
    fiscalyear_last_month = fields.Selection(
        related="company_id.fiscalyear_last_month",
        readonly=False,
        required=True,
    )
    period_lock_date = fields.Date(
        string="Lock Date for Non-Advisers",
        related="company_id.period_lock_date",
        readonly=False,
        help="Only users with the 'Adviser' role can"
        " edit accounts prior to and inclusive of this date."
        " Use it for period locking inside an open fiscal year,"
        " for example."
    )
    fiscalyear_lock_date = fields.Date(
        string="Lock Date",
        related="company_id.fiscalyear_lock_date",
        readonly=False,
        help="No users, including Advisers, can edit accounts prior to"
        " and inclusive of this date. Use it for fiscal year"
        " locking for example."
    )
    overdue_msg = fields.Text(
        related="company_id.overdue_msg",
        string="Overdue Payments Message",
        translate=True,
        readonly=False,
    )
    incoterm_id = fields.Many2one(
        comodel_name="account.incoterms",
        related="company_id.incoterm_id",
        readonly=False,
        string="Default incoterm",
        help="International Commercial Terms are a series"
        " of predefined commercial terms used in international transactions.",
    )

    # TODO: Include the fields below in the view part
    transfer_account_id = fields.Many2one(
        comodel_name="account.account",
        related="company_id.transfer_account_id",
        domain=lambda self: self._get_domain_transfert_account_id(),
        string="Inter-Banks Transfer Account",
        help="Intermediary account used when moving money from"
        " a liquidity account to another"
    )
    bank_account_code_prefix = fields.Char(
        related="company_id.bank_account_code_prefix",
        readonly=False,
        string="Prefix of the bank accounts"
    )
    cash_account_code_prefix = fields.Char(
        related="company_id.cash_account_code_prefix",
        readonly=False,
        string="Prefix of the cash accounts",
    )
    transfer_account_code_prefix = fields.Char(
        related="company_id.transfer_account_code_prefix",
        readonly=False,
        string="Prefix of the transfer accounts",
    )
    income_currency_exchange_account_id = fields.Many2one(
        comodel_name="account.account",
        related="company_id.income_currency_exchange_account_id",
        readonly=False,
        string="Gain Exchange Rate Account",
        domain=lambda self: self._get_domain_currency_exchange_accounts(),

    )
    expense_currency_exchange_account_id = fields.Many2one(
        comodel_name="account.account",
        related="company_id.expense_currency_exchange_account_id",
        readonly=False,
        string="Loss Exchange Rate Account",
        domain=lambda self: self._get_domain_currency_exchange_accounts(),
    )
    anglo_saxon_accounting = fields.Boolean(
        comodel_name="anglo_saxon_accounting",
        related="company_id.anglo_saxon_accounting",
        readonly=False,
        string="Use anglo-saxon accounting",
    )
    property_stock_account_input_categ_id = fields.Many2one(
        comodel_name="account.account",
        related="company_id.property_stock_account_input_categ_id",
        readonly=False,
        string="Input Account for Stock Valuation",
    )
    property_stock_account_output_categ_id = fields.Many2one(
        comodel_name="account.account",
        related="company_id.property_stock_account_output_categ_id",
        readonly=False,
        string="Output Account for Stock Valuation",
    )
    property_stock_valuation_account_id = fields.Many2one(
        comodel_name="account.account",
        related="company_id.property_stock_valuation_account_id",
        readonly=False,
        string="Account Template for Stock Valuation",
    )
    bank_journal_ids = fields.One2many(
        comodel_name="account.journal",
        related="company_id.bank_journal_ids",
        readonly=False,
        domain=[("type", "=", "bank")],
        string="Bank Journals",
    )

    account_opening_move_id = fields.Many2one(
        comodel_name="account.move",
        related="company_id.account_opening_move_id",
        readonly=False,
        string="Opening Journal Entry",
        help="The journal entry containing the initial balance"
        " of all this company's accounts."
    )
    account_opening_journal_id = fields.Many2one(
        comodel_name="account.journal",
        related="company_id.account_opening_journal_id",
        readonly=False,
        string="Opening Journal",
        help="Journal where the opening entry of this company's"
        " accounting has been posted."
    )
    account_opening_date = fields.Date(
        related="company_id.account_opening_date",
        readonly=False,
        string="Opening Date",
        help="Date at which the opening entry of this company's"
        " accounting has been posted.",
    )

    def _get_domain_transfert_account_id(self):
        current_assets_type = self.env.ref(
            "account.data_account_type_current_assets")
        return [
            ("reconcile", "=", True),
            ("user_type_id.id", "=", current_assets_type.id),
            ("deprecated", "=", False),
        ]

    def _get_domain_currency_exchange_accounts(false):
        return [
            ("internal_type", "=", "other"),
            ("deprecated", "=", False),
        ]
