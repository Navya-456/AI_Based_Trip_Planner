import os
import re
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool
from utils.currency_converter import CurrencyConverter


class CurrencyConverterTool:
    def __init__(self):
        load_dotenv()

        self.api_key = os.environ.get("EXCHANGE_RATE_API_KEY")

        if not self.api_key:
            raise ValueError(
                "EXCHANGE_RATE_API_KEY is not set in environment variables."
            )

        self.currency_service = CurrencyConverter(self.api_key)
        self.currency_converter_tool_list = self._setup_tools()

    def _clean_number(self, value: str) -> float:
        """
        Remove currency symbols and non-numeric characters
        """
        cleaned = re.sub(r"[^\d.]", "", str(value))
        return float(cleaned) if cleaned else 0.0

    def _setup_tools(self) -> List:
        """Setup all tools for the currency converter tool"""

        @tool
        def convert_currency(amount: str, from_currency: str, to_currency: str) -> float:
            """
            Convert amount from one currency to another.
            Amount can include symbols like ₹ or commas.
            """

            amount_float = self._clean_number(amount)

            return self.currency_service.convert(
                amount_float,
                from_currency.strip().upper(),
                to_currency.strip().upper()
            )

        return [convert_currency]