from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.order_schema import CreateOrderRequest, UpdateOrderStatusRequest, AddOrderItemRequest
from ..middleware import auth_required
from ...services.order_service import OrderService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories import OrderRepository, OrderItemRepository
import logging

logger = logging.getLogger(__name__)

order_bp = Blueprint("orders", __name__, url_prefix="/orders")


@order_bp.route("", methods=["GET"])
@auth_required()
def get_orders():
    """
    Get all orders for current tenant
    ---
    tags:
      - Orders
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: query
        name: status
        type: string
        description: Filter by status
      - in: query
        name: table_id
        type: string
        description: Filter by table
    responses:
      200:
        description: List of orders
    """
    db = next(get_db())
    try:
        status = request.args.get('status')
        table_id = request.args.get('table_id')
        
        order_repo = OrderRepository(db)
        order_item_repo = OrderItemRepository(db)
        service = OrderService(order_repo, order_item_repo)
        
        if status:
            orders = service.get_orders_by_status(g.tenant_id, status)
        elif table_id:
            orders = service.get_orders_by_table(table_id)
        else:
            orders = service.get_orders_by_tenant(g.tenant_id)
        
        return jsonify({"orders": orders}), 200
    except Exception as e:
        logger.error(f"Get orders error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@order_bp.route("/<order_id>", methods=["GET"])
@auth_required()
def get_order(order_id):
    """
    Get order by ID with items
    ---
    tags:
      - Orders
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: order_id
        type: string
        required: true
    responses:
      200:
        description: Order details
      404:
        description: Order not found
    """
    db = next(get_db())
    try:
        order_repo = OrderRepository(db)
        order_item_repo = OrderItemRepository(db)
        service = OrderService(order_repo, order_item_repo)
        
        order = service.get_order(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        return jsonify(order), 200
    except Exception as e:
        logger.error(f"Get order error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@order_bp.route("", methods=["POST"])
@auth_required()
def create_order():
    """
    Create new order
    ---
    tags:
      - Orders
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: CreateOrderRequest
          required:
            - branch_id
          properties:
            branch_id:
              type: string
            table_id:
              type: string
            customer_id:
              type: string
            note:
              type: string
    responses:
      201:
        description: Order created
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = CreateOrderRequest(**data)
        
        order_repo = OrderRepository(db)
        order_item_repo = OrderItemRepository(db)
        service = OrderService(order_repo, order_item_repo)
        
        result = service.create_order(g.tenant_id, req.branch_id, req.model_dump())
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Create order error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@order_bp.route("/<order_id>/status", methods=["PUT"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def update_order_status(order_id):
    """
    Update order status
    ---
    tags:
      - Orders
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: order_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdateOrderStatusRequest
          required:
            - status
          properties:
            status:
              type: string
              description: PENDING, CONFIRMED, PREPARING, READY, SERVED, COMPLETED, CANCELLED
    responses:
      200:
        description: Order status updated
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateOrderStatusRequest(**data)
        
        order_repo = OrderRepository(db)
        service = OrderService(order_repo)
        
        result = service.update_order_status(order_id, req.status)
        db.commit()
        
        return jsonify(result), 200
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Update order status error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@order_bp.route("/<order_id>/items", methods=["POST"])
@auth_required()
def add_order_item(order_id):
    """
    Add item to order
    ---
    tags:
      - Orders
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: order_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: AddOrderItemRequest
          required:
            - product_id
            - price
          properties:
            product_id:
              type: string
            quantity:
              type: integer
            price:
              type: number
    responses:
      201:
        description: Item added to order
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = AddOrderItemRequest(**data)
        
        order_repo = OrderRepository(db)
        order_item_repo = OrderItemRepository(db)
        service = OrderService(order_repo, order_item_repo)
        
        result = service.add_item_to_order(order_id, g.tenant_id, req.model_dump())
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Add order item error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@order_bp.route("/<order_id>", methods=["DELETE"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def delete_order(order_id):
    """
    Delete order
    ---
    tags:
      - Orders
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: order_id
        type: string
        required: true
    responses:
      200:
        description: Order deleted
    """
    db = next(get_db())
    try:
        order_repo = OrderRepository(db)
        service = OrderService(order_repo)
        
        deleted = service.delete_order(order_id)
        db.commit()
        
        if deleted:
            return jsonify({"message": "Order deleted"}), 200
        return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Delete order error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
