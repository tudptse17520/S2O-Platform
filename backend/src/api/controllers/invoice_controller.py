from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.invoice_schema import CreateInvoiceRequest, UpdatePaymentStatusRequest
from ..middleware import auth_required
from ...services.invoice_service import InvoiceService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories import InvoiceRepository
import logging

logger = logging.getLogger(__name__)

invoice_bp = Blueprint("invoices", __name__, url_prefix="/invoices")


@invoice_bp.route("", methods=["GET"])
@auth_required()
def get_invoices():
    """
    Get all invoices for current tenant
    ---
    tags:
      - Invoices
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: query
        name: status
        type: string
        description: Filter by payment status
    responses:
      200:
        description: List of invoices
    """
    db = next(get_db())
    try:
        status = request.args.get('status')
        
        invoice_repo = InvoiceRepository(db)
        service = InvoiceService(invoice_repo)
        
        if status:
            invoices = service.get_invoices_by_status(g.tenant_id, status)
        else:
            invoices = service.get_invoices_by_tenant(g.tenant_id)
        
        return jsonify({"invoices": invoices}), 200
    except Exception as e:
        logger.error(f"Get invoices error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@invoice_bp.route("/<invoice_id>", methods=["GET"])
@auth_required()
def get_invoice(invoice_id):
    """
    Get invoice by ID
    ---
    tags:
      - Invoices
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: invoice_id
        type: string
        required: true
    responses:
      200:
        description: Invoice details
      404:
        description: Invoice not found
    """
    db = next(get_db())
    try:
        invoice_repo = InvoiceRepository(db)
        service = InvoiceService(invoice_repo)
        
        invoice = service.get_invoice(invoice_id)
        if not invoice:
            return jsonify({"error": "Invoice not found"}), 404
        return jsonify(invoice), 200
    except Exception as e:
        logger.error(f"Get invoice error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@invoice_bp.route("/order/<order_id>", methods=["GET"])
@auth_required()
def get_invoices_by_order(order_id):
    """
    Get invoices for an order
    ---
    tags:
      - Invoices
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
        description: List of invoices for order
    """
    db = next(get_db())
    try:
        invoice_repo = InvoiceRepository(db)
        service = InvoiceService(invoice_repo)
        
        invoices = service.get_invoice_by_order(order_id)
        return jsonify({"invoices": invoices}), 200
    except Exception as e:
        logger.error(f"Get invoices by order error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@invoice_bp.route("", methods=["POST"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def create_invoice():
    """
    Create new invoice
    ---
    tags:
      - Invoices
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: CreateInvoiceRequest
          required:
            - order_id
            - final_amount
          properties:
            order_id:
              type: string
            final_amount:
              type: number
            tax_amount:
              type: number
            discount_amount:
              type: number
            payment_method:
              type: string
    responses:
      201:
        description: Invoice created
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = CreateInvoiceRequest(**data)
        
        invoice_repo = InvoiceRepository(db)
        service = InvoiceService(invoice_repo)
        
        result = service.create_invoice(g.tenant_id, req.order_id, req.model_dump())
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Create invoice error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@invoice_bp.route("/<invoice_id>/pay", methods=["POST"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def mark_invoice_paid(invoice_id):
    """
    Mark invoice as paid
    ---
    tags:
      - Invoices
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: invoice_id
        type: string
        required: true
    responses:
      200:
        description: Invoice marked as paid
    """
    db = next(get_db())
    try:
        invoice_repo = InvoiceRepository(db)
        service = InvoiceService(invoice_repo)
        
        result = service.mark_paid(invoice_id)
        db.commit()
        
        return jsonify(result), 200
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Mark invoice paid error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@invoice_bp.route("/<invoice_id>/refund", methods=["POST"])
@auth_required(roles=['OWNER', 'SYS_ADMIN'])
def refund_invoice(invoice_id):
    """
    Refund invoice
    ---
    tags:
      - Invoices
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: invoice_id
        type: string
        required: true
    responses:
      200:
        description: Invoice refunded
    """
    db = next(get_db())
    try:
        invoice_repo = InvoiceRepository(db)
        service = InvoiceService(invoice_repo)
        
        result = service.refund(invoice_id)
        db.commit()
        
        return jsonify(result), 200
    except ValueError as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Refund invoice error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
