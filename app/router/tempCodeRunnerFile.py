@router.post('/login')
def login_user(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() # The email is actually stored in the 'uersname' field of the OAuth2PasswordRequestForm

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials!")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials!")
    
    token = oauth2.create_access_token(data={"user_id": user.id, "message": "Asif da boss!"})

    return {"token": token, "token_type":"bearer"}
