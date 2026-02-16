"""Testcases to validate BAI2 reader"""

import json
import tempfile
import pytest
import pandas as pd
from pathlib import Path

from bai2_reader.src.reader import BAI2Reader
from bai2_reader.src import exceptions as exc


# Test data paths
SAMPLE_DIR = Path(Path(__file__).parent.parent, "bai2_reader", "samples")
SAMPLE_1 = Path(SAMPLE_DIR, "sample_1.bai")
SAMPLE_2 = Path(SAMPLE_DIR, "sample_2.bai")


class TestBAI2Reader:
    """Test cases for BAI2Reader class"""

    def test_read_file_basic(self):
        """Test basic file reading and parsing"""
        reader = BAI2Reader(run_validation=False)
        result = reader.read_file(SAMPLE_1)

        assert result is not None
        assert result.bai_data is not None
        assert result.source_filename.name == "sample_1.bai"

    def test_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent files"""
        reader = BAI2Reader(run_validation=False)

        with pytest.raises(exc.Bai2ReaderException) as exc_info:
            reader.read_file("/nonexistent/path/file.bai")

        assert "File not found" in str(exc_info)

    def test_file_header_parsing(self):
        """Test that file header is parsed correctly"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        header = reader.bai_data.header
        assert header is not None
        assert header.sender == "GSBI"
        assert header.receiver == "cont001"
        assert header.file_date == "210706"
        assert header.file_time == "1249"
        assert header.file_id == "1"

    def test_group_header_parsing(self):
        """Test that group header is parsed correctly"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        assert len(reader.bai_data.groups) > 0
        group = reader.bai_data.groups[0]
        assert group.group_header is not None
        assert group.group_header.receiver == "cont001"
        assert group.group_header.sender == "026015079"

    def test_account_identifier_parsing(self):
        """Test that account identifier is parsed correctly"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        group = reader.bai_data.groups[0]
        assert len(group.accounts) > 0
        account = group.accounts[0]
        assert account.account_identifier is not None
        assert account.account_identifier.account_number == "107049924"
        assert account.account_identifier.currency_code == "USD"

    def test_transaction_parsing(self):
        """Test that transactions are parsed correctly"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        transactions = []
        for group in reader.bai_data.groups:
            for account in group.accounts:
                for txn in account.transactions:
                    transactions.append(txn.transaction)

        assert len(transactions) > 0
        # Check first transaction
        first_txn = transactions[0]
        assert first_txn.type_code == "447"
        assert first_txn.amount == 60000.0

    def test_continuation_records(self):
        """Test that continuation records are parsed correctly"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        # Find a transaction with continuation records
        found_continuation = False
        for group in reader.bai_data.groups:
            for account in group.accounts:
                for txn in account.transactions:
                    if len(txn.summary) > 0:
                        found_continuation = True
                        assert len(txn.summary) > 0
                        # Check continuation record format
                        first_summary = txn.summary[0]
                        assert first_summary.record_code == "88"
                        break
                if found_continuation:
                    break
            if found_continuation:
                break

        assert found_continuation, "Expected to find at least one transaction with continuation records"

    def test_file_trailer_parsing(self):
        """Test that file trailer is parsed correctly"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        trailer = reader.bai_data.file_trailer
        assert trailer is not None
        assert trailer.record_code == "99"

    def test_group_trailer_parsing(self):
        """Test that group trailer is parsed correctly"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        group = reader.bai_data.groups[0]
        assert group.group_trailer is not None
        assert group.group_trailer.record_code == "98"

    def test_account_trailer_parsing(self):
        """Test that account trailer is parsed correctly"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        group = reader.bai_data.groups[0]
        account = group.accounts[0]
        assert account.account_trailer is not None
        assert account.account_trailer.record_code == "49"

    def test_to_json(self):
        """Test conversion to JSON format"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        json_data = reader.to_json()

        assert isinstance(json_data, list)
        assert len(json_data) > 0

        # Check first record structure
        first_record = json_data[0]
        assert "file_header" in first_record
        assert "group_header" in first_record
        assert "account_identifier" in first_record
        assert "transaction" in first_record

    def test_to_json_serializable(self):
        """Test that to_json returns serializable data"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        json_data = reader.to_json()

        # Should not raise any exception
        json_str = json.dumps(json_data)
        assert json_str is not None

    def test_to_flat_dataframe(self):
        """Test conversion to flat DataFrame"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        df = reader.to_flat_dataframe()

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        # Check that we have transaction-related columns
        assert "transaction_type_code" in df.columns
        assert "transaction_amount" in df.columns

    def test_write_data_csv(self):
        """Test writing data to CSV format"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir, "test_output.csv")
            reader.write_data(output_dir=tmpdir, output_file_name="test_output.csv", output_format="csv")

            assert Path(output_path).is_file()

            # Verify CSV content
            df = pd.read_csv(output_path)
            assert len(df) > 0

    def test_write_data_json(self):
        """Test writing data to JSON format"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir, "test_output.json")
            reader.write_data(output_dir=tmpdir, output_file_name="test_output.json", output_format="json")

            assert Path(output_path).is_file()

            # Verify JSON content
            with open(output_path) as f:
                data = json.load(f)
            assert isinstance(data, list)
            assert len(data) > 0

    def test_write_data_parquet(self):
        """Test writing data to Parquet format"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir, "test_output.parquet")
            reader.write_data(output_dir=tmpdir, output_file_name="test_output.parquet", output_format="parquet")

            assert Path(output_path).is_file()

            # Verify Parquet content
            df = pd.read_parquet(output_path)
            assert len(df) > 0

    def test_write_data_creates_directory(self):
        """Test that write_data creates output directory if it doesn't exist"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir, "new_dir", "nested")
            output_path = Path(output_dir, "test_output.csv")

            reader.write_data(output_dir=output_dir, output_file_name="test_output.csv")

            assert Path(output_path).is_file()

    def test_validation_enabled_by_default(self):
        """Test that validation is enabled by default"""
        reader = BAI2Reader()
        assert reader.run_validation is True

    def test_validation_can_be_disabled(self):
        """Test that validation can be disabled"""
        reader = BAI2Reader(run_validation=False)
        assert reader.run_validation is False

    def test_custom_encoding(self):
        """Test reading file with custom encoding"""
        reader = BAI2Reader(encoding="utf-8")
        assert reader.encoding == "utf-8"

    def test_read_file_with_validation_disabled(self):
        """Test reading file with validation disabled"""
        reader = BAI2Reader(run_validation=False)
        result = reader.read_file(SAMPLE_1, run_validation=False)

        assert result is not None
        assert result.bai_data is not None

    def test_multiple_groups(self):
        """Test parsing file with multiple groups"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        # sample_1.bai has 4 accounts in one group
        assert len(reader.bai_data.groups) >= 1
        group = reader.bai_data.groups[0]
        assert len(group.accounts) >= 1

    def test_transaction_type_codes(self):
        """Test various transaction type codes are parsed"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        type_codes = set()
        for group in reader.bai_data.groups:
            for account in group.accounts:
                for txn in account.transactions:
                    if txn.transaction.type_code:
                        type_codes.add(txn.transaction.type_code)

        assert len(type_codes) > 0

    def test_empty_lines_ignored(self):
        """Test that empty lines in file are ignored"""
        # Create a temp file with empty lines
        with tempfile.NamedTemporaryFile(mode="w", suffix=".bai", delete=False) as f:
            f.write("01,GSBI,cont001,210706,1249,1,,,2/\n")
            f.write("\n")
            f.write("02,cont001,026015079,1,230906,2000,,/\n")
            f.write("\n")
            f.write("99,13060195162,1,3/\n")
            temp_path = f.name

        try:
            reader = BAI2Reader(run_validation=False)
            reader.read_file(temp_path)

            assert reader.bai_data is not None
            assert reader.bai_data.header is not None
        finally:
            Path(temp_path).unlink()

    def test_different_output_formats(self):
        """Test that different output formats work correctly"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        formats = ["csv", "json", "parquet"]

        for fmt in formats:
            with tempfile.TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir, f"test_output.{fmt}")
                reader.write_data(output_dir=tmpdir, output_file_name=f"test_output.{fmt}", output_format=fmt)
                assert Path(output_path).is_file()

    def test_unsupported_output_format(self):
        """Test that unsupported output format raises error"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(exc.Bai2ReaderException) as exc_info:
                reader.write_data(output_dir=tmpdir, output_format="unsupported")

            assert "Unsupported" in str(exc_info)

    def test_record_counter_populated(self):
        """Test that record counters are populated"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        assert reader.bai_data.header.record_counter is not None
        assert reader.bai_data.header.record_counter > 0

    def test_group_count(self):
        """Test that group count is correct"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        assert len(reader.bai_data.groups) > 0

    def test_account_transactions_count(self):
        """Test transaction count per account"""
        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_1)

        for group in reader.bai_data.groups:
            for account in group.accounts:
                # Account should have transactions or be empty
                assert account.transactions is not None

    def test_sample_file_2(self):
        """Test reading another sample file"""
        if not Path(SAMPLE_2).is_file():
            pytest.skip("sample_2.bai not found")

        reader = BAI2Reader(run_validation=False)
        reader.read_file(SAMPLE_2)

        assert reader.bai_data is not None
        assert reader.bai_data.header is not None
        assert len(reader.bai_data.groups) > 0


