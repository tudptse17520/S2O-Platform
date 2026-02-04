from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from ..schemas.reservation_schema import CreateReservationRequest, UpdateReservationRequest, UpdateReservationStatusRequest
from ..middleware import auth_required
from ...services.reservation_service import ReservationService
from ...infrastructure.databases.postgres import get_db
from ...infrastructure.repositories import ReservationRepository
import logging

logger = logging.getLogger(__name__)

reservation_bp = Blueprint("reservations", __name__, url_prefix="/reservations")


@reservation_bp.route("", methods=["GET"])
@auth_required()
def get_reservations():
    """
    Get reservations
    ---
    tags:
      - Reservations
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: query
        name: upcoming
        type: boolean
        description: Filter upcoming reservations only
    responses:
      200:
        description: List of reservations
    """
    db = next(get_db())
    try:
        upcoming = request.args.get('upcoming', 'false').lower() == 'true'
        
        reservation_repo = ReservationRepository(db)
        service = ReservationService(reservation_repo)
        
        if upcoming:
            reservations = service.get_upcoming_reservations(g.tenant_id)
        else:
            reservations = service.get_reservations_by_tenant(g.tenant_id)
        
        return jsonify({"reservations": reservations}), 200
    except Exception as e:
        logger.error(f"Get reservations error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@reservation_bp.route("/<reservation_id>", methods=["GET"])
@auth_required()
def get_reservation(reservation_id):
    """
    Get reservation by ID
    ---
    tags:
      - Reservations
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: reservation_id
        type: string
        required: true
    responses:
      200:
        description: Reservation details
      404:
        description: Reservation not found
    """
    db = next(get_db())
    try:
        reservation_repo = ReservationRepository(db)
        service = ReservationService(reservation_repo)
        
        reservation = service.get_reservation(reservation_id)
        if not reservation:
            return jsonify({"error": "Reservation not found"}), 404
        return jsonify(reservation), 200
    except Exception as e:
        logger.error(f"Get reservation error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@reservation_bp.route("/my", methods=["GET"])
@auth_required()
def get_my_reservations():
    """
    Get current user's reservations
    ---
    tags:
      - Reservations
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
    responses:
      200:
        description: User's reservations
    """
    db = next(get_db())
    try:
        reservation_repo = ReservationRepository(db)
        service = ReservationService(reservation_repo)
        
        reservations = service.get_reservations_by_user(g.user_id)
        return jsonify({"reservations": reservations}), 200
    except Exception as e:
        logger.error(f"Get my reservations error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@reservation_bp.route("", methods=["POST"])
@auth_required()
def create_reservation():
    """
    Create new reservation
    ---
    tags:
      - Reservations
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: CreateReservationRequest
          required:
            - branch_id
            - booking_time
          properties:
            branch_id:
              type: string
            booking_time:
              type: string
              description: ISO format datetime
            party_size:
              type: integer
    responses:
      201:
        description: Reservation created
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = CreateReservationRequest(**data)
        
        reservation_repo = ReservationRepository(db)
        service = ReservationService(reservation_repo)
        
        result = service.create_reservation(g.tenant_id, req.branch_id, g.user_id, req.model_dump())
        db.commit()
        
        return jsonify(result), 201
    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Create reservation error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@reservation_bp.route("/<reservation_id>", methods=["PUT"])
@auth_required()
def update_reservation(reservation_id):
    """
    Update reservation
    ---
    tags:
      - Reservations
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: reservation_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdateReservationRequest
          properties:
            booking_time:
              type: string
            party_size:
              type: integer
    responses:
      200:
        description: Reservation updated
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateReservationRequest(**data)
        
        reservation_repo = ReservationRepository(db)
        service = ReservationService(reservation_repo)
        
        result = service.update_reservation(reservation_id, req.model_dump(exclude_unset=True))
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
        logger.error(f"Update reservation error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@reservation_bp.route("/<reservation_id>/status", methods=["PUT"])
@auth_required(roles=['OWNER', 'STAFF', 'SYS_ADMIN'])
def update_reservation_status(reservation_id):
    """
    Update reservation status
    ---
    tags:
      - Reservations
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: reservation_id
        type: string
        required: true
      - in: body
        name: body
        schema:
          id: UpdateReservationStatusRequest
          required:
            - status
          properties:
            status:
              type: string
    responses:
      200:
        description: Status updated
    """
    data = request.get_json()
    db = next(get_db())
    try:
        req = UpdateReservationStatusRequest(**data)
        
        reservation_repo = ReservationRepository(db)
        service = ReservationService(reservation_repo)
        
        result = service.update_reservation_status(reservation_id, req.status)
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
        logger.error(f"Update reservation status error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@reservation_bp.route("/<reservation_id>/cancel", methods=["POST"])
@auth_required()
def cancel_reservation(reservation_id):
    """
    Cancel reservation
    ---
    tags:
      - Reservations
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: path
        name: reservation_id
        type: string
        required: true
    responses:
      200:
        description: Reservation cancelled
    """
    db = next(get_db())
    try:
        reservation_repo = ReservationRepository(db)
        service = ReservationService(reservation_repo)
        
        cancelled = service.cancel_reservation(reservation_id)
        db.commit()
        
        if cancelled:
            return jsonify({"message": "Reservation cancelled"}), 200
        return jsonify({"error": "Reservation not found"}), 404
    except Exception as e:
        db.rollback()
        logger.error(f"Cancel reservation error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
