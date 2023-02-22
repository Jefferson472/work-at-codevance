from apps.antecipation.models import LogTransactions, RequestAntecipation
from apps.user_profile.models import Operator


def log_create(req_antecipation_id, operator_id):
    req_antecipation = RequestAntecipation.objects.get(id=req_antecipation_id)
    operator = Operator.objects.get(id=operator_id)
    LogTransactions.objects.create(
        operator=operator,
        request_antecipation=req_antecipation,
        status_after=req_antecipation.get_status_display(),
        value_before=req_antecipation.payment.value,
        value_after=req_antecipation.payment.value - req_antecipation.fee,
    )
