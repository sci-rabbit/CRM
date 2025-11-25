from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base

if TYPE_CHECKING:
    from core.models.lead import Lead
    from core.models.source import Source
    from core.models.operator import Operator


class Interaction(Base):
    __tablename__ = "interactions"

    created_at: Mapped[datetime]

    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"), nullable=False
    )
    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id", ondelete="CASCADE"), nullable=False
    )
    operator_id: Mapped[int | None] = mapped_column(
        ForeignKey("operators.id", ondelete="SET NULL"),
        nullable=True
    )

    lead: Mapped["Lead"] = relationship(back_populates="interactions")
    source: Mapped["Source"] = relationship(back_populates="interactions")
    operator: Mapped["Operator"] = relationship(back_populates="interactions")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
