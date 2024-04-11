def individual_category_serializer(category) -> dict:
    return {
        'id': str(category['_id']),
        'value': category['value'],
        'title': category['title'],
        'image_url': category['image_url'],
        'created_at': category['created_at'],
    }


def individual_restaurant_serializer(restaurant) -> dict:
    return {
        'id': str(restaurant['_id']),
        'title': restaurant['title'],
        'time': restaurant['time'],
        'foods': restaurant['foods'],
        'pickup': restaurant['pickup'],
        'delivery': restaurant['delivery'],
        'is_available': restaurant['is_available'],
        'owner': restaurant['owner'],
        'code': restaurant['code'],
        'image_url': restaurant['image_url'],
        'logo_url': restaurant['logo_url'],
        'verification': restaurant['verification'],
        'verification_message': restaurant['verification_message'],
        'rating': restaurant['rating'],
        'rating_count': restaurant['rating_count'],
        'coords': restaurant['coords'],
        'created_at': restaurant['created_at'],
    }


def individual_food_serializer(food) -> dict:
    return {
        'id': str(food['_id']),
        'title': food['title'],
        'time': food['time'],
        'food_tags': food['food_tags'],
        'category': food['category'],
        'food_type': food['food_type'],
        'code': food['code'],
        'is_available': food['is_available'],
        'restaurant': food['restaurant'],
        'rating': food['rating'],
        'rating_count': food['rating_count'],
        'description': food['description'],
        'price': food['price'],
        'additives': food['additives'],
        'image_urls': food['image_urls'],
        'created_at': food['created_at'],
    }


def individual_rating_serializer(food) -> dict:
    return {
        'id': str(food['_id']),
        'user_id': food['user_id'],
        'rating_type': food['rating_type'],
        'rating': food['rating'],
        'product_id': food['product_id'],
        'created_at': food['created_at'],
    }


def individual_user_serializer(user, token) -> dict:
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'otp': user['otp'],
        'fcm': user['fcm'],
        'email': user['email'],
        'verification': user['verification'],
        'phone_verification': user['phone_verification'],
        'address': user['address'],
        'user_type': user['user_type'],
        'profile': user['profile'],
        'access_token': token,
        'created_at': user['created_at'],
    }


def individual_address_serializer(food) -> dict:
    return {
        'id': str(food['_id']),
        'user_id': food['user_id'],
        'address_line_1': food['address_line_1'],
        'postal_code': food['postal_code'],
        'default': food['default'],
        'delivery_instructions': food['delivery_instructions'],
        'latitude': food['latitude'],
        'longitude': food['longitude'],
        'created_at': food['created_at'],
    }


def individual_cart_serializer(food) -> dict:
    return {
        'id': str(food['_id']),
        'user_id': food['user_id'],
        'product_id': food['product_id'],
        'additives': food['additives'],
        'total_price': food['total_price'],
        'quantity': food['quantity'],
        'created_at': food['created_at'],
    }


def individual_order_serializer(order) -> dict:
    return {
        'id': str(order['_id']),
        'user_id': order['user_id'],
        'order_items': order['order_items'],
        'order_total': order['order_total'],
        'delivery_fee': order['delivery_fee'],
        'grand_total': order['grand_total'],
        'delivery_address_id': order['delivery_address_id'],
        'restsaurant_address': order['restsaurant_address'],
        'payment_method': order['payment_method'],
        'payment_status': order['payment_status'],
        'order_status': order['order_status'],
        'restaurant_id': order['restaurant_id'],
        'restaurrant_coords': order['restaurrant_coords'],
        'driver_id': order['driver_id'],
        'rating': order['rating'],
        'feedback': order['feedback'],
        'promo_code': order['promo_code'],
        'discount_amount': order['discount_amount'],
        'notes': order['notes'],
        'created_at': order['created_at'],
    }


def list_serial(result, individual_serializer) -> list:
    return [individual_serializer(res) for res in result]

# def cart_list_serial(result, individual_serializer) -> list:
#     cart = []
#     for item in result:
#         cart_item =
