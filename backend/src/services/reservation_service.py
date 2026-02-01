import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

from ..domain.interfaces.ireservation_repository import IReservationRepository
from ..domain.models.reservation import Reservation, ReservationStatus


class ReservationService:
    """Service layer for Reservation operations"""
    
    def __init__(self, reservation_repo: IReservationRepository):
        self.reservation_repo = reservation_repo

    def create_reservation(self, tenant_id: str, branch_id: str, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new reservation"""
        reservation_id = uuid.uuid4()
        
        # Parse booking time
        booking_time = data.get('booking_time')
        if isinstance(booking_time, str):
            booking_time = datetime.fromisoformat(booking_time.replace('Z', '+00:00'))
        
        reservation = Reservation(
            id=str(reservation_id),
            tenant_id=tenant_id,
            branch_id=branch_id,
            user_id=user_id,
            booking_time=booking_time,
            party_size=data.get('party_size', 1),
            status=ReservationStatus.PENDING,
            created_at=datetime.utcnow()
        )
        
        saved_reservation = self.reservation_repo.create(reservation)
        return self._to_dict(saved_reservation)

    def get_reservation(self, reservation_id: str) -> Optional[Dict[str, Any]]:
        """Get a reservation by ID"""
        reservation = self.reservation_repo.get_by_id(reservation_id)
        if reservation:
            return self._to_dict(reservation)
        return None

    def get_reservations_by_tenant(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all reservations for a tenant"""
        reservations = self.reservation_repo.get_by_tenant(tenant_id)
        return [self._to_dict(r) for r in reservations]

    def get_upcoming_reservations(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get upcoming reservations for a tenant"""
        reservations = self.reservation_repo.get_upcoming_for_tenant(tenant_id)
        return [self._to_dict(r) for r in reservations]

    def get_reservations_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Get reservations by user"""
        reservations = self.reservation_repo.get_by_user(user_id)
        return [self._to_dict(r) for r in reservations]

    def update_reservation(self, reservation_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a reservation"""
        existing = self.reservation_repo.get_by_id(reservation_id)
        if not existing:
            raise ValueError(f"Reservation with id {reservation_id} not found")
        
        if 'booking_time' in data:
            booking_time = data['booking_time']
            if isinstance(booking_time, str):
                booking_time = datetime.fromisoformat(booking_time.replace('Z', '+00:00'))
            existing.booking_time = booking_time
        
        if 'party_size' in data:
            existing.party_size = data['party_size']
        
        updated_reservation = self.reservation_repo.update(reservation_id, existing)
        return self._to_dict(updated_reservation)

    def update_reservation_status(self, reservation_id: str, status: str) -> Dict[str, Any]:
        """Update reservation status"""
        existing = self.reservation_repo.get_by_id(reservation_id)
        if not existing:
            raise ValueError(f"Reservation with id {reservation_id} not found")
        
        existing.status = status
        
        updated_reservation = self.reservation_repo.update(reservation_id, existing)
        return self._to_dict(updated_reservation)

    def cancel_reservation(self, reservation_id: str) -> bool:
        """Cancel a reservation"""
        return self.reservation_repo.cancel(reservation_id)

    def _to_dict(self, reservation: Reservation) -> Dict[str, Any]:
        """Convert reservation entity to dictionary"""
        return {
            "id": str(reservation.id),
            "tenant_id": str(reservation.tenant_id),
            "branch_id": str(reservation.branch_id),
            "user_id": str(reservation.user_id),
            "booking_time": reservation.booking_time.isoformat() if reservation.booking_time else None,
            "party_size": reservation.party_size,
            "status": reservation.status if isinstance(reservation.status, str) else reservation.status.value,
            "created_at": reservation.created_at.isoformat() if reservation.created_at else None
        }
