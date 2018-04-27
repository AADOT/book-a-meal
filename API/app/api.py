from app.model import BAM
from flask import Blueprint, jsonify, request


api = Blueprint('api', __name__)
bam = BAM()

"""
Authentication Routes

"""
@api.route('/api/v1/auth/register', methods=['POST'])
def register():
    if not request.is_json: 
        return jsonify({ 'message': 'Request should be JSON' }), 400

    fails, errors = bam.validate_user_fails(request.json)
    if fails:
        return jsonify({'errors': errors}), 400
    else:
        return jsonify(bam.post_user(request.json)), 201

@api.route('/api/v1/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({ 'errors': ['Request should be JSON'] }), 400

    fails, errors = bam.validate_user_fails(request.json)
    if fails:
        return jsonify({'errors': errors}), 400
    else:
        return jsonify({
            'access_token':  '<token>',
            'message' : 'User successfully registered'
        }), 201

"""
Meals Routes

"""
@api.route('/api/v1/meals', methods=['POST', 'GET' ])
def meals():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({ 
                'errors': ['Request should be JSON'] }), 400

        fails, errors = bam.validate_meal_fails(request.json)
        if fails:
            return jsonify({ 'errors': errors }), 400
        else:
            return jsonify(bam.post_meal(request.json)), 201

    elif request.method == 'GET':
        return jsonify({'num_results': len(bam.meals), 
                        'objects': list(bam.get_meals().values())})

@api.route('/api/v1/meals/<int:id>', methods=['PATCH', 'GET', 'DELETE'])
def meal(id):
    if request.method == 'GET':
        if not id in bam.meals.keys():
            return jsonify({ 'errors': ['Not Found'] }), 404
        return jsonify(bam.get_meal(id)), 200

    elif request.method == 'DELETE': 
        if not id in bam.meals.keys():
            return jsonify({ 'errors': ['Not Found'] }), 404
        bam.delete_meal(id)
        return jsonify({'message': 'Successfully deleted' }), 204

    elif request.method == 'PATCH':
        if not request.is_json:
            return jsonify({ 
                'errors': ['Request should be JSON'] 
            }), 400

        if not id in bam.meals:
            return jsonify({ 'errors': ['Not Found'] }), 404

        fails, errors = bam.validate_meal_fails(request.json)
        if fails:
            return jsonify({ 'errors': errors }), 400
        bam.put_meal(request.json, id)
        return jsonify({ 'message': 'Successfully updated' }), 200

"""
Menus Routes

"""

@api.route('/api/v1/menus', methods=['POST', 'GET' ])
def menus():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({ 
                'errors': ['Request should be JSON'] }), 400

        fails, errors = bam.validate_menu_fails(request.json)
        if fails:
            return jsonify({ 'errors': errors }), 400
        else:
            return jsonify(bam.post_menu(request.json)), 201

    elif request.method == 'GET':
        return jsonify({'num_results': len(bam.menus), 
                        'objects': list(bam.get_menus().values())})

@api.route('/api/v1/menus/<int:id>', methods=['PATCH', 'GET', 'DELETE'])
def menu(id):
    if request.method == 'GET':
        if not id in bam.menus.keys():
            return jsonify({ 'errors': ['Not Found'] }), 404
        return jsonify(bam.get_menu(id)), 200

    elif request.method == 'DELETE': 
        if not id in bam.menus.keys():
            return jsonify({ 'errors': ['Not Found'] }), 404
        bam.delete_menu(id)
        return jsonify({'message': 'Successfully deleted' }), 204

    elif request.method == 'PATCH':
        if not request.is_json:
            return jsonify({ 
                'errors': ['Request should be JSON'] 
            }), 400

        if not id in bam.menus:
            return jsonify({ 'errors': ['Not Found'] }), 404

        fails, errors = bam.validate_menu_fails(request.json)
        if fails:
            return jsonify({ 'errors': errors }), 400
        bam.put_menu(request.json, id)
        return jsonify({ 'message': 'Successfully updated' }), 200

"""
Orders Routes

"""

@api.route('/api/v1/orders', methods=['POST', 'GET' ])
def orders():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({ 
                'errors': ['Request should be JSON'] }), 400

        fails, errors = bam.validate_order_fails(request.json)
        if fails:
            return jsonify({ 'errors': errors }), 400
        else:
            return jsonify(bam.post_order(request.json)), 201

    elif request.method == 'GET':
        return jsonify({'num_results': len(bam.orders), 
                        'objects': list(bam.get_orders().values())})

@api.route('/api/v1/orders/<int:id>', methods=['PATCH', 'GET', 'DELETE'])
def order(id):
    if request.method == 'GET':
        if not id in bam.orders.keys():
            return jsonify({ 'errors': ['Not Found'] }), 404
        return jsonify(bam.get_order(id)), 200

    elif request.method == 'DELETE': 
        if not id in bam.orders.keys():
            return jsonify({ 'errors': ['Not Found'] }), 404
        bam.delete_order(id)
        return jsonify({'message': 'Successfully deleted' }), 204

    elif request.method == 'PATCH':
        if not request.is_json:
            return jsonify({ 
                'errors': ['Request should be JSON'] 
            }), 400

        if not id in bam.orders:
            return jsonify({ 'errors': ['Not Found'] }), 404

        fails, errors = bam.validate_order_fails(request.json)
        if fails:
            return jsonify({ 'errors': errors }), 400
        bam.put_order(request.json, id)
        return jsonify({ 'message': 'Successfully updated' }), 200

@api.route('/api/v1/notifications', methods=['POST', 'GET' ])
def notifications():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({ 
                'errors': ['Request should be JSON'] }), 400

        fails, errors = bam.validate_notification_fails(request.json)
        if fails:
            return jsonify({ 'errors': errors }), 400
        else:
            return jsonify(bam.post_notification(request.json)), 201

    elif request.method == 'GET':
        return jsonify({'num_results': len(bam.notifications), 
                        'objects': list(bam.get_notifications().values())})
"""
Notifications Routes

"""

@api.route('/api/v1/notifications/<int:id>', methods=['PATCH', 'GET', 'DELETE'])
def notification(id):
    if request.method == 'GET':
        if not id in bam.notifications.keys():
            return jsonify({ 'errors': ['Not Found'] }), 404
        return jsonify(bam.get_notification(id)), 200

    elif request.method == 'DELETE': 
        if not id in bam.notifications.keys():
            return jsonify({ 'errors': ['Not Found'] }), 404
        bam.delete_notification(id)
        return jsonify({'message': 'Successfully deleted' }), 204

    elif request.method == 'PATCH':
        if not request.is_json:
            return jsonify({ 
                'errors': ['Request should be JSON'] 
            }), 400

        if not id in bam.notifications:
            return jsonify({ 'errors': ['Not Found'] }), 404

        fails, errors = bam.validate_notification_fails(request.json)
        if fails:
            return jsonify({ 'errors': errors }), 400
        bam.put_notification(request.json, id)
        return jsonify({ 'message': 'Successfully updated' }), 200