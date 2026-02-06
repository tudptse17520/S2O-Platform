from flask import Blueprint, request, jsonify, g, Response
from pydantic import BaseModel, Field
from typing import Optional
from ..middleware import auth_required
from ...infrastructure.services.qrcode_service import QRCodeService
import logging

logger = logging.getLogger(__name__)

qrcode_bp = Blueprint("qrcode", __name__, url_prefix="/qrcode")


class GenerateTableQRRequest(BaseModel):
    branch_id: str
    table_id: str
    table_number: Optional[str] = None


class GeneratePaymentQRRequest(BaseModel):
    order_id: str
    amount: float = Field(..., gt=0)
    bank_id: Optional[str] = None
    account_number: Optional[str] = None


@qrcode_bp.route("/table", methods=["POST"])
@auth_required()
def generate_table_qr():
    """
    Generate QR code for table ordering
    ---
    tags:
      - QR Codes
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - branch_id
            - table_id
          properties:
            branch_id:
              type: string
            table_id:
              type: string
            table_number:
              type: string
    responses:
      200:
        description: QR code generated
        schema:
          type: object
          properties:
            qr_data:
              type: string
              description: URL encoded in QR
            qr_image_base64:
              type: string
              description: Base64 encoded PNG image
    """
    data = request.get_json()
    
    try:
        req = GenerateTableQRRequest(**data)
        
        service = QRCodeService()
        result = service.generate_table_qr(
            tenant_id=g.tenant_id,
            branch_id=req.branch_id,
            table_id=req.table_id,
            table_number=req.table_number
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Generate table QR error: {e}")
        return jsonify({"error": str(e)}), 500


@qrcode_bp.route("/payment", methods=["POST"])
@auth_required()
def generate_payment_qr():
    """
    Generate QR code for payment (VietQR supported)
    ---
    tags:
      - QR Codes
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          type: object
          required:
            - order_id
            - amount
          properties:
            order_id:
              type: string
            amount:
              type: number
            bank_id:
              type: string
              description: Bank ID for VietQR
            account_number:
              type: string
              description: Bank account number for VietQR
    responses:
      200:
        description: Payment QR code generated
    """
    data = request.get_json()
    
    try:
        req = GeneratePaymentQRRequest(**data)
        
        service = QRCodeService()
        result = service.generate_payment_qr(
            tenant_id=g.tenant_id,
            order_id=req.order_id,
            amount=req.amount,
            bank_id=req.bank_id,
            account_number=req.account_number
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Generate payment QR error: {e}")
        return jsonify({"error": str(e)}), 500


@qrcode_bp.route("/restaurant", methods=["GET"])
@auth_required()
def generate_restaurant_qr():
    """
    Generate QR code for restaurant info page
    ---
    tags:
      - QR Codes
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: query
        name: branch_id
        type: string
    responses:
      200:
        description: Restaurant QR code generated
    """
    branch_id = request.args.get('branch_id')
    
    try:
        service = QRCodeService()
        result = service.generate_restaurant_qr(
            tenant_id=g.tenant_id,
            branch_id=branch_id
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Generate restaurant QR error: {e}")
        return jsonify({"error": str(e)}), 500


@qrcode_bp.route("/loyalty/<customer_id>", methods=["GET"])
@auth_required()
def generate_loyalty_qr(customer_id):
    """
    Generate QR code for customer loyalty card
    ---
    tags:
      - QR Codes
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: customer_id
        type: string
        required: true
    responses:
      200:
        description: Loyalty QR code generated
    """
    try:
        service = QRCodeService()
        result = service.generate_loyalty_qr(
            tenant_id=g.tenant_id,
            customer_id=customer_id
        )
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Generate loyalty QR error: {e}")
        return jsonify({"error": str(e)}), 500


@qrcode_bp.route("/image/<qr_type>/<entity_id>", methods=["GET"])
def get_qr_image(qr_type, entity_id):
    """
    Get QR code as PNG image (public endpoint)
    ---
    tags:
      - QR Codes
    parameters:
      - in: path
        name: qr_type
        type: string
        enum: [table, payment, restaurant]
        required: true
      - in: path
        name: entity_id
        type: string
        required: true
      - in: query
        name: tenant_id
        type: string
        required: true
    responses:
      200:
        description: QR code PNG image
        content:
          image/png:
            schema:
              type: string
              format: binary
    """
    import base64
    
    tenant_id = request.args.get('tenant_id')
    if not tenant_id:
        return jsonify({"error": "tenant_id required"}), 400
    
    try:
        service = QRCodeService()
        
        if qr_type == "table":
            branch_id = request.args.get('branch_id', '')
            result = service.generate_table_qr(tenant_id, branch_id, entity_id)
        elif qr_type == "restaurant":
            result = service.generate_restaurant_qr(tenant_id, entity_id)
        else:
            return jsonify({"error": "Invalid qr_type"}), 400
        
        if result.get("qr_image_base64"):
            image_data = base64.b64decode(result["qr_image_base64"])
            return Response(image_data, mimetype='image/png')
        else:
            return jsonify({"error": "QR code generation failed"}), 500
            
    except Exception as e:
        logger.error(f"Get QR image error: {e}")
        return jsonify({"error": str(e)}), 500
