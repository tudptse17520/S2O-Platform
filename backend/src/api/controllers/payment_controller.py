from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.payment_schema import ProcessPaymentRequest
from ..middleware import auth_required
from ...services.payment_service import PaymentService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories.payment_repository import PaymentRepository
import logging

logger = logging.getLogger(__name__)

payment_bp = Blueprint("payments", __name__, url_prefix="/payments")


@payment_bp.route("", methods=["GET"])
@auth_required()
def get_payments():
    """
    Get all payments for current tenant
    ---
    tags:
      - Payments
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
    responses:
      200:
        description: List of payments
    """
    db = next(get_db())
    try:
        payment_repo = PaymentRepository(db)
        service = PaymentService(payment_repo)
        
        payments = service.get_payments_by_tenant(g.tenant_id)
        return jsonify({"payments": payments}), 200
    except Exception as e:
        logger.error(f"Get payments error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@payment_bp.route("/<payment_id>", methods=["GET"])
@auth_required()
def get_payment(payment_id):
    """
    Get payment by ID
    ---
    tags:
      - Payments
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: payment_id
        type: string
        required: true
    responses:
      200:
        description: Payment details
      404:
        description: Payment not found
    """
    db = next(get_db())
    try:
        payment_repo = PaymentRepository(db)
        service = PaymentService(payment_repo)
        
        payment = service.get_payment(payment_id)
        if not payment:
            return jsonify({"error": "Payment not found"}), 404
        return jsonify(payment), 200
    except Exception as e:
        logger.error(f"Get payment error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@payment_bp.route("/order/<order_id>", methods=["GET"])
@auth_required()
def get_payments_by_order(order_id):
    """
    Get payments for an order
    ---
    tags:
      - Payments
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
        description: List of payments for order
    """
    db = next(get_db())
    try:
        payment_repo = PaymentRepository(db)
        service = PaymentService(payment_repo)
        
        payments = service.get_payments_by_order(order_id)
        return jsonify({"payments": payments}), 200
    except Exception as e:
        logger.error(f"Get payments by order error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@payment_bp.route("", methods=["POST"])
@auth_required()
def create_payment():
    """
    Create new payment
    ---
    tags:
      - Payments
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: ProcessPaymentRequest
          required:
            - amount
          properties:
            order_id:
              type: string
            invoice_id:
              type: string
            amount:
              type: number
            method:
              type: string
              description: CASH, CARD, VIETQR, BANK_TRANSFER
    responses:
      201:
        description: Payment created
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = ProcessPaymentRequest(**data)
        
        payment_repo = PaymentRepository(db)
        service = PaymentService(payment_repo)
        
        result = service.create_payment(g.tenant_id, req.model_dump())
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Create payment error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@payment_bp.route("/<payment_id>/process", methods=["POST"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def process_payment(payment_id):
    """
    Process payment (mark as success)
    ---
    tags:
      - Payments
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: payment_id
        type: string
        required: true
    responses:
      200:
        description: Payment processed successfully
    """
    db = next(get_db())
    try:
        payment_repo = PaymentRepository(db)
        service = PaymentService(payment_repo)
        
        result = service.process_payment(payment_id)
        db.commit()
        
        return jsonify(result), 200
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Process payment error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@payment_bp.route("/<payment_id>/qr", methods=["GET"])
@auth_required()
def generate_qr_code(payment_id):
    """
    Generate VietQR code for payment
    ---
    tags:
      - Payments
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: payment_id
        type: string
        required: true
    responses:
      200:
        description: QR code information
    """
    db = next(get_db())
    try:
        payment_repo = PaymentRepository(db)
        service = PaymentService(payment_repo)
        
        result = service.generate_qr_code(payment_id, g.tenant_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"Generate QR error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@payment_bp.route("/<payment_id>/refund", methods=["POST"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def refund_payment(payment_id):
    """
    Refund a payment
    ---
    tags:
      - Payments
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: payment_id
        type: string
        required: true
    responses:
      200:
        description: Payment refunded
    """
    db = next(get_db())
    try:
        payment_repo = PaymentRepository(db)
        service = PaymentService(payment_repo)
        
        result = service.refund_payment(payment_id)
        db.commit()
        
        return jsonify(result), 200
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Refund payment error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
