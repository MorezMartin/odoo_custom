# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Taxes and subtotals on order lines',
    'version' : '8.0.1.0',
    'category' : 'Sales',
    'description' : """
Add Taxes and Subtotals on Sale Order Lines.
============================================

You can see Taxes and Subtotals on Sale Order Lines.
----------------------------------------------------
    * Tax Price
    * Taxed Price
    * Tax Line
    * Taxed Line
""",
    'author' : 'Martin Morez',
    'website' : 'http://www.mh-receptions.com',
    'images' : [],
    'depends' : ['website_sale', 'account_voucher', 'account', 'report', 'product'], # TODO : Add report
    'data': ['tax_website_product_report.xml'],
    'demo': [],
    'test' : [],
    'installable' : True,
    'auto_install' : False,
}
