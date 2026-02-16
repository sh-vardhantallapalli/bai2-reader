"""Pydantic Models defining how the BAI file should look like"""

from pydantic import BaseModel, Field
from typing import List, Optional

from bai2_reader.src import enums


class Record(BaseModel):
    """Every line in the BAI2 file will have a record code, and we will also store the record counter"""

    record_code: str = Field(
        ...,
        description="The record code for this line",
        exclude=True,  # will not be part of exports/ model dumps
    )
    record_counter: int = Field(
        ...,
        description="The record counter for this line, this is internally calculated, not seen in BAI2 file",
        exclude=True,  # will not be part of exports/ model dumps
    )


class FileHeader(Record):
    """The header record TransactionType.debit, which will be the first line of the file, record code: '01'"""

    sender: str = Field(..., description="The sender ID")
    receiver: str = Field(..., description="The receiver ID")
    file_date: str = Field(..., description="The file date")
    file_time: str = Field(..., description="The file time")
    file_id: str = Field(..., description="The file ID")
    record_length: Optional[str] = Field(None, description="The record length, which is optional")
    block_size: Optional[str] = Field(None, description="The block size, which is optional")
    version_number: Optional[str] = Field(None, description="The version number, which is optional")


class FileTrailer(Record):
    """The file trailer record TransactionType.debit, which will be the last line of the file, record code: '99'"""

    file_control_total: Optional[float] = Field(None, description="The file control total, which is optional")
    num_of_groups: Optional[int] = Field(None, description="The number of groups for this file, which is optional")
    num_of_records: Optional[int] = Field(None, description="The number of records for this file, which is optional")


class GroupHeader(Record):
    """The group header record TransactionType.debit, which will be the first line of each group, record code: '02'"""

    receiver: str = Field(..., description="The receiver ID")
    sender: str = Field(..., description="The sender ID")
    group_status: enums.GroupStatus | None = Field(..., description="The group status code")
    as_of_date: str = Field(..., description="The as of date")
    as_of_time: str = Field(..., description="The as of time")
    currency_code: str = Field(..., description="The currency code")
    as_of_date_modifier: enums.AsOfDateModifier | None = Field(
        None, description="The as of date modifier, which is optional"
    )


class GroupTrailer(Record):
    """The group trailer record TransactionType.debit, which will be the last line of each group, record code: '98'"""

    group_control_total: Optional[float] = Field(None, description="The group control total, which is optional")
    num_of_accounts: Optional[int] = Field(None, description="The number of accounts for this group, which is optional")
    num_of_records: Optional[int] = Field(None, description="The number of records for this group, which is optional")


class AccountIdentifier(Record):
    """The account identifier record, which will be the first line of each account, record code: '03'"""

    account_number: str = Field(..., description="The account number")
    currency_code: Optional[str] = Field(None, description="The currency code, which is optional")
    type_code: Optional[str] = Field(None, description="The type code, which is optional")
    opening_balance: Optional[float] = Field(None, description="The opening balance, which is optional")
    item_count: Optional[int] = Field(None, description="The item count, which is optional")
    fund_type: Optional[str] = Field(None, description="The fund type, which is optional")
    rest_of_record: Optional[str] = Field(
        None,
        description="The rest of the record, which is optional, "
        "this is for the case when there are more fields than expected, "
        "we will store the rest of the record in this field for future use",
    )


class Continuation(Record):
    """The continuation record, which will be the line of each continuation, record code: '88'"""

    record: str = Field(
        ...,
        description="The continuation record, which will be used when the record is too long "
        "and needs to be continued in the next line",
    )


class Transaction(Record):
    """The transaction record which will be the line of each transaction. '16' record code"""

    type_code: str = Field(..., description="The type code for this transaction")
    amount: float = Field(..., description="The amount for this transaction")
    funds_type: Optional[str] = Field(None, description="The funds type for this transaction, which is optional")
    bank_reference_number: Optional[str] = Field(
        None, description="The bank reference number for this transaction, which is optional"
    )
    customer_reference_number: Optional[str] = Field(
        None, description="The customer reference number for this transaction, which is optional"
    )
    description: Optional[str] = Field(None, description="The text for this transaction, which is optional")
    transaction_type: enums.TransactionType = Field(
        None, description="The transaction type for this transaction, which is optional"
    )
    rest_of_record: Optional[str] = Field(
        None,
        description="The rest of the record, which is optional, "
        "this is for the case when there are more fields than expected, "
        "we will store the rest of the record in this field for future use",
    )


class AccountTrailer(Record):
    """The account trailer record which will be the last line of each account, record code: '49'"""

    account_control_total: Optional[float] = Field(None, description="The account control total, which is optional")
    num_of_records: Optional[int] = Field(None, description="The number of records for this account, which is optional")


class TransactionSection(BaseModel):
    """The transaction section for each transaction, which will contain
    - the transaction detail record
    - and the continuation records that follow the transaction detail
    """

    transaction: Transaction = Field(..., description="The transaction detail, record code: '16' ")
    summary: List[Continuation] = Field(
        default_factory=list,
        description="The summary of this transaction, "
        "which is the continuation records that follow the transaction detail record",
    )


class AccountSection(BaseModel):
    """Account section for each account, which will contain
    - the account identifier record,
    - account summary
    - the transaction sections,
    - and the account trailer record
    """

    account_identifier: AccountIdentifier | None = Field(
        None, description="The account identifier record, record code: '03' "
    )
    summary: List[Continuation] = Field(
        default_factory=list,
        description="The summary of this account, "
        "which is the continuation records that follow the account identifier record."
        " all '88' after '03' ",
    )
    transactions: List[TransactionSection] = Field(
        default_factory=list,
        description="The transactions for this account, "
        "which is the list of transaction sections that follow the account identifier record",
    )
    account_trailer: AccountTrailer = Field(
        None, description="The account trailer record for this account, record code: '49' "
    )


class GroupSection(BaseModel):
    """The group section for each group, which will contain
    - the group header record,
    - the account sections,
    - and the group trailer record
    """

    group_header: GroupHeader | None = Field(None, description="The group header record, record code: '02' ")
    accounts: List[AccountSection] = Field(
        default_factory=list,
        description="The accounts for this group,"
        " which is the list of account sections that follow the group header record",
    )
    group_trailer: GroupTrailer = Field(None, description="The group trailer record for this group, record code: '98' ")


class Bai2Model(BaseModel):
    """The model for the BAI2 file, which will be the output of the parser"""

    header: FileHeader | None = Field(None, description="The header record for this file, record code: '01' ")
    groups: List[GroupSection] = Field(
        default_factory=list,
        description="The groups for this file, which is the list of group sections that follow the header record",
    )
    file_trailer: FileTrailer = Field(None, description="The file trailer record for this file, record code: '99' ")
