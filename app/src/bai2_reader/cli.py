"""BAI2 Reader CLI"""

import json
import typer

from src.bai2_reader import enums, exceptions as exc
from src.bai2_reader.logger import log
from src.bai2_reader.reader import BAI2Reader

app = typer.Typer(help="Utility to parse BAI2 files")


@app.command(help="Export BAI2 file to structured formats")
def export(
    input_files: str = typer.Option(
        ...,
        help="Input BAI2 file, if you have multiple files pass them as comma separated. ",
    ),
    run_validation: bool = typer.Option(True, help="Run Validations to perform the counts checks in trailers"),
    output_dir: str = typer.Option("output", help="Output path where the output files have to be stored"),
    output_file_names: str = typer.Option(
        None,
        help="""Custom output file name if you want, use comma separated if you are passing multiple input files
                 \n\nDefault : '{input_filesNAME_WITHOUT_EXTENSION}_{DATETIME_IN_UTC}.{OUTPUT_FORMAT}'""",
    ),
    output_format: enums.OutputFormat = typer.Option(enums.OutputFormat.CSV, help="Output forma"),
    encoding: str = typer.Option("utf-8", help="Input BAI2 file"),
    write_args: str = typer.Option(
        None,
        help="""Write args that will be passed to pandas to_csv/to_json/to_parquet functions
                    \n\nExample : '{"sep": ",", "compression": "gzip"}'
                    \n\nNote    : Make sure you wrap the strings in double quotes. :)
                    """,
    ),
):
    """Export BAI2 file to structured formats"""
    input_files = input_files.split(",")
    output_file_names = output_file_names.split(",") if output_file_names else []

    if len(input_files) > 1 and len(output_file_names) > 1 and len(input_files) != len(output_file_names):
        log.debug(f"input_files: {input_files} | output_file_names: {output_file_names}")
        raise exc.Bai2ReaderException(
            "Output filenames are passed but the count of output filenames doesnt match with input files passed"
        )

    if write_args:
        try:
            write_args = json.loads(write_args)
        except json.JSONDecodeError as e:
            raise exc.Bai2ReaderException(f"Failed to Parse the write_args: {write_args}.\n Exception: {e}")

        log.debug(f"write_args: {write_args}")
        exit()

    reader = BAI2Reader(
        write_to_files=True,
        run_validation=run_validation,
        output_dir=output_dir,
        output_format=output_format,
        encoding=encoding,
    )

    for cntr, input_file in enumerate(input_files):
        reader.read_file(file_path=input_file).write_data(
            output_file_name=output_file_names[cntr] if output_file_names else None, write_args=write_args
        )


@app.callback()
def main(debug: bool = typer.Option(False, help="Set this if you want to log the debug statements")):
    """Default callback that is called for all subcommands"""
    if debug:
        import logging

        log.setLevel(logging.DEBUG)
        log.handlers[0].setLevel(logging.DEBUG)
        log.debug("Debugging enabled!")
