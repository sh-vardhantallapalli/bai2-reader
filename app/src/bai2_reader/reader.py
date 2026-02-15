"""Core BAI reader script which read and parses the BAI files and converts to a pydantic model"""

import pandas as pd

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Self, List

from src.bai2_reader.logger import log
from src.bai2_reader import enums, exceptions as exc, models


class BAI2Reader:
    """Class to read and parse BAI2 files"""

    def __init__(
        self,
        run_validation: bool = True,
        write_to_files: bool = False,
        output_dir: str = "output",
        output_format: enums.OutputFormat = enums.OutputFormat.CSV,
        encoding: str = "utf-8",
        delimiter: str = ",",
    ):
        """Initializer"""
        self.encoding = encoding
        self.run_validation = run_validation
        self.write_to_files = write_to_files
        self.output_dir = output_dir
        self.output_format = output_format
        self.delimiter = delimiter

        self.source_filename: Path | None = None
        self.bai_data: models.Bai2Model | None = None

    def read_file(self, file_path: str, run_validation: bool | None = None, encoding: str | None = None) -> Self:
        """Reads a BAI2 file and returns a Bai2Model object containing the parsed data.
        If any of the parameters are not provided, it will use the default values set in the constructor.
        :param file_path: The path to the BAI2 file to be read.
        :param run_validation: Whether to run validation on the parsed data, defaults to True.
        :param encoding: The encoding of the BAI2 file, defaults to "utf-8".
        """
        if not Path(file_path).is_file():
            raise exc.Bai2ReaderException(f"File not found: {file_path}")
        self.source_filename = Path(file_path)

        log.info(f"Reading input file: {self.source_filename.name}")

        run_validation = self.run_validation if run_validation is None else run_validation
        encoding = self.encoding if encoding is None else encoding

        with open(self.source_filename, encoding=encoding) as file:
            lines = file.readlines()

        previous_rec_code = None
        account_record_counter = 0
        group_record_counter = 0
        total_records_counter = 0

        bai_data = models.Bai2Model()

        for line in lines:
            if not line.strip():
                continue

            total_records_counter += 1
            group_record_counter += 1

            record_code = enums.Record(line[:2])
            rest_of_record = line[3:].strip()

            log.debug(f"Reading line: {total_records_counter}, record_code: {record_code.name} ")

            # if EOL has '/' the remove it
            if rest_of_record and rest_of_record.endswith("/"):
                rest_of_record = rest_of_record[:-1]

            record = rest_of_record.split(self.delimiter)

            try:
                if record_code == enums.Record.file_header:
                    bai_data.header = models.FileHeader(
                        record_code=record_code,
                        sender=record[0],
                        receiver=record[1],
                        file_date=record[2],
                        file_time=record[3],
                        file_id=record[4],
                        record_length=record[5] if len(record) > 5 else None,
                        block_size=record[6] if len(record) > 6 else None,
                        version_number=record[7] if len(record) > 7 else None,
                        record_counter=total_records_counter,
                    )

                    group_record_counter = 0  # file header is not part of any group, so reset the group record counter

                elif record_code == enums.Record.group_header:
                    group = models.GroupSection()
                    bai_data.groups.append(group)
                    bai_data.groups[-1].group_header = models.GroupHeader(
                        record_code=record_code,
                        receiver=record[0],
                        sender=record[1],
                        group_status=enums.GroupStatus(record[2]) if len(record) > 2 and record[2] else None,
                        as_of_date=record[3],
                        as_of_time=record[4],
                        currency_code=record[5],
                        as_of_date_modifier=enums.AsOfDateModifier(record[6])
                        if len(record) > 6 and record[6]
                        else None,
                        record_counter=total_records_counter,
                    )

                elif record_code == enums.Record.account_identifier:
                    account_record_counter += 1
                    previous_rec_code = record_code

                    _rec = models.AccountIdentifier(
                        record_code=record_code,
                        account_number=record[0],
                        currency_code=record[1] if len(record) > 1 else None,
                        type_code=record[2] if len(record) > 2 else None,
                        opening_balance=float(record[3]) if len(record) > 3 and record[3] else None,
                        item_count=int(record[4]) if len(record) > 4 and record[4] else None,
                        fund_type=record[5] if len(record) > 5 else None,
                        rest_of_record=record[6] if len(record) > 6 else None,
                        record_counter=total_records_counter,
                    )

                    accounts_section = models.AccountSection(account_identifier=_rec)
                    bai_data.groups[-1].accounts.append(accounts_section)

                elif record_code == enums.Record.transaction:
                    account_record_counter += 1
                    previous_rec_code = record_code

                    _rec = models.Transaction(
                        record_code=record_code,
                        type_code=record[0] if len(record) > 0 else None,
                        amount=float(record[1]) if len(record) > 1 and record[1] else None,
                        fund_type=record[2] if len(record) > 2 else None,
                        reference_number=record[3] if len(record) > 3 else None,
                        text=record[4] if len(record) > 4 else None,
                        record_counter=total_records_counter,
                    )
                    transaction_section = models.TransactionSection(transaction=_rec)
                    bai_data.groups[-1].accounts[-1].transactions.append(transaction_section)

                elif record_code == enums.Record.account_trailer:
                    _rec = models.AccountTrailer(
                        record_code=record_code,
                        account_control_total=float(record[0]) if len(record) > 0 and record[0] else None,
                        num_of_records=int(record[1]) if len(record) > 1 and record[1] else None,
                        record_counter=total_records_counter,
                    )

                    if run_validation and account_record_counter != _rec.num_of_records:
                        raise exc.Bai2ReaderException(
                            "Account trailer record count mismatch:"
                            f" expected {account_record_counter}, got {_rec.num_of_records}"
                        )
                    bai_data.groups[-1].accounts[-1].account_trailer = _rec

                    account_record_counter = 0  # reset account record counter for the next account

                elif record_code == enums.Record.continuation:
                    account_record_counter += 1

                    _rec = models.Continuation(
                        record_code=record_code, record=rest_of_record, record_counter=account_record_counter
                    )

                    if previous_rec_code not in [enums.Record.account_identifier, enums.Record.transaction]:
                        raise exc.Bai2ReaderException(
                            "Continuation record found without a preceding account identifier or transaction record"
                        )

                    if previous_rec_code == enums.Record.account_identifier:
                        # append the continuation record to the summary of the last account identifier record
                        bai_data.groups[-1].accounts[-1].summary.append(_rec)
                    elif previous_rec_code == enums.Record.transaction:
                        # append the continuation record to the summary of the last transaction record
                        bai_data.groups[-1].accounts[-1].transactions[-1].summary.append(_rec)

                elif record_code == enums.Record.group_trailer:
                    _rec = models.GroupTrailer(
                        record_code=record_code,
                        group_control_total=float(record[0]) if len(record) > 0 and record[0] else None,
                        num_of_accounts=int(record[1]) if len(record) > 1 and record[1] else None,
                        num_of_records=int(record[2]) if len(record) > 2 and record[2] else None,
                        record_counter=total_records_counter,
                    )

                    if run_validation and group_record_counter != _rec.num_of_records:
                        raise exc.Bai2ReaderException(
                            f"Group trailer record count mismatch: "
                            f"expected {group_record_counter}, got {_rec.num_of_records}"
                        )

                    bai_data.groups[-1].group_trailer = _rec
                    group_record_counter = 0

                elif record_code == enums.Record.file_trailer:
                    _rec = models.FileTrailer(
                        record_code=record_code,
                        file_control_total=float(record[0]) if len(record) > 0 and record[0] else None,
                        num_of_groups=int(record[1]) if len(record) > 1 and record[1] else None,
                        num_of_records=int(record[2]) if len(record) > 2 and record[2] else None,
                        record_counter=total_records_counter,
                    )

                    if run_validation and total_records_counter != _rec.num_of_records:
                        raise exc.Bai2ReaderException(
                            f"File trailer record count mismatch: "
                            f"expected {total_records_counter}, got {_rec.num_of_records}"
                        )

                    bai_data.file_trailer = _rec

            except Exception as e:
                raise exc.Bai2ReaderException(f"Error parsing record: {line.strip()}\nError: {str(e)}")

        self.bai_data = bai_data
        return self

    def write_data(
        self,
        output_dir: str | None = None,
        output_file_name: str | None = None,
        output_format: enums.OutputFormat | str | None = None,
        write_args: Dict | None = None,
    ) -> None:
        """Write the BAI2 data to files
        :param write_args: Write args that will be passed to pandas to_csv or to_json functions, this is optional
        :param output_dir: The directory where the output files will be saved, defaults to "output".
        :param output_file_name: The Filename  will be saved, defaults to "bai2_output.<typeof export>".
        :param output_format: The format to write the output files in, defaults to CSV.
        :return:
        """
        output_dir = self.output_dir if output_dir is None else output_dir
        output_format = self.output_format if output_format is None else output_format
        if output_format is None:
            output_format = self.output_format

        if isinstance(output_format, str):
            try:
                output_format = enums.OutputFormat(output_format.lower())
            except ValueError:
                raise exc.Bai2ReaderException(f"Unsupported write format: {output_format}")

        flat_df = self.to_flat_dataframe()
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        if output_file_name:
            output_abs = Path(output_path, output_file_name)
        else:
            output_abs = Path(
                output_path, f"{self.source_filename.stem}_{datetime.now(tz=timezone.utc)}.{output_format.value}"
            )

        if output_format == enums.OutputFormat.CSV:
            if write_args is None:
                write_args = {"index": False}
            flat_df.to_csv(output_abs, **write_args)
        elif output_format == enums.OutputFormat.JSON:
            if write_args is None:
                write_args = {"orient": "records", "indent": 2, "index": False}
            flat_df.to_json(output_abs, **write_args)
        elif output_format == enums.OutputFormat.PARQUET:
            if write_args is None:
                write_args = {"index": False}
            flat_df.to_parquet(output_abs, **write_args)
        else:
            raise exc.Bai2ReaderException(f"Unsupported write format: {output_format}")

        log.info(f"Exported input file: {self.source_filename} to: {output_abs}")
        log.debug(f"Write args: {write_args}")

    def to_json(self) -> List:
        """BAI2 data into a list of dictionaries"""
        return bai_to_json(self.bai_data)

    def to_flat_dataframe(self) -> pd.DataFrame:
        """Flattens the nested structure of the BAI2 data into a list of dictionaries, where each dictionary represents
        a single transaction with all relevant information from the file, group, account, and transaction levels.
        :return: A list of dictionaries, where each dictionary represents a single transaction with all
        relevant information from the file, group, account, and transaction levels.
        """
        return bai_to_flat_dataframe(self.bai_data)


