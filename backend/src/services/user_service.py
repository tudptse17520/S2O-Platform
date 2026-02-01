from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import bcrypt

from ..domain.interfaces.iuser_repository import IUserRepository
from ..domain.models.user import User, UserRole


class UserService:
    """Service for user management business logic"""
    
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        user = self.user_repo.get_by_id(user_id)
        return self._to_dict(user) if user else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        user = self.user_repo.get_by_email(email)
        return self._to_dict(user) if user else None
    
    def get_users_by_tenant(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all users for a tenant"""
        users = self.user_repo.get_by_tenant(tenant_id)
        return [self._to_dict(u) for u in users]
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users (admin only)"""
        users = self.user_repo.get_all()
        return [self._to_dict(u) for u in users]
    
    def create_user(self, data: Dict[str, Any], tenant_id: str = None) -> Dict[str, Any]:
        """Create a new user"""
        # Check if email already exists
        existing = self.user_repo.get_by_email(data['email'])
        if existing:
            raise ValueError("Email already registered")
        
        # Hash password
        password_hash = bcrypt.hashpw(
            data['password'].encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        
        user = User(
            id=uuid.uuid4(),
            email=data['email'],
            password_hash=password_hash,
            full_name=data.get('full_name'),
            role=UserRole(data.get('role', 'CUSTOMER')),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        
        created = self.user_repo.save(user, tenant_id)
        return self._to_dict(created)
    
    def update_user(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'role' in data:
            user.role = UserRole(data['role'])
        
        updated = self.user_repo.update(user_id, user)
        return self._to_dict(updated)
    
    def change_user_role(self, user_id: str, new_role: str) -> Dict[str, Any]:
        """Change user role (admin only)"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        user.role = UserRole(new_role)
        updated = self.user_repo.update(user_id, user)
        return self._to_dict(updated)
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        return self.user_repo.delete(user_id)
    
    def _to_dict(self, user: User) -> Dict[str, Any]:
        return {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value if isinstance(user.role, UserRole) else user.role,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        }
