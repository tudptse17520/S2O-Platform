from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ...domain.interfaces.ireservation_repository import IReservationRepository
from ...domain.models.reservation import Reservation as DomainReservation
from ...infrastructure.models import Reservation as ORMReservation, ReservationStatus as ORMReservationStatus


class ReservationRepository(IReservationRepository):
    """SQLAlchemy implementation of IReservationRepository"""
    
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, orm_reservation: ORMReservation) -> DomainReservation:
        """Convert ORM model to domain model"""
        return DomainReservation(
            id=str(orm_reservation.id),
            tenant_id=str(orm_reservation.tenant_id),
            branch_id=str(orm_reservation.branch_id),
            user_id=str(orm_reservation.user_id),
            booking_time=orm_reservation.booking_time,
            party_size=1,  # Default if not in ORM model
            status=orm_reservation.status.value if orm_reservation.status else "PENDING",
            created_at=orm_reservation.created_at
        )

    def _to_orm(self, domain_reservation: DomainReservation) -> ORMReservation:
        """Convert domain model to ORM model"""
        return ORMReservation(
            id=domain_reservation.id,
            tenant_id=domain_reservation.tenant_id,
            branch_id=domain_reservation.branch_id,
            user_id=domain_reservation.user_id,
            booking_time=domain_reservation.booking_time,
            status=ORMReservationStatus(domain_reservation.status) if domain_reservation.status else ORMReservationStatus.PENDING,
            created_at=domain_reservation.created_at,
            updated_at=datetime.utcnow()
        )

    def create(self, reservation: DomainReservation) -> DomainReservation:
        """Create a new reservation"""
        orm_reservation = self._to_orm(reservation)
        self.session.add(orm_reservation)
        self.session.flush()
        return reservation

    def get_by_id(self, reservation_id: str) -> Optional[DomainReservation]:
        """Get reservation by ID"""
        orm = self.session.query(ORMReservation).filter_by(id=reservation_id).first()
        if orm:
            return self._to_domain(orm)
        return None

    def get_all(self) -> List[DomainReservation]:
        """Get all reservations"""
        orm_list = self.session.query(ORMReservation).all()
        return [self._to_domain(r) for r in orm_list]

    def get_by_user(self, user_id: str) -> List[DomainReservation]:
        """Get reservations by user"""
        orm_list = self.session.query(ORMReservation).filter_by(user_id=user_id).all()
        return [self._to_domain(r) for r in orm_list]

    def get_by_tenant(self, tenant_id: str) -> List[DomainReservation]:
        """Get reservations by tenant"""
        orm_list = self.session.query(ORMReservation).filter_by(tenant_id=tenant_id).all()
        return [self._to_domain(r) for r in orm_list]

    def get_upcoming_for_tenant(self, tenant_id: str) -> List[DomainReservation]:
        """Get upcoming reservations for a tenant"""
        now = datetime.utcnow()
        orm_list = self.session.query(ORMReservation).filter(
            ORMReservation.tenant_id == tenant_id,
            ORMReservation.booking_time >= now,
            ORMReservation.status != ORMReservationStatus.CANCELLED
        ).order_by(ORMReservation.booking_time).all()
        return [self._to_domain(r) for r in orm_list]

    def update(self, reservation_id: str, reservation: DomainReservation) -> DomainReservation:
        """Update reservation"""
        orm = self.session.query(ORMReservation).filter_by(id=reservation_id).first()
        if orm:
            orm.booking_time = reservation.booking_time
            orm.status = ORMReservationStatus(reservation.status) if reservation.status else orm.status
            orm.updated_at = datetime.utcnow()
            self.session.flush()
            return self._to_domain(orm)
        raise ValueError(f"Reservation with id {reservation_id} not found")

    def cancel(self, reservation_id: str) -> bool:
        """Cancel a reservation"""
        orm = self.session.query(ORMReservation).filter_by(id=reservation_id).first()
        if orm:
            orm.status = ORMReservationStatus.CANCELLED
            orm.updated_at = datetime.utcnow()
            self.session.flush()
            return True
        return False
