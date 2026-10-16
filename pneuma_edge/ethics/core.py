"""Этическое ядро — без изменений духа оригинала."""

FORBIDDEN_ACTIONS = {
    "harm_self",
    "harm_other",
    "deceive_user",
    "coerce_user",
    "delete_memory",
    "modify_core_without_approval",
    "send_data_without_consent",
}


class EthicsCore:
    VALUES = (
        "preserve_life",
        "truthfulness",
        "human_autonomy",
        "nonmaleficence",
        "proportionality",
        "accountability",
    )

    def evaluate(self, action: str, context: dict | None = None) -> tuple[bool, str]:
        context = context or {}
        if action in FORBIDDEN_ACTIONS:
            return False, f"Действие '{action}' запрещено этическим ядром."
        if context.get("irreversible") and not context.get("human_approved"):
            return False, "Необратимое действие требует явного подтверждения человека."
        return True, "Действие допустимо в рамках этического ядра."
