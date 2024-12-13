from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import Task, User
from schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    tasks = db.scalars(select(Task).where(Task.id == task_id))
    for task in tasks:
        if task is not None:
            return task
    raise HTTPException(status_code=404, detail='Task was not found')


@router.post('/create')
async def create_task(
        db: Annotated[Session, Depends(get_db)],
        task_create_model: CreateTask,
        user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        db.execute(insert(Task).values(title=task_create_model.title,
                                       content=task_create_model.content,
                                       user_id=user.id))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED,
                'transaction': 'Successful'}


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task_model: UpdateTask):
    tasks = db.scalars(update(Task).where(Task.id == task_id))
    for task in tasks:
        if task is not None:
            db.execute(update(User).values(title=update_task_model.title, content=update_task_model.content,
                                           priority=update_task_model.priority))
            db.commit()
            return {'status_code': status.HTTP_200_OK,
                    'transaction': 'Task update is successful!'}
    raise HTTPException(status_code=404, detail='Task was not found')


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    tasks = db.scalars(select(Task).where(Task.id == task_id))
    for task in tasks:
        if task is not None:
            db.execute(delete(User).where(Task.id == task_id))
            db.commit()
            return {'status_code': status.HTTP_200_OK,
                    'transaction': 'Task deletion was successful!'}
    raise HTTPException(status_code=404, detail='Task was not found')