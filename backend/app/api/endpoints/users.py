from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.user import User, UserCreate, UserUpdate, Role, RoleCreate, RoleUpdate, Permission
from app.services.user_service import UserService
from app.models.user import User as UserModel

router = APIRouter()

# Dependency override or check to ensure ADMIN only
def get_current_admin_user(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
) -> UserModel:
    if "Admin" not in current_user.role_names:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user

@router.get("/", response_model=List[User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_admin_user),
) -> Any:
    """
    Retrieve users.
    """
    users = UserService.get_multi(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: UserModel = Depends(get_current_admin_user),
) -> Any:
    """
    Create new user.
    """
    user = UserService.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    return UserService.create(db, obj_in=user_in)

@router.put("/{user_id}", response_model=User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_admin_user),
) -> Any:
    """
    Update a user.
    """
    user = UserService.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = UserService.update(db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/{user_id}", response_model=User)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: UserModel = Depends(get_current_admin_user),
) -> Any:
    """
    Delete a user.
    """
    user = UserService.delete(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/permissions", response_model=List[Permission])
def read_permissions(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(get_current_admin_user),
) -> Any:
    """
    Retrieve permissions.
    """
    return UserService.get_permissions(db)

@router.get("/roles", response_model=List[Role])
def read_roles(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(get_current_admin_user),
) -> Any:
    """
    Retrieve roles.
    """
    return UserService.get_roles(db)

@router.post("/roles", response_model=Role)
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role_in: RoleCreate,
    current_user: UserModel = Depends(get_current_admin_user),
) -> Any:
    """
    Create new role.
    """
    return UserService.create_role(db, obj_in=role_in)

@router.put("/roles/{role_id}", response_model=Role)
def update_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    role_in: RoleUpdate,
    current_user: UserModel = Depends(get_current_admin_user),
) -> Any:
    """
    Update a role.
    """
    role = UserService.update_role(db, role_id=role_id, obj_in=role_in)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.delete("/roles/{role_id}", response_model=Role)
def delete_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    current_user: UserModel = Depends(get_current_admin_user),
) -> Any:
    """
    Delete a role.
    """
    role = UserService.delete_role(db, role_id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role
