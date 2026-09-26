import enum

class SourceType(enum.Enum):
    STATION = "станция"
    SHIP = "судно"
    EXPEDITION = "экспедиция"
    AIRCRAFT = "воздушное судно"


class HelpMessageType(enum.Enum):
    FIRE = "пожар"
    ENGINE_FAILURE = "отказ двигателя"
    SHIP_COLLISION = "столкновение судов"
    GROUNDING = "посадка на мель"
    SHIP_CAPSIZE = "накренение / опрокидывание/ затопление судна"
    MAN_OVERBOARD = "падение человека за борт"
    OIL_SPILL = "разлив нефтепродуктов"
    LOSS_OF_COMMUNICATION_WITH_SHIP = "потеря связи с судном"
    EMERGENCY_LANDING = "аварийная посадка"
    AIRCRAFT_CRASH = "падение воздушного судна"
    LOSS_OF_RADIO_COMMUNICATION_WITH_SHIP = "потеря радиосвязи с судном"
    POWER_FAILURE = "отказ энергоснабжения"
    STRUCTURAL_DAMAGE = "обрушение/ повреждение конструкций"
    MISSING_EXPEDITION_MEMBER = "пропажа участника экспедиции"
    ACUTE_ILLNESS_OR_INJURY = "острое заболевание/ травма в полевых условиях"
    EXPEDITION_TRANSPORT_FAILURE = "отказ транспорта экспедиции"


class CommunicationChannelType(enum.Enum):
    COSPAS_SARSAT = "КОСПАС‑САРСАТ"
    SATELLITE_PHONE = "спутниковый телефон"
    RADIO = "радиосвязь"



class IncidentStatus(enum.Enum):
    ACCEPTED = "принято"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершено"
    FALSE_ALARM = "ложное срабатывание"