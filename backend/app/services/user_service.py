from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.models.user import User, Role, Permission
from app.schemas.user import UserCreate, UserUpdate, RoleCreate, RoleUpdate, Permission as PermissionSchema, ProfileUpdate
from app.core.security import get_password_hash, verify_password

class UserService:
    @staticmethod
    def get(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).options(joinedload(User.roles).joinedload(Role.permissions)).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).options(joinedload(User.roles).joinedload(Role.permissions)).filter(User.email == email).first()

    @staticmethod
    def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).options(joinedload(User.roles).joinedload(Role.permissions)).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
        )
        if obj_in.role_ids:
            roles = db.query(Role).filter(Role.id.in_(obj_in.role_ids)).all()
            db_obj.roles = roles
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        if obj_in.email:
            db_obj.email = obj_in.email
        if obj_in.full_name:
            db_obj.full_name = obj_in.full_name
        if obj_in.password:
            db_obj.hashed_password = get_password_hash(obj_in.password)
        if obj_in.is_active is not None:
            db_obj.is_active = obj_in.is_active
        if obj_in.role_ids is not None:
            roles = db.query(Role).filter(Role.id.in_(obj_in.role_ids)).all()
            db_obj.roles = roles
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update_profile(db: Session, db_obj: User, obj_in: ProfileUpdate) -> User:
        if obj_in.full_name is not None:
            db_obj.full_name = obj_in.full_name
        if obj_in.phone is not None:
            db_obj.phone = obj_in.phone
        if obj_in.cell_phone is not None:
            db_obj.cell_phone = obj_in.cell_phone
        if obj_in.birth_date is not None:
            db_obj.birth_date = obj_in.birth_date
        if obj_in.cedula is not None:
            db_obj.cedula = obj_in.cedula
        if obj_in.linkedin is not None:
            db_obj.linkedin = obj_in.linkedin
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update_password(db: Session, db_obj: User, new_password: str) -> User:
        db_obj.hashed_password = get_password_hash(new_password)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)

    @staticmethod
    def delete(db: Session, user_id: int) -> Optional[User]:
        db_obj = db.query(User).filter(User.id == user_id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[User]:
        user = UserService.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_roles(db: Session) -> List[Role]:
        return db.query(Role).options(joinedload(Role.permissions)).all()

    @staticmethod
    def create_role(db: Session, obj_in: RoleCreate) -> Role:
        db_obj = Role(name=obj_in.name)
        if obj_in.permission_ids:
            perms = db.query(Permission).filter(Permission.id.in_(obj_in.permission_ids)).all()
            db_obj.permissions = perms
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update_role(db: Session, role_id: int, obj_in: RoleUpdate) -> Optional[Role]:
        db_obj = db.query(Role).filter(Role.id == role_id).first()
        if db_obj:
            if obj_in.name:
                db_obj.name = obj_in.name
            if obj_in.permission_ids is not None:
                perms = db.query(Permission).filter(Permission.id.in_(obj_in.permission_ids)).all()
                db_obj.permissions = perms
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete_role(db: Session, role_id: int) -> Optional[Role]:
        db_obj = db.query(Role).filter(Role.id == role_id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

    @staticmethod
    def get_permissions(db: Session) -> List[Permission]:
        return db.query(Permission).all()
