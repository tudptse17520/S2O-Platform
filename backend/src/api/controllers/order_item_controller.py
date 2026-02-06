from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.order_item_schema import (
    CreateOrderItemRequest, 
    UpdateOrderItemRequest,
    UpdateOrderItemStatusRequest
)
from ..middleware import auth_required
from ...services.order_item_service import OrderItemService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories.order_item_repository import OrderItemRepository
import logging

logger = logging.getLogger(__name__)

order_item_bp = Blueprint("order_items", __name__, url_prefix="/order-items")


@order_item_bp.route("/<order_item_id>", methods=["GET"])
@auth_required()
def get_order_item(order_item_id):
    """
    Get order item by ID
    ---
    tags:
      - Order Items
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: order_item_id
        type: string
        required: true
    responses:
      200:
        description: Order item details
      404:
        description: Order item not found
    """
    db = next(get_db())
    try:
        repo = OrderItemRepository(db)
        service = OrderItemService(repo)
        
        item = service.get_order_item(order_item_id)
        if not item:
            return jsonify({"error": "Order item not found"}), 404
        return jsonify(item), 200
    except Exception as e:
        logger.error(f"Get order item error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@order_item_bp.route("/by-order/<order_id>", methods=["GET"])
@auth_required()
def get_order_items_by_order(order_id):
    """
    Get all items for an order
    ---
    tags:
      - Order Items
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: order_id
        type: string
        required: true
      - in: query
        name: status
        type: string
        description: Filter by status (PENDING, COOKING, READY, SERVED, CANCELLED)
    responses:
      200:
        description: List of order items
    """
    db = next(get_db())
    try:
        repo = OrderItemRepository(db)
        service = OrderItemService(repo)
        
        status = request.args.get('status')
        if status:
            items = service.get_order_items_by_status(order_id, status)
        else:
            items = service.get_order_items_by_order(order_id)
        
        return jsonify({"order_items": items}), 200
    except Exception as e:
        logger.error(f"Get order items error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@order_item_bp.route("", methods=["POST"])
@auth_required()
def create_order_item():
    """
    Create new order item
    ---
    tags:
      - Order Items
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: CreateOrderItemRequest
          required:
            - order_id
            - product_id
            - quantity
            - price_at_order
          properties:
            order_id:
              type: string
            product_id:
              type: string
            quantity:
              type: integer
              minimum: 1
            price_at_order:
              type: number
    responses:
      201:
        description: Order item created
      400:
        description: Validation error
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = CreateOrderItemRequest(**data)
        
        repo = OrderItemRepository(db)
        service = OrderItemService(repo)
        
        result = service.create_order_item(g.tenant_id, req.model_dump())
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Create order item error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@order_item_bp.route("/<order_item_id>", methods=["PUT"])
@auth_required()
def update_order_item(order_item_id):
    """
    Update order item
    ---
    tags:
      - Order Items
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: order_item_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdateOrderItemRequest
          properties:
            quantity:
              type: integer
              minimum: 1
            item_status:
              type: string
              enum: [PENDING, COOKING, READY, SERVED, CANCELLED]
    responses:
      200:
        description: Order item updated
      404:
        description: Order item not found
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateOrderItemRequest(**data)
        
        repo = OrderItemRepository(db)
        service = OrderItemService(repo)
        
        result = service.update_order_item(order_item_id, req.model_dump(exclude_unset=True))
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
        logger.error(f"Update order item error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@order_item_bp.route("/<order_item_id>/status", methods=["PATCH"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def update_order_item_status(order_item_id):
    """
    Update order item status (for kitchen staff)
    ---
    tags:
      - Order Items
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: order_item_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdateOrderItemStatusRequest
          required:
            - item_status
          properties:
            item_status:
              type: string
              enum: [PENDING, COOKING, READY, SERVED, CANCELLED]
    responses:
      200:
        description: Status updated
      404:
        description: Order item not found
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateOrderItemStatusRequest(**data)
        
        repo = OrderItemRepository(db)
        service = OrderItemService(repo)
        
        result = service.update_status(order_item_id, req.item_status.value)
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
        logger.error(f"Update status error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@order_item_bp.route("/<order_item_id>", methods=["DELETE"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def delete_order_item(order_item_id):
    """
    Delete order item
    ---
    tags:
      - Order Items
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: order_item_id
        type: string
        required: true
    responses:
      200:
        description: Order item deleted
      404:
        description: Order item not found
    """
    db = next(get_db())
    try:
        repo = OrderItemRepository(db)
        service = OrderItemService(repo)
        
        deleted = service.delete_order_item(order_item_id)
        db.commit()
        
        if deleted:
            return jsonify({"message": "Order item deleted"}), 200
        return jsonify({"error": "Order item not found"}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Delete order item error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


# Kitchen workflow endpoints
@order_item_bp.route("/<order_item_id>/cooking", methods=["POST"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def mark_cooking(order_item_id):
    """
    Mark order item as cooking (kitchen use)
    ---
    tags:
      - Order Items
      - Kitchen
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: order_item_id
        type: string
        required: true
    responses:
      200:
        description: Status updated to COOKING
    """
    db = next(get_db())
    try:
        repo = OrderItemRepository(db)
        service = OrderItemService(repo)
        
        result = service.mark_cooking(order_item_id)
        db.commit()
        
        return jsonify(result), 200
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Mark cooking error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@order_item_bp.route("/<order_item_id>/ready", methods=["POST"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def mark_ready(order_item_id):
    """
    Mark order item as ready to serve
    ---
    tags:
      - Order Items
      - Kitchen
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: order_item_id
        type: string
        required: true
    responses:
      200:
        description: Status updated to READY
    """
    db = next(get_db())
    try:
        repo = OrderItemRepository(db)
        service = OrderItemService(repo)
        
        result = service.mark_ready(order_item_id)
        db.commit()
        
        return jsonify(result), 200
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Mark ready error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@order_item_bp.route("/<order_item_id>/served", methods=["POST"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def mark_served(order_item_id):
    """
    Mark order item as served
    ---
    tags:
      - Order Items
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: order_item_id
        type: string
        required: true
    responses:
      200:
        description: Status updated to SERVED
    """
    db = next(get_db())
    try:
        repo = OrderItemRepository(db)
        service = OrderItemService(repo)
        
        result = service.mark_served(order_item_id)
        db.commit()
        
        return jsonify(result), 200
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Mark served error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@order_item_bp.route("/<order_item_id>/cancel", methods=["POST"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def cancel_order_item(order_item_id):
    """
    Cancel order item
    ---
    tags:
      - Order Items
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: order_item_id
        type: string
        required: true
    responses:
      200:
        description: Order item cancelled
    """
    db = next(get_db())
    try:
        repo = OrderItemRepository(db)
        service = OrderItemService(repo)
        
        result = service.cancel_order_item(order_item_id)
        db.commit()
        
        return jsonify(result), 200
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Cancel order item error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
