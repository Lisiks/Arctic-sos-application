import enum

class WeatherCondition(enum.Enum):
    LOW_TEMPERATURE = "низкие температуры"
    STRONG_WINDS = "сильные ветры"
    HIGH_HUMIDITY = "высокая влажность"
    FOG = "туманы"
    SNOWFALL = "снегопады"
    BLIZZARD = "метели"
    POLAR_NIGHT = "полярная ночь"
    POLAR_DAY = "полярный день"
    LOW_PRESSURE = "низкое атмосферное давление"
    ICING = "обледенение"
    LOW_CLOUDINESS = "малая облачность"
    HIGH_CLOUDINESS = "повышенная облачность"