def bai_to_json(bai_data: models.Bai2Model) -> List[Dict]:
    """BAI2 data into a list of dictionaries
    :param bai_data: input data that is generated using Bai2Model
    :return: BAI data in JSON format
    """
    json_data = []

    for group in bai_data.groups:
        for account in group.accounts:
            for transaction in account.transactions:
                json_data.append(
                    {
                        "file_header": bai_data.header.model_dump(),
                        "group_header": group.group_header.model_dump(),
                        "account_identifier": account.account_identifier.model_dump(),
                        "account_summary": " ".join([summary.record for summary in account.summary]),
                        "transaction": transaction.transaction.model_dump(),
                        "transaction_summary": " ".join([summary.record for summary in transaction.summary]),
                        "account_trailer": account.account_trailer.model_dump() if account.account_trailer else {},
                        "group_trailer": group.group_trailer.model_dump() if group.group_trailer else {},
                        "file_trailer": bai_data.file_trailer.model_dump(),
                    }
                )
    return json_data


def bai_to_flat_dataframe(bai_data: models.Bai2Model) -> pd.DataFrame:
    """Flattens the nested structure of the BAI2 data into a list of dictionaries, where each dictionary represents
    a single transaction with all relevant information from the file, group, account, and transaction levels.
    :param bai_data: input data that is generated using Bai2Model
    :return: A list of dictionaries, where each dictionary represents a single transaction with all
    relevant information from the file, group, account, and transaction levels.
    """
    flat_data = bai_to_json(bai_data)
    df = pd.json_normalize(flat_data, sep="_")

    order = [
        "file_header",
        "group_header",
        "account_identifier",
        "account_summary",
        "transaction",
        "account_trailer",
        "group_trailer",
        "file_trailer",
    ]

    ordered_columns = []
    for prefix in order:
        for column in df.columns:
            if column.startswith(prefix):
                ordered_columns.append(column)

    return df[ordered_columns]