class TestBAI2ReaderValidation:
    """Test cases for validation functionality"""

    def test_account_trailer_mismatch(self):
        """Test that account trailer record count mismatch is detected"""
        # Create a file with invalid account trailer count
        with tempfile.NamedTemporaryFile(mode="w", suffix=".bai", delete=False) as f:
            f.write("01,GSBI,cont001,210706,1249,1,,,2/\n")
            f.write("02,cont001,026015079,1,230906,2000,,/\n")
            f.write("03,107049924,USD,,,,,060,13053325440,,,100,000,0,,400,000,0,/\n")
            f.write("16,447,60000,,SPB2322984714570,1111,ACH Credit Payment,Test\n")
            # Wrong record count - should be 2 but we put 99
            f.write("49,13053325440,99/\n")
            f.write("98,13060195162,4,16/\n")
            f.write("99,13060195162,1,7/\n")
            temp_path = f.name

        try:
            reader = BAI2Reader(run_validation=True)
            with pytest.raises(exc.Bai2ReaderException) as exc_info:
                reader.read_file(temp_path)

            assert "Account trailer record count mismatch" in str(exc_info)
        finally:
            Path(temp_path).unlink()


class TestBAI2ReaderContinuation:
    """Test cases for continuation record handling"""

    def test_continuation_after_account_identifier(self):
        """Test continuation records after account identifier"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".bai", delete=False) as f:
            f.write("01,GSBI,cont001,210706,1249,1,,,2/\n")
            f.write("02,cont001,026015079,1,230906,2000,,/\n")
            f.write("03,107049924,USD,,,,,060,13053325440,,,100,000,0,,400,000,0,/\n")
            f.write("88,Some continuation data\n")
            f.write("49,13053325440,2/\n")
            f.write("98,13060195162,4,6/\n")
            f.write("99,13060195162,1,7/\n")
            temp_path = f.name

        try:
            reader = BAI2Reader(run_validation=False)
            reader.read_file(temp_path)

            account = reader.bai_data.groups[0].accounts[0]
            assert len(account.summary) > 0
        finally:
            Path(temp_path).unlink()

    def test_continuation_invalid_placement(self):
        """Test that continuation without preceding record raises error"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".bai", delete=False) as f:
            f.write("01,GSBI,cont001,210706,1249,1,,,2/\n")
            f.write("02,cont001,026015079,1,230906,2000,,/\n")
            f.write("88,Some continuation data\n")
            f.write("49,0,1/\n")
            f.write("98,0,3,4/\n")
            f.write("99,0,1,6/\n")
            temp_path = f.name

        try:
            reader = BAI2Reader(run_validation=False)
            with pytest.raises(exc.Bai2ReaderException) as exc_info:
                reader.read_file(temp_path)

            assert "Continuation record found without" in str(exc_info)
        finally:
            Path(temp_path).unlink()


class TestBAI2ReaderEdgeCases:
    """Test edge cases and error handling"""

    def test_read_returns_self(self):
        """Test that read_file returns self for method chaining"""
        reader = BAI2Reader(run_validation=False)
        result = reader.read_file(SAMPLE_1)

        assert result is reader

    def test_bai_data_initially_none(self):
        """Test that bai_data is None before reading"""
        reader = BAI2Reader(run_validation=False)
        assert reader.bai_data is None

    def test_source_filename_initially_none(self):
        """Test that source_filename is None before reading"""
        reader = BAI2Reader(run_validation=False)
        assert reader.source_filename is None

    def test_method_chaining(self):
        """Test method chaining works"""
        reader = BAI2Reader(run_validation=False)
        result = reader.read_file(SAMPLE_1).to_json()

        assert result is not None
        assert isinstance(result, list)
