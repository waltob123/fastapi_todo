from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from ..models import Tasks, Users
from ..database import get_db
from ..auth_jwt import get_current_user
from ..schemas import Task, TaskResponseModel
from ..utils import set_all_inactive_tasks_to_false


router = APIRouter(prefix='/tasks', tags=['Tasks'])

# create tasks
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=TaskResponseModel)
def create_task(task: Task, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    new_task = Tasks(**task.dict())

    # set task user_id to the current user id
    new_task.user_id = current_user.id
    try:
        db.add(new_task)
        db.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'cannot add task')
    else:
        set_all_inactive_tasks_to_false()
        db.refresh(new_task)
    return new_task


# get all tasks
@router.get('/')
def get_all_tasks(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    set_all_inactive_tasks_to_false()
    tasks = db.query(Tasks).filter(Tasks.user_id == current_user.id).all()

    if tasks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='tasks not found')
    return tasks


# get one task
@router.get('/{id}', response_model=TaskResponseModel)
def get_one_task(id: int, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    set_all_inactive_tasks_to_false()
    task = db.query(Tasks).filter(Tasks.user_id == current_user.id).filter(Tasks.id == id).first()
    
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'task with id:{id} not found')
    return task


# update one task
@router.put('/{id}', response_model=TaskResponseModel)
def get_one_task(id: int, task: Task, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    set_all_inactive_tasks_to_false()
    task_to_update_query = db.query(Tasks).filter(Tasks.user_id == current_user.id).filter(Tasks.id == id)
    task_to_update = task_to_update_query.first()
    
    if task_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'task with id:{id} not found')
    
    task_to_update_query.update(task.dict(), synchronize_session=False)
    db.commit()
    return task_to_update


# delete one task
@router.delete('/{id}')
def get_one_task(id: int, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    set_all_inactive_tasks_to_false()
    task_to_delete_query = db.query(Tasks).filter(Tasks.user_id == current_user.id).filter(Tasks.id == id)
    task_to_delete = task_to_delete_query.first()
    
    if task_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'task with id:{id} not found')
    
    task_to_delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
