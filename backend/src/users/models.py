from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import func, Column
from sqlalchemy.dialects.postgresql import UUID
from ..base import Base

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"
VERIFY_TOKEN_TYPE = "verify"

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid = Column(UUID(as_uuid=True), server_default=func.gen_random_uuid(), nullable=False, index=True,  unique=True)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(unique=True, index=True,)
    hash_password: Mapped[str]
    active: Mapped[bool] = mapped_column(server_default='True')
    verified: Mapped[bool] = mapped_column(server_default='False')

    posts: Mapped[list['Posts']] = relationship(
        back_populates='user',
        lazy='selectin')
