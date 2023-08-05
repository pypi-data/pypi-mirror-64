# coding: utf-8

"""
    marax-server-sdk

    Marax Server SDK to send transactional events from client server to marax server  # noqa: E501

    The version of the OpenAPI document: 0.3.0
    Contact: team@marax.ai
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import marax_server_sdk
from marax_server_sdk.models.request_body_properties import RequestBodyProperties  # noqa: E501
from marax_server_sdk.rest import ApiException

class TestRequestBodyProperties(unittest.TestCase):
    """RequestBodyProperties unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RequestBodyProperties
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = marax_server_sdk.models.request_body_properties.RequestBodyProperties()  # noqa: E501
        if include_optional :
            return RequestBodyProperties(
                timestamp = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                marax_id = '0', 
                client_id = '0', 
                reward = marax_server_sdk.models.request_body_properties_reward.RequestBody_properties_reward(
                    id = '0', 
                    expiry = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    timezone = 'Asia/Kolkata', 
                    promocode = 'SWIGGYIT', 
                    title = 'Flat Rs 100/- off', 
                    body = 'Applicable on all order above', 
                    updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    type = 'monetory', 
                    ui = 'scratch_card', 
                    handled_by = 'marax', ), 
                payment_mode = 'cash', 
                total_cart_price = marax_server_sdk.models.request_body_properties_total_cart_price.RequestBody_properties_totalCartPrice(
                    value = 500, 
                    units = 'rupees', ), 
                total_discount = marax_server_sdk.models.request_body_properties_total_discount.RequestBody_properties_totalDiscount(
                    value = 100, 
                    type = 'rupees', ), 
                total_order_price = marax_server_sdk.models.request_body_properties_total_order_price.RequestBody_properties_totalOrderPrice(
                    value = 510.5, 
                    units = 'rupees', ), 
                products = [
                    marax_server_sdk.models.request_body_properties_products.RequestBody_properties_products(
                        quantity = 2, 
                        product_id = '0', 
                        name = 'Fossil Wrist Watch for Men', 
                        brand = 'Fossil', 
                        category = 'watch', 
                        price = 500, 
                        price_units = 1.337, 
                        discount = 100, 
                        discount_type = 'monetory', )
                    ], 
                fulfillment = [
                    marax_server_sdk.models.request_body_properties_fulfillment.RequestBody_properties_fulfillment(
                        type = 'surcharge', 
                        price = 10.5, 
                        price_units = 'rupees', 
                        discount = 0, 
                        discount_type = 'monetory', )
                    ]
            )
        else :
            return RequestBodyProperties(
        )

    def testRequestBodyProperties(self):
        """Test RequestBodyProperties"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
