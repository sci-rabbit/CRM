from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from core.models.interaction import Interaction
from core.models.operator import Operator
from core.models.source_operator import SourceOperator
from core.repository.base_repository import AsyncRepository


class OperatorRepository(AsyncRepository[Operator]):
    def __init__(self, session):
        super().__init__(session, Operator)

    async def get_with_load(self, operator_id: int) -> Operator | None:
        stmt = (
            select(Operator)
            .options(selectinload(Operator.interactions))
            .where(Operator.id == operator_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_available_for_source(self, source_id: int):
        active_q = (
            select(func.count(Interaction.id).label("current_load"))
            .where(
                Interaction.is_active == True, Interaction.operator_id == Operator.id
            )
            .correlate(Operator)
            .scalar_subquery()
        )

        stmt = (
            select(Operator, active_q)
            .options(selectinload(Operator.source_configs))
            .join(SourceOperator, SourceOperator.operator_id == Operator.id)
            .where(
                SourceOperator.source_id == source_id,
                Operator.is_active.is_(True),
                active_q < Operator.limit,
            )
        )

        result = await self.session.execute(stmt)
        rows = result.unique().all()
        operators = []
        for op, load in rows:
            op.current_load = load or 0
            operators.append(op)
        return operators

    async def update(self, operator_id: int, **kwargs) -> Operator | None:
        stmt = select(Operator).where(Operator.id == operator_id)
        result = await self.session.execute(stmt)
        operator = result.scalar_one_or_none()
        if not operator:
            return None

        for key, value in kwargs.items():
            if hasattr(operator, key):
                setattr(operator, key, value)

        self.session.add(operator)
        await self.session.commit()
        await self.session.refresh(operator)
        return operator
