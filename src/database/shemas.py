from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import NUMERIC, Enum, Text, DateTime, ForeignKey, CheckConstraint, String, ARRAY, PrimaryKeyConstraint, Text
from datetime import datetime

from ..enums import *

class Base(DeclarativeBase):
    ...



class HelpMessages(Base):
    __tablename__ = "help_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_type: Mapped[str] = mapped_column(Enum(SourceType, name="sourse_type"))
    latitude: Mapped[float] = mapped_column(NUMERIC(7, 4))
    longitude: Mapped[float] = mapped_column(NUMERIC(7, 4))
    
    incident_type: Mapped[str] = mapped_column(Enum(HelpMessageType, name="help_message_type"))
    incident_description: Mapped[str] = mapped_column(Text)
    chanell_type: Mapped[str] = mapped_column(Enum(CommunicationChannelType, name="communication_channel_type"))
    datetime: Mapped[datetime] = mapped_column(DateTime, index=True)
    status: Mapped[str] = mapped_column(Enum(IncidentStatus, name="incident_status"))

    __table_args__ = (
        CheckConstraint("latitude >= -180.0 AND latitude <= 180.0", name="latitude_ck"),
        CheckConstraint("longitude >= -180.0 AND longitude <= 180.0", name="longitude_ck")
    )


class LifesavingDevices(Base):
    __tablename__ = "lifesaving_devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Enum(RescueAssetType, name="rescue_asset_type"))
    latitude: Mapped[float] = mapped_column(NUMERIC(7, 4))
    longitude: Mapped[float] = mapped_column(NUMERIC(7, 4))
    reach_zone_km: Mapped[float] = mapped_column(NUMERIC(20, 2))
    status: Mapped[str] = mapped_column(Enum(RescueAssetStatus, name="rescue_asset_status"))

    __table_args__ = (
        CheckConstraint("latitude >= -180.0 AND latitude <= 180.0", name="latitude_ck"),
        CheckConstraint("longitude >= -180.0 AND longitude <= 180.0", name="longitude_ck"),
        CheckConstraint("reach_zone_km >= 0.01", name="reach_zone_km_ck")
    )

    crews: Mapped[list["Crews"]] = relationship(
        back_populates="lifesaving_device",
        cascade="all, delete-orphan"
    )


class Crews(Base):
    __tablename__ = "crews"

    id: Mapped[int] = mapped_column(primary_key=True)
    f: Mapped[str] = mapped_column(String(100))
    i: Mapped[str] = mapped_column(String(100))
    o: Mapped[str] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(Enum(Position, name="crew_position"))
    lifesaving_devices_id: Mapped[int] = mapped_column(ForeignKey("lifesaving_devices.id", name="lifesaving_device_fk", ondelete="RESTRICT", onupdate="CASCADE"))

    lifesaving_device: Mapped["LifesavingDevices"] = relationship(
        back_populates="crews"
    )

class ReactionPlans(Base):
    __tablename__ = "reaction_plans"

    help_message_id: Mapped[int] = mapped_column(ForeignKey("help_messages.id", name="help_message_fk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    lifesaving_devices_id: Mapped[int] = mapped_column(ForeignKey("lifesaving_devices.id", name="lifesaving_device_fk", ondelete="RESTRICT", onupdate="CASCADE"))
    planning_datetime: Mapped[datetime] = mapped_column(DateTime)
    weather_condition: Mapped[list[str]] = mapped_column(ARRAY(Enum(WeatherCondition, name="weather_condition")))

    lifesaving_device: Mapped["LifesavingDevices"] = relationship()
    help_message: Mapped["HelpMessages"] = relationship()

class ReactionPlansHistory(Base):
    __tablename__ = "reaction_plans_history"

    help_message_id: Mapped[int] = mapped_column(ForeignKey("reaction_plans.help_message_id", name="reaction_plans_fk", ondelete="CASCADE", onupdate="CASCADE"))
    change_datetime: Mapped[datetime] = mapped_column(DateTime, index=True)
    lifesaving_devices_id: Mapped[int] = mapped_column(ForeignKey("lifesaving_devices.id", name="lifesaving_device_fk", ondelete="RESTRICT", onupdate="CASCADE"))
    planning_time: Mapped[datetime] = mapped_column(DateTime)
    weather_condition: Mapped[list[str]] = mapped_column(ARRAY(Enum(WeatherCondition, name="weather_condition")))

    lifesaving_device: Mapped["LifesavingDevices"] = relationship()

    __table_args__ = (
        PrimaryKeyConstraint("help_message_id", "change_datetime", name="plans_history_pk"),
    )



class OperationActs(Base):
    __tablename__ = "operation_acts"

    help_message_id: Mapped[int] = mapped_column(ForeignKey("help_messages.id", name="help_message_fk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    resque_count: Mapped[int] = mapped_column()
    help_info: Mapped[str] = mapped_column(Text)
    resourses_info: Mapped[str] = mapped_column(Text)
    fact_datetime: Mapped[datetime] = mapped_column(DateTime)

    __table_args__ = (
        CheckConstraint("resque_count >= 0", name="resque_count_ck"),
    )

    help_message: Mapped["HelpMessages"] = relationship()


class LieActs(Base):
    __tablename__ = "lie_acts"

    help_message_id: Mapped[int] = mapped_column(ForeignKey("help_messages.id", name="help_message_fk", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    reason_description: Mapped[str] = mapped_column(Text)
    action_description: Mapped[str] = mapped_column(Text)
    fact_datetime: Mapped[datetime] = mapped_column(DateTime)

    help_message: Mapped["HelpMessages"] = relationship()




