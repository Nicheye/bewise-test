from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import SessionLocal, init_db
from app.models import ApplicationDB
from app.schemas import ApplicationCreate, ApplicationOut
from app.kafka import send_message

app = FastAPI()


async def lifespan(app: FastAPI):
    await init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/applications", response_model=ApplicationOut)
async def create_application(
    application: ApplicationCreate, db: AsyncSession = Depends(get_db)
):
    db_application = ApplicationDB(
        user_name=application.user_name, description=application.description
    )

    db.add(db_application)
    await db.commit()
    await db.refresh(db_application)

    await send_message(
        {
            "id": db_application.id,
            "user_name": db_application.user_name,
            "description": db_application.description,
            "created_at": db_application.created_at.isoformat(),
        }
    )

    return ApplicationOut.from_orm(db_application)


@app.get("/applications", response_model=list[ApplicationOut])
async def get_applications(
    user_name: str = None,
    page: int = 1,
    size: int = 10,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(ApplicationDB)

    if user_name:
        stmt = stmt.filter(ApplicationDB.user_name == user_name)

    stmt = stmt.offset((page - 1) * size).limit(size)

    result = await db.execute(stmt)
    applications = result.scalars().all()

    return [ApplicationOut.model_validate(app) for app in applications]
