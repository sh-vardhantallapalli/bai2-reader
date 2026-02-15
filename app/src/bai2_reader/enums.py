"""All Enumeration are defined here"""

import warnings

from enum import Enum
from dataclasses import dataclass
from functools import cached_property
from src.bai2_reader.exceptions import UnknownValueException


class OutputFormat(str, Enum):
    """An enumeration representing the different formats that the parsed BAI2 data can be written to."""

    CSV = "csv"
    JSON = "json"
    EXCEL = "excel"
    PARQUET = "parquet"


class Record(str, Enum):
    """An enumeration representing the different types of records in a BAI2 file."""

    file_header = "01"
    group_header = "02"
    account_identifier = "03"
    transaction = "16"
    account_trailer = "49"
    continuation = "88"
    group_trailer = "98"
    file_trailer = "99"


class GroupStatus(str, Enum):
    """An enumeration representing the different group status codes in a BAI2 file."""

    new = "1"
    update = "2"
    delete = "3"
    test_only = "4"


class AsOfDateModifier(str, Enum):
    """An enumeration representing the different as-of date modifiers in a BAI2 file."""

    interim_previous_day = "1"
    final_previous_day = "2"
    interim_same_day = "3"
    final_same_day = "4"


class FundsType(str, Enum):
    """An enumeration representing the different funds types in a BAI2 file."""

    unknown_availability = "Z"
    immediate_availability = "0"
    one_day_availability = "1"
    two_day_availability = "2"
    distributed_availability_simple = "S"
    value_dated = "V"
    distributed_availability = "D"


class TransactionType(str, Enum):
    """An enumeration representing the different transaction types in a BAI2 file."""

    credit = "CR"
    debit = "DB"
    misc = "M"


class TypeCodeLevel(str, Enum):
    """An enumeration representing the different type code levels in a BAI2 file."""

    status = "status"
    detail = "detail"
    summary = "summary"


