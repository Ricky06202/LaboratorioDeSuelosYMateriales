from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from app.schemas.user import Token, User, UserCreate
from app.services.user_service import UserService
from app.models.user import Role

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = UserService.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=60 * 24) # 24 hours
    role_names = user.role_names if user.roles else ["Visor"]
    
    # Aggregate permission codes
    permissions = []
    for role in user.roles:
        for perm in role.permissions:
            if perm.code not in permissions:
                permissions.append(perm.code)
    
    return {
        "access_token": security.create_access_token(
            user.id, roles=role_names, permissions=permissions, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=User)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate
) -> Any:
    """
    Public registration endpoint. Assigns 'Visor' role by default.
    """
    user = UserService.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    # Get default role 'Visor'
    visor_role = db.query(Role).filter(Role.name == "Visor").first()
    if not visor_role:
        visor_role = Role(name="Visor")
        db.add(visor_role)
        db.commit()
        db.refresh(visor_role)
    
    user_in.role_ids = [visor_role.id]
    return UserService.create(db, obj_in=user_in)
