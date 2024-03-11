from enum import Enum


class LangEnum(Enum):
    EN = "en"
    UZ = "uz"


print(LangEnum['EN'].value)

class MoneyEnum(Enum):
    DOLLAR = "$"
    CENT = "¢"
    SUM = "S"


class VolEnum(Enum):
    HARD = "Hard"
    SOFT = "Soft"


class OrderStatusEnum(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
