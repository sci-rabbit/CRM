from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base

if TYPE_CHECKING:
    from core.models.source_operator import SourceOperator
    from core.models.interaction import Interaction


class Operator(Base):
    __tablename__ = "operators"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    limit: Mapped[int] = mapped_column(Integer, nullable=False, default=10)

    interactions: Mapped[list["Interaction"]] = relationship(
        back_populates="operator"
    )

    source_configs: Mapped[list["SourceOperator"]] = relationship(
        back_populates="operator",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
