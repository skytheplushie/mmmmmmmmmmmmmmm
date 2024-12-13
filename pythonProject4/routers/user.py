from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import User
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    users = db.scalars(select(User).where(User.id == user_id))
    for user in users:
        if user is not None:
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user_model: CreateUser):
    db.execute(insert(User).values(username=create_user_model.username, firstname=create_user_model.firstname,
                                   lastname=create_user_model.lastname, age=create_user_model.age))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user_model: UpdateUser):
    users = db.scalars(select(User).where(User.id == user_id))
    for user in users:
        if user is not None:
            db.execute(update(User).values(firstname=update_user_model.firstname, lastname=update_user_model.lastname,
                                           age=update_user_model.age))
            db.commit()
            return {'status_code': status.HTTP_200_OK,
                    'transaction': 'User update is successful!'}
    raise HTTPException(status_code=404, detail='User was not found')


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    users = db.scalars(select(User).where(User.id == user_id))
    for user in users:
        if user is not None:
            db.execute(delete(User).where(User.id == user_id))
            db.commit()
            return {'status_code': status.HTTP_200_OK,
                    'transaction': 'User deletion was successful!'}
    raise HTTPException(status_code=404, detail='User was not found')