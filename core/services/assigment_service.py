from sqlalchemy.ext.asyncio import AsyncSession

from core.models.operator import Operator
from core.repository.operator_repository import OperatorRepository
from core.services.interaction_service import InteractionService
from core.services.lead_service import LeadService


class AssignmentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.leads = LeadService(session)
        self.interactions = InteractionService(session)
        self.operators = OperatorRepository(session)

    async def handle_new_interaction(
        self,
        *,
        external_lead_id: str,
        source_id: int,
    ):
        lead = await self.leads.get_or_create(external_lead_id)

        ops = await self.operators.list_available_for_source(source_id)

        if not ops:
            operator_id = None
        else:
            operator_id = self._weighted_round_robin(source_id, ops)

        interaction = await self.interactions.create(
            lead_id=lead.id,
            source_id=source_id,
            operator_id=operator_id,
        )

        await self.session.commit()
        return interaction

    def _weighted_round_robin(
        self,
        source_id: int,
        operators: list[Operator],
    ) -> int:

        candidates = []

        for op in operators:
            cfg = next((c for c in op.source_configs if c.source_id == source_id), None)
            if not cfg:
                continue

            weight = cfg.weight
            current_load = getattr(op, "current_load", 0)

            score = current_load / weight if weight > 0 else float("inf")

            candidates.append((score, weight, op.id))

        candidates.sort(key=lambda x: (x[0], x[1]))
        return candidates[0][2]