class TypeCodes:
    """A class representing the different type codes in a BAI2 file,
    including the transaction type, type level code, and description.
    """

    @dataclass
    class TypeCode:
        """A data class representing the details of a type code,
        including the transaction type, type level code, and description.
        """

        transaction_type: TransactionType | None = None
        type_level_code: TypeCodeLevel | None = None
        description: str | None = ""

    def get_type_code(self, type_code: str, ignore_if_not_found: bool = True):
        """Get the details of a type code by its code.
        set ignore_if_not_found to false to raise an exception if the type code is not found,
        otherwise it will return empty details and log a warning
        """
        details = self.type_codes.get(type_code)

        if details is None and ignore_if_not_found:
            warnings.warn(f"Type code {type_code} not found, returning empty details")
            details = self.TypeCode()

        if details is None and not ignore_if_not_found:
            raise UnknownValueException(f"Type code {type_code} not found")

        return self.TypeCode(**details)

    @cached_property
    def type_codes(self) -> dict[str, dict[str, str | TransactionType | TypeCodeLevel]]:
        """Get all Typecode details
        Thanks to : https://github.com/mrrozz/bai2-codes-csv/blob/master/bai-codes.csv
        """
        return {
            "010": {"transaction_type": None, "type_level_code": TypeCodeLevel.status, "description": "Opening Ledger"},
            "011": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Opening Ledger MTD",
            },
            "012": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Opening Ledger YTD",
            },
            "015": {"transaction_type": None, "type_level_code": TypeCodeLevel.status, "description": "Closing Ledger"},
            "020": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Closing Ledger MTD",
            },
            "021": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Closing Ledger – Previous Month",
            },
            "022": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Aggregate Balance Adjustments",
            },
            "024": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Closing Ledger YTD – Previous Month",
            },
            "025": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Closing Ledger YTD",
            },
            "030": {"transaction_type": None, "type_level_code": TypeCodeLevel.status, "description": "Current Ledger"},
            "037": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "ACH Net Position",
            },
            "039": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Opening Available + Total Same-Day ACH DTC Deposit",
            },
            "040": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Opening Available",
            },
            "041": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Opening Available MTD",
            },
            "042": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Opening Available YTD",
            },
            "043": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Available – Previous Month",
            },
            "044": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Disbursing Opening Available Balance",
            },
            "045": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Status Closing Available",
            },
            "050": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Closing Available MTD",
            },
            "051": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Closing Available – Last Month",
            },
            "054": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Closing Available YTD – Last Month",
            },
            "055": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Closing Available YTD",
            },
            "056": {"transaction_type": None, "type_level_code": TypeCodeLevel.status, "description": "Loan Balance"},
            "057": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Total Investment Position",
            },
            "059": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Current Available (CRS Supressed)",
            },
            "060": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Current Available",
            },
            "061": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Current Available MTD",
            },
            "062": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Current Available YTD",
            },
            "063": {"transaction_type": None, "type_level_code": TypeCodeLevel.status, "description": "Total Float"},
            "065": {"transaction_type": None, "type_level_code": TypeCodeLevel.status, "description": "Target Balance"},
            "066": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Adjusted Balance",
            },
            "067": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Adjusted Balance MTD",
            },
            "068": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Adjusted Balance YTD",
            },
            "070": {"transaction_type": None, "type_level_code": TypeCodeLevel.status, "description": "0-Day Float"},
            "072": {"transaction_type": None, "type_level_code": TypeCodeLevel.status, "description": "1-Day Float"},
            "073": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Float Adjustment",
            },
            "074": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "2 or More Days Float",
            },
            "075": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "3 or More Days Float",
            },
            "076": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Adjustment to Balances",
            },
            "077": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Adjustment to Balances MTD",
            },
            "078": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average Adjustment to Balances YTD",
            },
            "079": {"transaction_type": None, "type_level_code": TypeCodeLevel.status, "description": "4-Day Float"},
            "080": {"transaction_type": None, "type_level_code": TypeCodeLevel.status, "description": "5-Day Float"},
            "081": {"transaction_type": None, "type_level_code": TypeCodeLevel.status, "description": "6-Day Float"},
            "082": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average 1-Day Float MTD",
            },
            "083": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average 1-Day Float YTD",
            },
            "084": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average 2-Day Float MTD",
            },
            "085": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Average 2-Day Float YTD",
            },
            "086": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Transfer Calculation",
            },
            "100": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Credits",
            },
            "101": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Credit Amount MTD",
            },
            "105": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Credits Not Detailed",
            },
            "106": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Deposits Subject to Float",
            },
            "107": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Adjustment Credits YTD",
            },
            "108": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Credit (Any Type)",
            },
            "109": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Current Day Total Lockbox Deposits",
            },
            "110": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Lockbox Deposits",
            },
            "115": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Lockbox Deposit",
            },
            "116": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Item in Lockbox Deposit",
            },
            "118": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Lockbox Adjustment Credit",
            },
            "120": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "EDI* Transaction Credit",
            },
            "121": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "EDI Transaction Credit",
            },
            "122": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "EDIBANX Credit Received",
            },
            "123": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "EDIBANX Credit Return",
            },
            "130": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Concentration Credits",
            },
            "131": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total DTC Credits",
            },
            "135": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "DTC Concentration Credit",
            },
            "136": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Item in DTC Deposit",
            },
            "140": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total ACH Credits",
            },
            "142": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ACH Credit Received",
            },
            "143": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Item in ACH Deposit",
            },
            "145": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ACH Concentration Credit",
            },
            "146": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Bank Card Deposits",
            },
            "147": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Bank Card Deposit",
            },
            "150": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Preauthorized Payment Credits",
            },
            "155": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Preauthorized Draft Credit",
            },
            "156": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Item in PAC Deposit",
            },
            "160": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total ACH Disbursing Funding Credits",
            },
            "162": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Corporate Trade Payment Settlement",
            },
            "163": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Corporate Trade Payment Credits",
            },
            "164": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Corporate Trade Payment Credit",
            },
            "165": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Preauthorized ACH Credit",
            },
            "166": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ACH Settlement",
            },
            "167": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "ACH Settlement Credits",
            },
            "168": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ACH Return Item or Adjustment Settlement",
            },
            "169": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Miscellaneous ACH Credit",
            },
            "170": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Other Check Deposits",
            },
            "171": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Loan Deposit",
            },
            "172": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Deposit Correction",
            },
            "173": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Bank-Prepared Deposit",
            },
            "174": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Other Deposit",
            },
            "175": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Check Deposit Package",
            },
            "176": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Re-presented Check Deposit",
            },
            "178": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "List Post Credits",
            },
            "180": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Loan Proceeds",
            },
            "182": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Bank-Prepared Deposits",
            },
            "184": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Draft Deposit",
            },
            "185": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Miscellaneous Deposits",
            },
            "186": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Cash Letter Credits",
            },
            "187": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Cash Letter Credit",
            },
            "188": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Cash Letter Adjustments",
            },
            "189": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Cash Letter Adjustment",
            },
            "190": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Incoming Money Transfers",
            },
            "191": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Incoming Internal Money Transfer",
            },
            "195": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Incoming Money Transfer",
            },
            "196": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Money Transfer Adjustment",
            },
            "198": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Compensation",
            },
            "200": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Automatic Transfer Credits",
            },
            "201": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Automatic Transfer Credit",
            },
            "202": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Bond Operations Credit",
            },
            "205": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Book Transfer Credits",
            },
            "206": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Book Transfer Credit",
            },
            "207": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total International Money Transfer Credits",
            },
            "208": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual International Money Transfer Credit",
            },
            "210": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total International Credits",
            },
            "212": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Foreign Letter of Credit",
            },
            "213": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Letter of Credit",
            },
            "214": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Foreign Exchange of Credit",
            },
            "215": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Letters of Credit",
            },
            "216": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Foreign Remittance Credit",
            },
            "218": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Foreign Collection Credit",
            },
            "221": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Foreign Check Purchase",
            },
            "222": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Foreign Checks Deposited",
            },
            "224": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Commission",
            },
            "226": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "International Money Market Trading",
            },
            "227": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Standing Order",
            },
            "229": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Miscellaneous International Credit",
            },
            "230": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Security Credits",
            },
            "231": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Collection Credits",
            },
            "232": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Sale of Debt Security",
            },
            "233": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Securities Sold",
            },
            "234": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Sale of Equity Security",
            },
            "235": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Matured Reverse Repurchase Order",
            },
            "236": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Maturity of Debt Security",
            },
            "237": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Collection Credit",
            },
            "238": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Collection of Dividends",
            },
            "239": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Bankers’ Acceptance Credits",
            },
            "240": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Coupon Collections – Banks",
            },
            "241": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Bankers’ Acceptances",
            },
            "242": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Collection of Interest Income",
            },
            "243": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Matured Fed Funds Purchased",
            },
            "244": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Interest/Matured Principal Payment",
            },
            "245": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Monthly Dividends",
            },
            "246": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Commercial Paper",
            },
            "247": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Capital Change",
            },
            "248": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Savings Bonds Sales Adjustment",
            },
            "249": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Miscellaneous Security Credit",
            },
            "250": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Checks Posted and Returned",
            },
            "251": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Debit Reversals",
            },
            "252": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Debit Reversal",
            },
            "254": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Posting Error Correction Credit",
            },
            "255": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Check Posted and Returned",
            },
            "256": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total ACH Return Items",
            },
            "257": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual ACH Return Item",
            },
            "258": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ACH Reversal Credit",
            },
            "260": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Rejected Credits",
            },
            "261": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Rejected Credit",
            },
            "263": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Overdraft",
            },
            "266": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Return Item",
            },
            "268": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Return Item Adjustment",
            },
            "270": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total ZBA Credits",
            },
            "271": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Net Zero-Balance Amount",
            },
            "274": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Cumulative** ZBA or Disbursement Credits",
            },
            "275": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ZBA Credit",
            },
            "276": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ZBA Float Adjustment",
            },
            "277": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ZBA Credit Transfer",
            },
            "278": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ZBA Credit Adjustment",
            },
            "280": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Controlled Disbursing Credits",
            },
            "281": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Controlled Disbursing Credit",
            },
            "285": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total DTC Disbursing Credits",
            },
            "286": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual DTC Disbursing Credit",
            },
            "294": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total ATM Credits",
            },
            "295": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ATM Credit",
            },
            "301": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Commercial Deposit",
            },
            "302": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Correspondent Bank Deposit",
            },
            "303": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Wire Transfers In – FF",
            },
            "304": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Wire Transfers In – CHF",
            },
            "305": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Fed Funds Sold",
            },
            "306": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Fed Funds Sold",
            },
            "307": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Trust Credits",
            },
            "308": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Trust Credit",
            },
            "309": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Value - Dated Funds",
            },
            "310": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Commercial Deposits",
            },
            "315": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total International Credits – FF",
            },
            "316": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total International Credits – CHF",
            },
            "318": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Foreign Check Purchased",
            },
            "319": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Late Deposit",
            },
            "320": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Securities Sold – FF",
            },
            "321": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Securities Sold – CHF",
            },
            "324": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Securities Matured – FF",
            },
            "325": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Securities Matured – CHF",
            },
            "326": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Securities Interest",
            },
            "327": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Securities Matured",
            },
            "328": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Securities Interest – FF",
            },
            "329": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Securities Interest – CHF",
            },
            "330": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Escrow Credits",
            },
            "331": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Escrow Credit",
            },
            "332": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Miscellaneous Securities Credits – FF",
            },
            "336": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Miscellaneous Securities Credits – CHF",
            },
            "338": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Securities Sold",
            },
            "340": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Broker Deposits",
            },
            "341": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Broker Deposits – FF",
            },
            "342": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Broker Deposit",
            },
            "343": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Broker Deposits – CHF",
            },
            "344": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Back Value Credit",
            },
            "345": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Item in Brokers Deposit",
            },
            "346": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Sweep Interest Income",
            },
            "347": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Sweep Principal Sell",
            },
            "348": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Futures Credit",
            },
            "349": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Principal Payments Credit",
            },
            "350": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Investment Sold",
            },
            "351": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Investment Sold",
            },
            "352": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Cash Center Credits",
            },
            "353": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Cash Center Credit",
            },
            "354": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Interest Credit",
            },
            "355": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Investment Interest",
            },
            "356": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Credit Adjustment",
            },
            "357": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Credit Adjustment",
            },
            "358": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "YTD Adjustment Credit",
            },
            "359": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Interest Adjustment Credit",
            },
            "360": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Credits Less Wire Transfer and Returned Checks",
            },
            "361": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Grand Total Credits Less Grand Total Debits",
            },
            "362": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Correspondent Collection",
            },
            "363": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Correspondent Collection Adjustment",
            },
            "364": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Loan Participation",
            },
            "366": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Currency and Coin Deposited",
            },
            "367": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Food Stamp Letter",
            },
            "368": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Food Stamp Adjustment",
            },
            "369": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Clearing Settlement Credit",
            },
            "370": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Back Value Credits",
            },
            "372": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Back Value Adjustment",
            },
            "373": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Customer Payroll",
            },
            "374": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Statement Recap",
            },
            "376": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Savings Bond Letter or Adjustment",
            },
            "377": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Treasury Tax and Loan Credit",
            },
            "378": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Transfer of Treasury Credit",
            },
            "379": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Government Checks Cash Letter Credit",
            },
            "381": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Government Check Adjustment",
            },
            "382": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Postal Money Order Credit",
            },
            "383": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Postal Money Order Adjustment",
            },
            "384": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Cash Letter Auto Charge Credit",
            },
            "385": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Universal Credits",
            },
            "386": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Cash Letter Auto Charge Adjustment",
            },
            "387": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Fine-Sort Cash Letter Credit",
            },
            "388": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Fine-Sort Adjustment",
            },
            "389": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Freight Payment Credits",
            },
            "390": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Miscellaneous Credits",
            },
            "391": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Universal Credit",
            },
            "392": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Freight Payment Credit",
            },
            "393": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Itemized Credit Over $10,000",
            },
            "394": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Cumulative** Credits",
            },
            "395": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Check Reversal",
            },
            "397": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Float Adjustment",
            },
            "398": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Miscellaneous Fee Refund",
            },
            "399": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Miscellaneous Credit",
            },
            "400": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Debits",
            },
            "401": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Debit Amount MTD",
            },
            "403": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Today’s Total Debits",
            },
            "405": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Debit Less Wire Transfers and Charge- Backs",
            },
            "406": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Debits not Detailed",
            },
            "408": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Float Adjustment",
            },
            "409": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Debit (Any Type)",
            },
            "410": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total YTD Adjustment",
            },
            "412": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Debits (Excluding Returned Items)",
            },
            "415": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Lockbox Debit",
            },
            "416": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Lockbox Debits",
            },
            "420": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "EDI Transaction Debits",
            },
            "421": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "EDI Transaction Debit",
            },
            "422": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "EDIBANX Settlement Debit",
            },
            "423": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "EDIBANX Return Item Debit",
            },
            "430": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Payable–Through Drafts",
            },
            "435": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Payable–Through Draft",
            },
            "445": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ACH Concentration Debit",
            },
            "446": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total ACH Disbursement Funding Debits",
            },
            "447": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ACH Disbursement Funding Debit",
            },
            "450": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total ACH Debits",
            },
            "451": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ACH Debit Received",
            },
            "452": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Item in ACH Disbursement or Debit",
            },
            "455": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Preauthorized ACH Debit",
            },
            "462": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Account Holder Initiated ACH Debit",
            },
            "463": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Corporate Trade Payment Debits",
            },
            "464": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Corporate Trade Payment Debit",
            },
            "465": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Corporate Trade Payment Settlement",
            },
            "466": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ACH Settlement",
            },
            "467": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "ACH Settlement Debits",
            },
            "468": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ACH Return Item or Adjustment Settlement",
            },
            "469": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Miscellaneous ACH Debit",
            },
            "470": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Check Paid",
            },
            "471": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Check Paid – Cumulative MTD",
            },
            "472": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Cumulative** Checks Paid",
            },
            "474": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Certified Check Debit",
            },
            "475": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Check Paid",
            },
            "476": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Federal Reserve Bank Letter Debit",
            },
            "477": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Bank Originated Debit",
            },
            "478": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "List Post Debits",
            },
            "479": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "List Post Debit",
            },
            "480": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Loan Payments",
            },
            "481": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Loan Payment",
            },
            "482": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Bank-Originated Debits",
            },
            "484": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Draft",
            },
            "485": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "DTC Debit",
            },
            "486": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Cash Letter Debits",
            },
            "487": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Cash Letter Debit",
            },
            "489": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Cash Letter Adjustment",
            },
            "490": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Outgoing Money Transfers",
            },
            "491": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Outgoing Internal Money Transfer",
            },
            "493": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Customer Terminal Initiated Money Transfer",
            },
            "495": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Outgoing Money Transfer",
            },
            "496": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Money Transfer Adjustment",
            },
            "498": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Compensation",
            },
            "500": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Automatic Transfer Debits",
            },
            "501": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Automatic Transfer Debit",
            },
            "502": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Bond Operations Debit",
            },
            "505": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Book Transfer Debits",
            },
            "506": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Book Transfer Debit",
            },
            "507": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total International Money Transfer Debits",
            },
            "508": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual International Money Transfer Debits",
            },
            "510": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total International Debits",
            },
            "512": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Letter of Credit Debit",
            },
            "513": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Letter of Credit",
            },
            "514": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Foreign Exchange Debit",
            },
            "515": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Letters of Credit",
            },
            "516": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Foreign Remittance Debit",
            },
            "518": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Foreign Collection Debit",
            },
            "522": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Foreign Checks Paid",
            },
            "524": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Commission",
            },
            "526": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "International Money Market Trading",
            },
            "527": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Standing Order",
            },
            "529": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Miscellaneous International Debit",
            },
            "530": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Security Debits",
            },
            "531": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Securities Purchased",
            },
            "532": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Amount of Securities Purchased",
            },
            "533": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Security Collection Debit",
            },
            "534": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Miscellaneous Securities DB – FF",
            },
            "535": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Purchase of Equity Securities",
            },
            "536": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Miscellaneous Securities Debit – CHF",
            },
            "537": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Collection Debit",
            },
            "538": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Matured Repurchase Order",
            },
            "539": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Bankers’ Acceptances Debit",
            },
            "540": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Coupon Collection Debit",
            },
            "541": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Bankers’ Acceptances",
            },
            "542": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Purchase of Debt Securities",
            },
            "543": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Domestic Collection",
            },
            "544": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Interest/Matured Principal Payment",
            },
            "546": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Commercial paper",
            },
            "547": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Capital Change",
            },
            "548": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Savings Bonds Sales Adjustment",
            },
            "549": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Miscellaneous Security Debit",
            },
            "550": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Deposited Items Returned",
            },
            "551": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Credit Reversals",
            },
            "552": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Credit Reversal",
            },
            "554": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Posting Error Correction Debit",
            },
            "555": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Deposited Item Returned",
            },
            "556": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total ACH Return Items",
            },
            "557": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual ACH Return Item",
            },
            "558": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ACH Reversal Debit",
            },
            "560": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Rejected Debits",
            },
            "561": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Rejected Debit",
            },
            "563": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Overdraft",
            },
            "564": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Overdraft Fee",
            },
            "566": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Return Item",
            },
            "567": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Return Item Fee",
            },
            "568": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Return Item Adjustment",
            },
            "570": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total ZBA Debits",
            },
            "574": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Cumulative ZBA Debits",
            },
            "575": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ZBA Debit",
            },
            "577": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ZBA Debit Transfer",
            },
            "578": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ZBA Debit Adjustment",
            },
            "580": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Controlled Disbursing Debits",
            },
            "581": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Controlled Disbursing Debit",
            },
            "583": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Disbursing Checks Paid – Early Amount",
            },
            "584": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Disbursing Checks Paid – Later Amount",
            },
            "585": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Disbursing Funding Requirement",
            },
            "586": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "FRB Presentment Estimate (Fed Estimate)",
            },
            "587": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Late Debits (After Notification)",
            },
            "588": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Disbursing Checks Paid-Last Amount",
            },
            "590": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total DTC Debits",
            },
            "594": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total ATM Debits",
            },
            "595": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ATM Debit",
            },
            "596": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total APR Debits",
            },
            "597": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "ARP Debit",
            },
            "601": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Estimated Total Disbursement",
            },
            "602": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Adjusted Total Disbursement",
            },
            "610": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Funds Required",
            },
            "611": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Wire Transfers Out- CHF",
            },
            "612": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Wire Transfers Out – FF",
            },
            "613": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total International Debit – CHF",
            },
            "614": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total International Debit – FF",
            },
            "615": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Federal Reserve Bank – Commercial Bank Debit",
            },
            "616": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Federal Reserve Bank – Commercial Bank Debit",
            },
            "617": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Securities Purchased – CHF",
            },
            "618": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Securities Purchased – FF",
            },
            "621": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Broker Debits – CHF",
            },
            "622": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Broker Debit",
            },
            "623": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Broker Debits – FF",
            },
            "625": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Broker Debits",
            },
            "626": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Fed Funds Purchased",
            },
            "627": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Fed Funds Purchased",
            },
            "628": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Cash Center Debits",
            },
            "629": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Cash Center Debit",
            },
            "630": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Debit Adjustments",
            },
            "631": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Debit Adjustment",
            },
            "632": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Trust Debits",
            },
            "633": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Trust Debit",
            },
            "634": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "YTD Adjustment Debit",
            },
            "640": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Escrow Debits",
            },
            "641": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Escrow Debit",
            },
            "644": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Back Value Debit",
            },
            "646": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Transfer Calculation Debit",
            },
            "650": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Investments Purchased",
            },
            "651": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Individual Investment purchased",
            },
            "654": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Interest Debit",
            },
            "655": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Investment Interest Debits",
            },
            "656": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Sweep Principal Buy",
            },
            "657": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Futures Debit",
            },
            "658": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Principal Payments Debit",
            },
            "659": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Interest Adjustment Debit",
            },
            "661": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Account Analysis Fee",
            },
            "662": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Correspondent Collection Debit",
            },
            "663": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Correspondent Collection Adjustment",
            },
            "664": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Loan Participation",
            },
            "665": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Intercept Debits",
            },
            "666": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Currency and Coin Shipped",
            },
            "667": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Food Stamp Letter",
            },
            "668": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Food Stamp Adjustment",
            },
            "669": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Clearing Settlement Debit",
            },
            "670": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Back Value Debits",
            },
            "672": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Back Value Adjustment",
            },
            "673": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Customer Payroll",
            },
            "674": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Statement Recap",
            },
            "676": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Savings Bond Letter or Adjustment",
            },
            "677": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Treasury Tax and Loan Debit",
            },
            "678": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Transfer of Treasury Debit",
            },
            "679": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Government Checks Cash Letter Debit",
            },
            "681": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Government Check Adjustment",
            },
            "682": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Postal Money Order Debit",
            },
            "683": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Postal Money Order Adjustment",
            },
            "684": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Cash Letter Auto Charge Debit",
            },
            "685": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Universal Debits",
            },
            "686": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Cash Letter Auto Charge Adjustment",
            },
            "687": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Fine-Sort Cash Letter Debit",
            },
            "688": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "FRB Fine-Sort Adjustment",
            },
            "689": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "FRB Freight Payment Debits",
            },
            "690": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Miscellaneous Debits",
            },
            "691": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Universal Debit",
            },
            "692": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Freight Payment Debit",
            },
            "693": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Itemized Debit Over $10,000",
            },
            "694": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Deposit Reversal",
            },
            "695": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Deposit Correction Debit",
            },
            "696": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Regular Collection Debit",
            },
            "697": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Cumulative** Debits",
            },
            "698": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Miscellaneous Fees",
            },
            "699": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Miscellaneous Debit",
            },
            "701": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Principal Loan Balance",
            },
            "703": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Available Commitment Amount",
            },
            "705": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Payment Amount Due",
            },
            "707": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Principal Amount Past Due",
            },
            "709": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.status,
                "description": "Interest Amount Past Due",
            },
            "720": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Total Loan Payment",
            },
            "721": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Amount Applied to Interest",
            },
            "722": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Amount Applied to Principal",
            },
            "723": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Amount Applied to Escrow",
            },
            "724": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Amount Applied to Late Charges",
            },
            "725": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Amount Applied to Buydown",
            },
            "726": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Amount Applied to Misc. Fees",
            },
            "727": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Amount Applied to Deferred Interest Detail",
            },
            "728": {
                "transaction_type": TransactionType.credit,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Amount Applied to Service Charge",
            },
            "760": {
                "transaction_type": TransactionType.debit,
                "type_level_code": TypeCodeLevel.summary,
                "description": "Loan Disbursement",
            },
            "890": {
                "transaction_type": None,
                "type_level_code": TypeCodeLevel.detail,
                "description": "Contains Non-monetary Information",
            },
        }
