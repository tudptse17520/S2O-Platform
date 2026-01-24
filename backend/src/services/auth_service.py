import uuid
import jwt
import datetime
import bcrypt
from typing import Optional

from ..domain.interfaces.iuser_repository import IUserRepository
from ..domain.interfaces.itenant_repository import ITenantRepository
from ..domain.models.user import User, UserRole
from ..domain.models.tenant import Tenant
from ..domain.models.staff_profile import StaffProfile
from config import Config

class AuthService:
    def __init__(self, user_repo: IUserRepository, tenant_repo: ITenantRepository):
        self.user_repo = user_repo
        self.tenant_repo = tenant_repo

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def _verify_password(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def _generate_token(self, user_id: str, tenant_id: str, role: str) -> str:
        payload = {
            'sub': user_id,
            'tenant_id': tenant_id,
            'role': role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

    def register_tenant(self, data: dict):
        # Business Logic: Check if email exists
        if self.user_repo.get_by_email(data['email']):
            raise ValueError("Email already registered")

        # Create Tenant Entity
        tenant_id = uuid.uuid4()
        slug = data['tenant_name'].lower().replace(' ', '-') + '-' + str(uuid.uuid4())[:8]
        tenant = Tenant(
            id=tenant_id,
            name=data['tenant_name'], 
            slug=slug,
            subscription_plan="FREE",
            is_active=True,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        self.tenant_repo.save(tenant)

        # Create User Entity (Owner)
        user_id = uuid.uuid4()
        user = User(
            id=user_id,
            email=data['email'],
            password_hash=self._hash_password(data['password']),
            full_name=data['full_name'],
            role=UserRole.OWNER,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        self.user_repo.save(user)

        # Create Staff Profile Entity
        staff_profile = StaffProfile(
            id=uuid.uuid4(),
            user_id=user.id,
            tenant_id=tenant.id,
            branch_id=None,
            position="Owner",
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        self.tenant_repo.save_staff_profile(staff_profile)
        
        # NOTE: Transaction commit responsibility usually lies with the Unit of Work or Controller in simple CA.
        # Since we are passing a Session-bound repository, we can rely on the caller to commit via UoW or 
        # have a commit method in repo. For now, we assume the controller commits the session.

        token = self._generate_token(str(user.id), str(tenant.id), user.role.value)
        
        return {
            "access_token": token,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value,
                "tenant_id": str(tenant.id)
            }
        }

    def login(self, data: dict):
        user = self.user_repo.get_by_email(data['email'])
        if not user or not self._verify_password(data['password'], user.password_hash):
            raise ValueError("Invalid email or password")
        
        # Find tenant for this user
        staff_profile = self.tenant_repo.get_staff_profile_by_user_id(user.id)
        tenant_id = None
        if staff_profile:
            tenant_id = str(staff_profile.tenant_id)

        if not tenant_id and user.role != UserRole.SYS_ADMIN:
             # In a real app we might allow login without tenant context to a user portal
             raise ValueError("User is not associated with any tenant")

        token = self._generate_token(str(user.id), tenant_id or "system", user.role.value)

        return {
            "access_token": token,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value,
                "tenant_id": tenant_id
            }
        }
