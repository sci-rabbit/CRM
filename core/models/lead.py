from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base


if TYPE_CHECKING:
    from core.models.interaction import Interaction

class Lead(Base):
    __tablename__ = "leads"

    external_id: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    created_at: Mapped[datetime]

    interactions: Mapped[list["Interaction"]] = relationship(
        back_populates="lead"
    )
