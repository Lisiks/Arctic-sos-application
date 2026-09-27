"""updating_plans_trigger

Revision ID: 860a0b8ac758
Revises: 03b0f37ebb56
Create Date: 2026-09-26 10:23:13.886430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '860a0b8ac758'
down_revision: Union[str, Sequence[str], None] = '03b0f37ebb56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE OR REPLACE FUNCTION insert_update_reaction_plans()
        RETURNS trigger AS $$
        DECLARE
            help_call_latitude NUMERIC(7, 4);
            help_call_longitude NUMERIC(7, 4);
            device_latitude NUMERIC(7, 4);
            device_longitude NUMERIC(7, 4);
            device_status VARCHAR;
            device_type VARCHAR;
            help_message_status VARCHAR;
            device_reach_zone_km NUMERIC(20, 2);
        BEGIN

            SELECT help_messages.status INTO help_message_status
            FROM help_messages
            WHERE help_messages.id = NEW.help_message_id;

            IF (help_message_status = 'завершено' OR help_message_status = 'ложное срабатывание') THEN
                RAISE 'This help message already done';
            END IF;
        
            SELECT help_messages.latitude, help_messages.longitude INTO help_call_latitude, help_call_longitude
            FROM help_messages
            WHERE help_messages.id = NEW.help_message_id;

            SELECT lifesaving_devices.latitude, lifesaving_devices.longitude, lifesaving_devices.status, lifesaving_devices.type, lifesaving_devices.reach_zone_km
            INTO device_latitude, device_longitude, device_status, device_type, device_reach_zone_km
            FROM lifesaving_devices
            WHERE lifesaving_devices.id = NEW.lifesaving_devices_id;

            IF TG_OP = 'INSERT' THEN
                IF (device_status = 'в рейде') OR (device_status = 'на обслуживании') THEN
                    RAISE EXCEPTION 'Lifesaving devices cannot be used for this operation, because its status is %', device_status;
                END IF;
            ELSIF TG_OP = 'UPDATE' THEN
                IF (device_status = 'в рейде' AND OLD.lifesaving_devices_id != NEW.lifesaving_devices_id) OR (device_status = 'на обслуживании') THEN
                    RAISE EXCEPTION 'Lifesaving devices cannot be used for this operation, because its status is %', device_status;
                END IF;
            END IF;

            IF (device_type = 'вертолет' AND ('снегопады' = ANY(NEW.weather_condition) OR 'метели' = ANY(NEW.weather_condition) OR 'сильные ветры' = ANY(NEW.weather_condition) OR 'туманы' = ANY(NEW.weather_condition))) THEN
                RAISE EXCEPTION 'Lifesaving devices cannot be used for this operation, because its type is helicopter and we have bad weather in reaction plan information';
            END IF;

            IF (haversine_km(help_call_latitude, help_call_longitude, device_latitude, device_longitude) > device_reach_zone_km) THEN
                RAISE EXCEPTION 'Lifesaving devices cannot be used for this operation, because it has small reach zone for this operation';
            END IF;

            UPDATE lifesaving_devices
            SET lifesaving_devices.status = 'в рейде'
            WHERE lifesaving_devices.id = NEW.lifesaving_devices_id;

            IF TG_OP = 'UPDATE' THEN
                IF NEW.lifesaving_devices_id != OLD.lifesaving_devices_id THEN
                    UPDATE lifesaving_devices
                    SET lifesaving_devices.status = 'готов'
                    WHERE lifesaving_devices.id = OLD.lifesaving_devices_id;
                END IF;
            END IF;

            IF TG_OP = 'INSERT' THEN
                UPDATE help_messages
                SET help_messages.status = 'в работе'
                WHERE help_messages.id = NEW.help_message_id;
            END IF;

            INSERT INTO reaction_plans_history
            VALUES (NEW.help_message_id, NOW(), NEW.lifesaving_devices_id, NEW.planning_time, NEW.weather_condition);
                
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        CREATE OR REPLACE FUNCTION insert_update_reaction_plans()
        RETURNS trigger AS $$
        DECLARE
            help_call_latitude NUMERIC(7, 4);
            help_call_longitude NUMERIC(7, 4);
            device_latitude NUMERIC(7, 4);
            device_longitude NUMERIC(7, 4);
            device_status VARCHAR;
            device_type VARCHAR;
            device_reach_zone_km NUMERIC(20, 2);
        BEGIN
            SELECT help_messages.latitude, help_messages.longitude INTO help_call_latitude, help_call_longitude
            FROM help_messages
            WHERE help_messages.id = NEW.help_message_id;

            SELECT lifesaving_devices.latitude, lifesaving_devices.longitude, lifesaving_devices.status, lifesaving_devices.type, lifesaving_devices.reach_zone_km
            INTO device_latitude, device_longitude, device_status, device_type, device_reach_zone_km
            FROM lifesaving_devices
            WHERE lifesaving_devices.id = NEW.lifesaving_devices_id;

            IF TG_OP = 'INSERT' THEN
                IF (device_status = 'в рейде') OR (device_status = 'на обслуживании') THEN
                    RAISE EXCEPTION 'Lifesaving devices cannot be used for this operation, because its status is %', device_status;
                END IF;
            ELSIF TG_OP = 'UPDATE' THEN
                IF (device_status = 'в рейде' AND OLD.lifesaving_devices_id != NEW.lifesaving_devices_id) OR (device_status = 'на обслуживании') THEN
                    RAISE EXCEPTION 'Lifesaving devices cannot be used for this operation, because its status is %', device_status;
                END IF;
            END IF;

            IF (device_type = 'вертолет' AND ('снегопады' = ANY(NEW.weather_condition) OR 'метели' = ANY(NEW.weather_condition) OR 'сильные ветры' = ANY(NEW.weather_condition) OR 'туманы' = ANY(NEW.weather_condition))) THEN
                RAISE EXCEPTION 'Lifesaving devices cannot be used for this operation, because its type is helicopter and we have bad weather in reaction plan information';
            END IF;

            IF (haversine_km(help_call_latitude, help_call_longitude, device_latitude, device_longitude) > device_reach_zone_km) THEN
                RAISE EXCEPTION 'Lifesaving devices cannot be used for this operation, because it has small reach zone for this operation';
            END IF;

            UPDATE lifesaving_devices
            SET lifesaving_devices.status = 'в рейде'
            WHERE lifesaving_devices.id = NEW.lifesaving_devices_id;

            IF TG_OP = 'INSERT' THEN
                UPDATE help_messages
                SET help_messages.status = 'в работе'
                WHERE help_messages.id = NEW.help_message_id;
            END IF;

            INSERT INTO reaction_plans_history
            VALUES (NEW.help_message_id, NOW(), NEW.lifesaving_devices_id, NEW.planning_time, NEW.weather_condition);
                
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
