from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base

if TYPE_CHECKING:
    from core.models.source import Source
    from core.models.operator import Operator

class SourceOperator(Base):
    __tablename__ = "source_operators"


    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id", ondelete="CASCADE"),
        nullable=False,
    )
    operator_id: Mapped[int] = mapped_column(
        ForeignKey("operators.id", ondelete="CASCADE"),
        nullable=False,
    )

    weight: Mapped[int] = mapped_column(Integer, nullable=False)

    source: Mapped["Source"] = relationship(back_populates="operator_configs")
    operator: Mapped["Operator"] = relationship(back_populates="source_configs")

    __table_args__ = (
        UniqueConstraint("source_id", "operator_id", name="uq_source_operator"),
    )
