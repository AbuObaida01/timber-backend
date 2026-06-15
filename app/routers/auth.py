from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse
from app.services.auth import(
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=TokenResponse, status_code=201)
def register(user_data: UserRegister, db: Session=Depends(get_db)):
    """Register a new user account"""

    #Check if email already exists
    existing=db.query(User).filter(User.email==user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    #Create new user
    new_user=User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=hash_password(user_data.password),
        role="user",
        latitude=user_data.latitude,
        longitude=user_data.longitude
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #create JWT Token
    token=create_access_token({"user_id": new_user.id})

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=new_user
    )

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session=Depends(get_db)):
    """Login and get JWT Token"""

    #Find user by email
    user=db.query(User).filter(User.email==credentials.email).first()

    #Check Password
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tnvalid Email or Password"
        )
    
    #Create JWT Token
    token=create_access_token({"user_id": user.id})

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=user
    )

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User=Depends(get_current_user)):
    """Get your own profile- requires login"""
    return current_user

@router.get("/test-admin")
def test_admin_access(
    db: Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    """Test route - returns your role and email"""
    return{
        "message":f"Hello{current_user.name}",
        "role":current_user.role,
        "email":current_user.email,
        "is_admin":current_user.role=="admin"
    }