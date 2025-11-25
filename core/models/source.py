from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base

if TYPE_CHECKING:
    from core.models.source_operator import SourceOperator
    from core.models.interaction import Interaction

class Source(Base):
    __tablename__ = "sources"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    operator_configs: Mapped[list["SourceOperator"]] = relationship(
        back_populates="source",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    interactions: Mapped[list["Interaction"]] = relationship(
        back_populates="source"
    )
