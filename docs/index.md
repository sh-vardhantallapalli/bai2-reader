# BAI2 Reader

The BAI2 file format is a standardized, comma-delimited plain text (.txt) format developed by the Bank Administration Institute for electronic cash management, balance reporting, and bank reconciliation. It uses specific record types (01-99) to detail file headers, group headers, account summaries, and transaction details, often including multiple bank accounts in one file. 

## Structure: 
- Comma-separated, with a slash (/) to denote the end of a record line.
- Common Record Codes:
  - 01: File Header
  - 02: Group Header
  - 03: Account Identifier
  - 16: Transaction Detail
  - 49: Account Trailer
  - 98/99: Group/File Trailers
  - 88: Continuation 

Sample nested structure for a BAI2 file. 
- File can have multiple section of
  - Groups :  meaning multiple sections of 02 -> 98
  - Accounts with in each group : meaning multiple sections of 03 -> 49
  - Transactions with in each Account : meaning multiple sections of 16 followed by 88
- 88 is a continuation record that applies only to 03 Accounts and 16 Transactions, and we can have multiple 88 meaning multiple lines of summary
- Some banks don't send 49, 98 Trailer records so they are treated optional

```text
├──  01 File Header
│    ├──  02 GROUP header
│    │    ├──  03 Account Identifier 1
│    │    │    ├──  88 Account Summary/ continuation record
│    │    │    ├──  88 Account Summary/ continuation record
│    │    │    ├──  16 Transaction 1
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    │    ├──  16 Transaction 2
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    ├──  49 Account Trailer
│    │    ├──  03 Account Identifier 2
│    │    │    ├──  16 Transaction 1
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    ├──  49 Account Trailer
│    ├──  98 GROUP Trailer
│    ├──  02 GROUP header 2
│    │    ├──  03 Account Identifier 1 
│    │    │    ├──  88 Account Summary/ continuation record
│    │    │    ├──  16 Transaction 1
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    ├──  49 Account Trailer
│    │    ├──  03 Account Identifier 2
│    │    │    ├──  16 Transaction 1
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    │    │    ├──  88 Transaction Summary/ continuation record
│    │    ├──  49 Account Trailer
│    ├──  98 GROUP Trailer
├──  99 File Trailer
```

## Usage

### Export Options

### Python Based

### CLI

#### Installation
```shell
pip install bai2-reader --
```


### UI for Analysis
