"""Test orders resource endpoints"""



import json
import unittest
from datetime import datetime, timedelta
from app import create_app, db
from tests.base import BaseTest
from app.models import MenuType, MenuItem, Menu, Meal


class OrderTestCase(BaseTest):
    """ This will test order resource endpoints """

    def setUp(self):
        """Create a test application"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.headers = {'Content-Type' : 'application/json'}

        with self.app.app_context():
            db.create_all()

    def test_order_creation(self):
        """Test order creation"""
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
            }),
            headers=customer_header
        )
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_result['user_id'], user_id)

    def test_cannot_create_order_without_menu_item_id(self):
        """Test cannot create order without a menu item id"""
        customer_header, _ = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({}),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 400)

    def test_cannot_create_order_with_non_existing_menu_item_id(self):
        """Test cannot create order with non-existing menu item"""
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({'menu_item_id': 40}),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 400)


    def test_can_get_all_orders(self):
        """Test can get all orders"""
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/orders', headers=caterer_header)
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['num_results'], 1)
        self.assertIn(b'objects', res.data)

    def test_can_get_order_by_id(self):
        """Test can get order by id"""
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
            }),
            headers=customer_header
        )
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/api/v1/orders/{}'.format(json_result['id']),
            headers=customer_header
        )

        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['user_id'], user_id)

    def test_cannot_get_other_users_order(self):
        """Test cannot get other user's order"""
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
            }),
            headers=customer_header
        )
        json_result = json.loads(res.get_data(as_text=True))
        self.assertEqual(res.status_code, 201)

        customer_header, user_id = self.loginCustomer('hacker@mail.com')
        res = self.client().get(
            '/api/v1/orders/{}'.format(json_result['id']),
            headers=customer_header
        )

        self.assertEqual(res.status_code, 401)
        self.assertIn(b'Unauthorized access', res.data)

    def test_cannot_create_order_with_expired_menu(self):
        """Test cannot create order with expired menu"""
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(yesterdays=True),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'This menu is expired', res.data)

    def test_cannot_create_order_with_more_quantity_than_is_available(self):
        """Test cannot create order with more quantity than is available"""
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': user_id,
                'quantity': 1000,
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'menu items are available', res.data)

    def test_cannot_create_order_with_negative_quantity(self):
        """Test cannot create order with negative quantity"""
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': user_id,
                'quantity': -1,
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'Quantity must be positive', res.data)

    def test_order_can_be_updated(self):
        """Test order can be updated"""
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/orders/1',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(menu_item_id=2),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 200)

        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/orders/1', headers=customer_header)
        json_result = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_result['menu_item_id'], 2)

    def test_cannot_update_order_with_wrong_menu_id(self):
        """Test cannot update order with wrong menu id"""
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/orders/1',
            data=json.dumps({
                'menu_item_id': 100,
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'No menu item found for that', res.data)

    def test_cannot_update_order_with_more_quantity_than_is_available(self):
        """Test cannot update order with more quantity than is available"""
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/orders/1',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': user_id,
                'quantity': 100,
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'menu items are available', res.data)


    def test_cannot_update_order_with_expired_menu(self):
        """Test cannot update order with expired menu"""
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/orders/1',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(yesterdays=True),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(b'This menu is expired', res.data)

    def test_cannot_edit_another_users_order(self):
        """Test cannot edit another users order"""
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': user_id
            }),
            headers=customer_header
        )
        customer_header, user_id = self.loginCustomer(email='hacker@mail.com')
        self.assertEqual(res.status_code, 201)
        res = self.client().put(
            '/api/v1/orders/1',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(menu_item_id=2),
                'user_id': user_id
            }),
            headers=customer_header
        )
        self.assertEqual(res.status_code, 401)
        self.assertIn(b'This user cannot edit this order', res.data)

    def test_order_deletion(self):
        """Test order deletion"""
        caterer_header, _ = self.loginCaterer()
        customer_header, user_id = self.loginCustomer()
        res = self.client().post(
            '/api/v1/orders',
            data=json.dumps({
                'menu_item_id': self.createMenuItem(),
                'user_id': user_id
            }),
            headers=caterer_header
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/orders/1',
                                   headers=customer_header)
        self.assertEqual(res.status_code, 200)
        customer_header, _ = self.loginCustomer()
        res = self.client().get('/api/v1/orders/1', headers=customer_header)
        self.assertEqual(res.status_code, 404)

    def createMenuItem(self, menu_item_id=1, quantity=1, yesterdays=False):
        """Create menu item for the order"""
        with self.app.app_context():
            menu_item = MenuItem.query.get(menu_item_id)
            if not menu_item or yesterdays:
                menu = Menu.query.get(1)
                if not menu or yesterdays:
                    menu = Menu(category=MenuType.BREAKFAST)
                    if yesterdays:
                        menu.day = datetime.utcnow().date() - timedelta(1)
                    menu.save()
                meal_name = 'ugali'
                meal = Meal.query.filter_by(name=meal_name).first()
                if not meal:
                    meal = Meal(name=meal_name, img_path='#', cost=200)
                    meal.save()
                menu_item = MenuItem(menu_id=menu.id, 
                                     meal_id=meal.id, quantity=quantity)
                menu_item.save()
            return menu_item.id


if __name__ == '__main__':
    unittest.main()
