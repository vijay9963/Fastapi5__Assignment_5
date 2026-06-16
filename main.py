
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

app = FastAPI(title="FastAPI Day 6 Assignment")


# -----------------------------
# Models
# -----------------------------
class Order(BaseModel):
    customer_name: str
    product_id: int
    quantity: int


# -----------------------------
# Sample Products
# -----------------------------
products = [
    {
        "id": 1,
        "name": "Wireless Mouse",
        "price": 499,
        "category": "Electronics",
        "in_stock": True,
    },
    {
        "id": 2,
        "name": "Notebook",
        "price": 99,
        "category": "Stationery",
        "in_stock": True,
    },
    {
        "id": 3,
        "name": "USB Hub",
        "price": 799,
        "category": "Electronics",
        "in_stock": True,
    },
    {
        "id": 4,
        "name": "Pen Set",
        "price": 49,
        "category": "Stationery",
        "in_stock": True,
    },
]

orders = []


# -----------------------------
# Home
# -----------------------------
@app.get("/")
def home():
    return {"message": "FastAPI Day 6 Assignment"}


# -----------------------------
# Get all products
# -----------------------------
@app.get("/products")
def get_products():
    return {
        "total": len(products),
        "products": products
    }


# -----------------------------
# Search Products
# -----------------------------
@app.get("/products/search")
def search_products(keyword: str = Query(...)):
    result = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    if not result:
        return {
            "message": f"No products found for: {keyword}"
        }

    return {
        "keyword": keyword,
        "total_found": len(result),
        "products": result
    }


# -----------------------------
# Sort Products
# -----------------------------
@app.get("/products/sort")
def sort_products(
    sort_by: str = Query("price"),
    order: str = Query("asc")
):

    if sort_by not in ["price", "name"]:
        return {
            "message": "sort_by must be 'price' or 'name'"
        }

    reverse = order == "desc"

    result = sorted(
        products,
        key=lambda p: p[sort_by],
        reverse=reverse
    )

    return {
        "sort_by": sort_by,
        "order": order,
        "products": result
    }


# -----------------------------
# Pagination
# -----------------------------
@app.get("/products/page")
def product_page(
    page: int = Query(1, ge=1),
    limit: int = Query(2, ge=1)
):

    start = (page - 1) * limit
    end = start + limit

    total_pages = -(-len(products) // limit)

    return {
        "page": page,
        "limit": limit,
        "total_products": len(products),
        "total_pages": total_pages,
        "products": products[start:end]
    }


# -----------------------------
# Q4 - Search Orders
# -----------------------------
@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):
    result = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not result:
        return {
            "message": f"No orders found for: {customer_name}"
        }

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }


# -----------------------------
# Q5 - Sort by Category then Price
# -----------------------------
@app.get("/products/sort-by-category")
def sort_by_category():

    result = sorted(
        products,
        key=lambda p: (p["category"], p["price"])
    )

    return {
        "total": len(result),
        "products": result
    }


# -----------------------------
# Q6 - Browse Products
# -----------------------------
@app.get("/products/browse")
def browse_products(
    keyword: str = Query(None),
    sort_by: str = Query("price"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1, le=20),
):

    result = products.copy()

    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p["name"].lower()
        ]

    if sort_by not in ["price", "name"]:
        return {
            "message": "sort_by must be 'price' or 'name'"
        }

    reverse = order == "desc"

    result = sorted(
        result,
        key=lambda p: p[sort_by],
        reverse=reverse
    )

    total_found = len(result)
    total_pages = -(-total_found // limit) if total_found else 0

    start = (page - 1) * limit
    end = start + limit

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total_found,
        "total_pages": total_pages,
        "products": result[start:end]
    }


# -----------------------------
# Create Order
# -----------------------------
@app.post("/orders")
def create_order(order: Order):

    product = None

    for p in products:
        if p["id"] == order.product_id:
            product = p
            break

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    new_order = {
        "order_id": len(orders) + 1,
        "customer_name": order.customer_name,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "pending"
    }

    orders.append(new_order)

    return {
        "message": "Order placed successfully",
        "order": new_order
    }


# -----------------------------
# BONUS - Orders Pagination
# -----------------------------
@app.get("/orders/page")
def orders_page(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1, le=20),
):

    start = (page - 1) * limit
    end = start + limit

    total = len(orders)
    total_pages = -(-total // limit) if total else 0

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "orders": orders[start:end]
    }


# -----------------------------
# Get Product by ID
# -----------------------------
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )

