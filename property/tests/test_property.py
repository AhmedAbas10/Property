from odoo.tests.common import TransactionCase
from odoo import fields


class TestProperty(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestProperty, self).setUp()
        self.property_01_record = self.env['property.property'].create({
            'ref': 'PRT0006',
            'name': 'Ahmed',
            'description': 'Ahmed Abas',
            'bedrooms': 10,
            'selling_price': 10000,
            'date_availability': fields.date.today(),
        })

    def test_01_property_values(self):
        property_id = self.property_01_record
        self.assertRecordValues(property_id, [{
            'ref': 'PRT0006',
            'name': 'Ahmed',
            'description': 'Ahmed Abas',
            'bedrooms': 10,
            'selling_price': 10000,
            'date_availability': fields.date.today(),
        }])
