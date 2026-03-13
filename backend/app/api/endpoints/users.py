from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.user import User, UserCreate, UserUpdate, Role, RoleCreate, RoleUpdate, Permission, ProfileUpdate, PasswordChange
from app.services.user_service import UserService
from app.models.user import User as UserModel

router = APIRouter()

# Dependency to get current user (any logged in user)
def get_current_active_user(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user),
) -> UserModel:
    return current_user

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

@router.get("/me", response_model=User)
def read_current_user(
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    Get current user profile.
    """
    return current_user

@router.put("/me", response_model=User)
def update_current_user(
    *,
    db: Session = Depends(deps.get_db),
    profile_in: ProfileUpdate,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    Update current user profile.
    """
    user = UserService.update_profile(db, db_obj=current_user, obj_in=profile_in)
    return user

@router.post("/me/password")
def change_password(
    *,
    db: Session = Depends(deps.get_db),
    password_change: PasswordChange,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    Change current user password.
    """
    if password_change.new_password != password_change.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las contraseñas no coinciden",
        )
    
    if len(password_change.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 6 caracteres",
        )
    
    if not UserService.verify_password(password_change.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña actual es incorrecta",
        )
    
    UserService.update_password(db, db_obj=current_user, new_password=password_change.new_password)
    return {"message": "Contraseña actualizada correctamente"}

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

@router.post("/me/photo")
async def upload_photo(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    Upload user profile photo.
    """
    import os
    import uuid
    from pathlib import Path
    
    # Validar tipo de archivo
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/gif"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Tipo de archivo no permitido. Use JPG, PNG, WebP o GIF.",
        )
    
    # Validar tamaño (max 5MB)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="El archivo no puede superar los 5MB.",
        )
    
    # Crear directorio de uploads si no existe
    upload_dir = Path("static/uploads/user_photos")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Eliminar foto anterior si existe
    old_photo = current_user.photo_url
    if old_photo:
        old_path = upload_dir / Path(old_photo).name
        if old_path.exists():
            try:
                old_path.unlink()
            except Exception:
                pass
    
    # Generar nombre único
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = upload_dir / filename
    
    # Guardar archivo
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Actualizar usuario
    photo_url = f"/uploads/user_photos/{filename}"
    current_user.photo_url = photo_url
    db.commit()
    db.refresh(current_user)
    
    return {"photo_url": photo_url}

@router.delete("/me/photo")
def delete_photo(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    Delete user profile photo.
    """
    from pathlib import Path
    
    if current_user.photo_url:
        photo_path = Path("static") / current_user.photo_url.lstrip("/")
        if photo_path.exists():
            try:
                photo_path.unlink()
            except Exception:
                pass
        
        current_user.photo_url = None
        db.commit()
    
    return {"message": "Foto eliminada correctamente"}
