import redis

# Connect to local Redis server
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# -------------------------------
# USER SETUP
# -------------------------------
def create_user(user_id, first_name, last_name):
    r.hset(f"user:{user_id}", mapping={"first_name": first_name, "last_name": last_name})
    print(f"User {user_id} created.")

def get_user(user_id):
    return r.hgetall(f"user:{user_id}")

# -------------------------------
# SKU SETUP
# -------------------------------
def add_sku(sku_id, name, price):
    r.hset(f"sku:{sku_id}", mapping={"name": name, "price": str(price)})
    print(f"SKU {sku_id} added.")

def get_sku(sku_id):
    return r.hgetall(f"sku:{sku_id}")

# -------------------------------
# SHOPPING CART FUNCTIONS
# -------------------------------
def add_item_to_cart(user_id, sku_id, quantity=1):
    r.hincrby(f"cart:{user_id}", sku_id, quantity)
    print(f"Added {quantity} of {sku_id} to cart:{user_id}.")

def remove_item_from_cart(user_id, sku_id, quantity=1):
    current_qty = int(r.hget(f"cart:{user_id}", sku_id) or 0)
    if quantity >= current_qty:
        r.hdel(f"cart:{user_id}", sku_id)
        print(f"Removed {sku_id} from cart:{user_id}.")
    else:
        r.hincrby(f"cart:{user_id}", sku_id, -quantity)
        print(f"Decreased {sku_id} by {quantity} in cart:{user_id}.")

def view_cart(user_id):
    cart = r.hgetall(f"cart:{user_id}")
    if not cart:
        print("Cart is empty.")
        return
    print("\nCart Contents:")
    total = 0
    for sku_id, qty in cart.items():
        sku = get_sku(sku_id)
        item_total = float(sku['price']) * int(qty)
        total += item_total
        print(f"- {sku['name']} x{qty} @ ${sku['price']} each = ${item_total:.2f}")
    print(f"Total: ${total:.2f}\n")

# -------------------------------
# LARGE SCALE INSERT + REVERSE READ
# -------------------------------
def insert_large_list():
    r.delete("biglist")
    pipe = r.pipeline()
    for i in range(1, 10001):
        pipe.lpush("biglist", i)
    pipe.execute()
    print("Inserted 1 to 10,000 into 'biglist'.")

def read_list_reverse():
    values = r.lrange("biglist", 0, -1)
    print("\nFirst 10 values in reverse (original) order:")
    print(values[:10])

# -------------------------------
# SAMPLE TEST FLOW
# -------------------------------
if __name__ == '__main__':
    # User and SKU setup
    create_user("1", "Parker", "Perry")
    add_sku("sku123", "AirPods", 199.99)
    add_sku("sku456", "Mechanical Keyboard", 89.99)

    # Add items to cart
    add_item_to_cart("1", "sku123", 2)
    add_item_to_cart("1", "sku456", 1)

    # View cart
    view_cart("1")

    # Remove item from cart
    remove_item_from_cart("1", "sku123", 1)
    view_cart("1")

    # Print user info
    print("User Info:", get_user("1"))

    # Run large list demo
    insert_large_list()
    read_list_reverse()