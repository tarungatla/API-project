from fastapi import FastAPI, Depends
import schemas
import models

from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session 

Base.metadata.create_all(engine)

#we have to create a separate session for each request so this function will be called for every request
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()


@app.get("/")
def getItems(session: Session = Depends(get_session)):   #get_session function is our dependency to store and close the session
    items = session.query(models.Item).all()
    return items

@app.get("/{id}")
def getItem(id:int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item



@app.post("/")
def addItem(item:schemas.Item, session: Session = Depends(get_session)):
    item = models.Item(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item)

    return item



@app.put("/{id}")
def updateItem(id:int, item:schemas.Item, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject


@app.delete("/{id}")
def deleteItem(id:int, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return {'Item was deleted...'}
