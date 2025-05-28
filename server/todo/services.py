import dataclasses
import requests

from bs4 import BeautifulSoup
from datetime import datetime, date

from .models import TechParkParticipants


ASTANA_HUB_URL = "https://astanahub.com/ru/service/techpark/"
ACTIVE_STATUS = "Активно"


class TechParkParticipantsServiceException(Exception):
    pass


@dataclasses.dataclass
class Participant:
    serial_number: int
    join_date: date
    end_date: date
    bin: int
    status: bool
    company_name: str


class TechParkParticipantsService:

    @classmethod
    def create_participants(cls) -> None:
        participants = cls._fetch_participants()
        for participant in participants:
            TechParkParticipants.objects.get_or_create(
                serial_number=participant.serial_number,
                join_date=participant.join_date,
                end_date=participant.end_date,
                status=participant.status,
                bin=participant.bin,
                company_name=participant.company_name,
            )

    @classmethod
    def _fetch_participants(cls) -> list:
        response = requests.get(
            ASTANA_HUB_URL, headers={"content-type": "application/json"}
        )
        if response.status_code != 200:
            raise TechParkParticipantsServiceException("Something went wrong.")

        return cls._parse_response(response.text)

    @classmethod
    def _parse_response(cls, response_text: str) -> list:
        soup = BeautifulSoup(response_text, "html.parser")
        rows = soup.find_all("tr", limit=11)

        participants = []
        for row in rows:
            cells = row.find_all("td")
            parsed_row_value = [cell.get_text(strip=True) for cell in cells]
            if parsed_row_value:
                participant = Participant(
                    serial_number=int(parsed_row_value[0]),
                    join_date=cls._convert_str_to_date(parsed_row_value[1]),
                    end_date=cls._convert_str_to_date(parsed_row_value[2]),
                    bin=int(parsed_row_value[3]),
                    status=True if parsed_row_value[4] == ACTIVE_STATUS else False,
                    company_name=parsed_row_value[5],
                )
                participants.append(participant)

        return participants

    @staticmethod
    def _convert_str_to_date(date_str: str) -> date:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
