from io import BytesIO
from openpyxl import Workbook
from datetime import datetime
from uuid import uuid4
import enum

class ExcelBuferManager:
    @staticmethod
    def make_message_per_type_report(report_data: tuple) -> BytesIO:
        wb = Workbook()
        ws = wb.active
        ws.title = "Отчёт по кол-ву сообщений по типу происшествия"

        ws.append(["Тип происшествия", "Кол-во сообщений"])

        for report_row in report_data:
            ws.append(tuple(map(lambda element: element.value if issubclass(element.__class__, enum.Enum) else element, report_row)))
        
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        return buffer

    @staticmethod
    def make_avg_reaction_time_report(report_data: tuple) -> BytesIO:
        wb = Workbook()
        ws = wb.active
        ws.title = "Отчёт посреднему времени реагирования"

        ws.append(["Среднее время реагирования сек."])

        for report_row in report_data:
            ws.append(tuple(map(lambda element: element.value if issubclass(element.__class__, enum.Enum) else element, report_row)))
        
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        return buffer

    @staticmethod
    def make_acts_count_report(report_data: tuple) -> BytesIO:
        wb = Workbook()
        ws = wb.active
        ws.title = "Отчёт по количеству ложных срабатываний"

        ws.append(["Кол-во ложных срабатываний", "Кол-во обычных вызовов", "% ложных срабатываний"])

        for report_row in report_data:
            ws.append(tuple(map(lambda element: element.value if issubclass(element.__class__, enum.Enum) else element, report_row)))
        
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        return buffer

    @staticmethod
    def make_devices_ready_count_report(report_data: tuple) -> BytesIO:
        wb = Workbook()
        ws = wb.active
        ws.title = "Отчёт по количеству ложных срабатываний"

        ws.append(["Тип", "Кол-во средств в готовности"])

        for report_row in report_data:
            ws.append(tuple(map(lambda element: element.value if issubclass(element.__class__, enum.Enum) else element, report_row)))
        
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        return buffer

    @staticmethod
    def make_message_per_seasons_report(report_data: tuple) -> BytesIO:
        wb = Workbook()
        ws = wb.active
        ws.title = "Отчёт по кол-ву сообщений по сезонам"

        ws.append(["Сезон", "Кол-во сообщений!"])

        for report_row in report_data:
            ws.append(tuple(map(lambda element: element.value if issubclass(element.__class__, enum.Enum) else element, report_row)))
        
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        return buffer