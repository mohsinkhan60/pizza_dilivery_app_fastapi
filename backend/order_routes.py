from fastapi import APIRouter, Depends, status # type: ignore
from fastapi.exceptions import HTTPException # type: ignore
from fastapi_jwt_auth import AuthJWT # type: ignore
from models import User, Order
from schemas import OrderModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder # type: ignore

order_router = APIRouter(
      prefix="/orders",
      tags=["orders"]
)

session = Session()

@order_router.get("/")
async def hellow(Authorize: AuthJWT = Depends()):
    """
    ## A simple route to test JWT authentication.
    This route returns Hellow Mohsin Khan, this is your order route!
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Hellow Mohsin Khan, this is your order route!"}
    
@order_router.post("/order", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    """
    ## Create a new order.
    This requires the folliwing
    - pizza_size: str
    - quantity: int
    """
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity,
    )
    new_order.user = user
    session.add(new_order)
    session.commit()
    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "order_status": new_order.order_status,
        "ïd": new_order.id,
        "user_id": new_order.user_id
    }
    return jsonable_encoder(response)

@order_router.get("/orders")
async def get_orders(Authorize: AuthJWT = Depends()):
    """
    ## List All Orders.
    The List of All orders made. It ca be accessed by staff members only.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user.is_staff:
        orders = session.query(Order).all()
        return jsonable_encoder(orders)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to view all orders.",
    )

@order_router.get("/order/{order_id}")
async def get_order(order_id: int, Authorize: AuthJWT = Depends()):
    """
    ## Get a order by ID.
    This gets an order by its ID. And is accessible by both staff members and the user who created the order.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    if user.is_staff or order.user_id == user.id:
        return jsonable_encoder(order)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to view this order.",
    )

@order_router.get("/user/orders")
async def get_user_orders(Authorize: AuthJWT = Depends()):
    """
    ## Get current user's orders.
    This gets all orders made by the current user.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    return jsonable_encoder(current_user.orders)

@order_router.get("/user/order/{order_id}")
async def get_specific_order(order_id: int, Authorize: AuthJWT = Depends()):
    """
    ## Get a specific order for the currently Logged In user.
    This returns a specific order for the currently logged in user.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    orders = current_user.orders
    for order in orders:
        if order.id == order_id:
            return jsonable_encoder(order)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Order not found for the current user."
    )

@order_router.put("/order/update/{order_id}", status_code=status.HTTP_200_OK)
async def update_order(order_id: int, order: OrderModel, Authorize: AuthJWT = Depends()):
    """
    ## Update an existing order.
    This updates an existing order. The user must be the owner of the order.
    - pizza_size: str
    - quantity: int
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    order_to_update = session.query(Order).filter(Order.id == order_id).first()
    order_to_update.pizza_size = order.pizza_size
    order_to_update.quantity = order.quantity
    session.commit()
    return jsonable_encoder(order_to_update)

@order_router.delete("/order/delete/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, Authorize: AuthJWT = Depends()):
    """
    ## Delete an order by ID.
    This deletes an order by its ID.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    order_to_delete = session.query(Order).filter(Order.id == order_id).first()
    if not order_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    session.delete(order_to_delete)
    session.commit()
    return {"message": "Order deleted successfully"}