# Dundie Tool Usage

The Dundie tool is a command-line interface (CLI) application designed to manage and distribute rewards within your organization. This guide will help you understand how to use the Dundie tool effectively.

## Help

Refer to the help option for more detailed information on the commands available.

```bash
❯ dundie --help

 Usage: dundie [OPTIONS] COMMAND [ARGS]...

 Dunder Mifflin Rewards System.
 This is a CLI tool for managing the Dunder Mifflin Rewards program.

            Features

  • Admins can load employees data to the database and assign points.
  • Users can view their rewards points and transfer them to other employees.

╭─ Options ─────────────────────────────────────────────────────────────────────╮
│ --version    Show the version and exit.                                       │
│ --help       Show this message and exit.                                      │
╰───────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────╮
│ load    Load employees data from a CSV file to the database and display them. │
│ show    Show employees data.                                                  │
│ update  Update the balance of reward points.                                  │
╰───────────────────────────────────────────────────────────────────────────────╯
```

## Commands

### Load Command

To load employees data from a CSV file to the database and display them, use the `load` command:

```bash
❯ dundie load --help

 Usage: dundie load [OPTIONS] FILEPATH

 Load employees data from a CSV file to the database and display them.
 FILEPATH is the path to the CSV file.

            Features

  • Validates the data.
  • Parses the data.
  • Displays the data.

╭─ Options ──────────────────────────────────╮
│ *  FILEPATH    (PATH) [required]           │
│    --help      Show this message and exit. │
╰────────────────────────────────────────────╯
```

Examples:

```bash
❯ dundie load assets/employees.csv
                                  Dunder Mifflin Employees
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Name           ┃ Department         ┃ Role          ┃ e-mail                    ┃ Created ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ Jim Halpert    │ Sales              │ Salesman      │ jim@dundermifflin.com     │ True    │
│ Dwight Schrute │ Sales              │ Sales Manager │ schrute@dundermifflin.com │ True    │
│ Gabe Lewis     │ Board of Directors │ Director      │ gabe@dundermifflin.com    │ True    │
└────────────────┴────────────────────┴───────────────┴───────────────────────────┴─────────┘
```

### Show Command

To list all employees in the system, use the `show` command.

```bash
❯  dundie show --help

 Usage: dundie show [OPTIONS]

 Show employees data.

            Features

  • Filter by email or department.
  • Output to console or file.
  • Output format as TXT or JSON.

╭─ Options ───────────────────────────────────╮
│ --email         Filter by employee email    │
│                 (TEXT)                      │
│ --department    Filter by department        │
│                 (TEXT)                      │
│ --file          Output to file              │
│                 (FILENAME)                  │
│ --format        Output format (txt or json) │
│                 (txt|json)                  │
│ --help          Show this message and exit. │
╰─────────────────────────────────────────────╯
```

Examples:

````bash
# Show All Employees

❯ dundie show
                                              Dunder Mifflin Rewards Report
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Email                     ┃ Balance ┃ Last_Transaction           ┃ Name           ┃ Department         ┃ Role          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ jim@dundermifflin.com     │ 500     │ 2025-02-09T14:34:03.927883 │ Jim Halpert    │ Sales              │ Salesman      │
│ schrute@dundermifflin.com │ 100     │ 2025-02-09T14:34:03.932154 │ Dwight Schrute │ Sales              │ Sales Manager │
│ gabe@dundermifflin.com    │ 100     │ 2025-02-09T14:34:03.932649 │ Gabe Lewis     │ Board of Directors │ Director      │
└───────────────────────────┴─────────┴────────────────────────────┴────────────────┴────────────────────┴───────────────┘

# Filter by email

❯ dundie show --email="jim@dundermifflin.com"
                                    Dunder Mifflin Rewards Report
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Email                 ┃ Balance ┃ Last_Transaction           ┃ Name        ┃ Department ┃ Role     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│ jim@dundermifflin.com │ 500     │ 2025-02-09T14:34:03.927883 │ Jim Halpert │ Sales      │ Salesman │
└───────────────────────┴─────────┴────────────────────────────┴─────────────┴────────────┴──────────┘

# Filter by department

❯ dundie show --department="Sales"
                                          Dunder Mifflin Rewards Report
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Email                     ┃ Balance ┃ Last_Transaction           ┃ Name           ┃ Department ┃ Role          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ jim@dundermifflin.com     │ 500     │ 2025-02-09T14:34:03.927883 │ Jim Halpert    │ Sales      │ Salesman      │
│ schrute@dundermifflin.com │ 100     │ 2025-02-09T14:34:03.932154 │ Dwight Schrute │ Sales      │ Sales Manager │
└───────────────────────────┴─────────┴────────────────────────────┴────────────────┴────────────┴───────────────┘

# Output in JSON format

❯ dundie show --format=json
[
    {
        "email": "jim@dundermifflin.com",
        "balance": 500,
        "last_transaction": "2025-02-09T14:34:03.927883",
        "name": "Jim Halpert",
        "department": "Sales",
        "role": "Salesman"
    },
    {
        "email": "schrute@dundermifflin.com",
        "balance": 100,
        "last_transaction": "2025-02-09T14:34:03.932154",
        "name": "Dwight Schrute",
        "department": "Sales",
        "role": "Sales Manager"
    },
    {
        "email": "gabe@dundermifflin.com",
        "balance": 100,
        "last_transaction": "2025-02-09T14:34:03.932649",
        "name": "Gabe Lewis",
        "department": "Board of Directors",
        "role": "Director"
    }
]

# Output in TXT format to a file

❯ dundie show --format=txt --file=employees.txt
❯ cat employees.txt
───────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: employees.txt
───────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │                                               Dunder Mifflin Rewards Report
   2   │ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
   3   │ ┃ Email                     ┃ Balance ┃ Last_Transaction           ┃ Name           ┃ Department         ┃ Role          ┃
   4   │ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
   5   │ │ jim@dundermifflin.com     │ 500     │ 2025-02-09T14:34:03.927883 │ Jim Halpert    │ Sales              │ Salesman      │
   6   │ │ schrute@dundermifflin.com │ 100     │ 2025-02-09T14:34:03.932154 │ Dwight Schrute │ Sales              │ Sales Manager │
   7   │ │ gabe@dundermifflin.com    │ 100     │ 2025-02-09T14:34:03.932649 │ Gabe Lewis     │ Board of Directors │ Director      │
   8   │ └───────────────────────────┴─────────┴────────────────────────────┴────────────────┴────────────────────┴───────────────┘
───────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

# Output in JSON format to a file

❯ dundie show --format=json --file=employees.json
❯ cat employees.json
───────┬──────────────────────────────────────────────────────────
       │ File: employees.json
───────┼──────────────────────────────────────────────────────────
   1   │ [
   2   │     {
   3   │         "email": "jim@dundermifflin.com",
   4   │         "balance": 500,
   5   │         "last_transaction": "2025-02-09T14:34:03.927883",
   6   │         "name": "Jim Halpert",
   7   │         "department": "Sales",
   8   │         "role": "Salesman"
   9   │     },
  10   │     {
  11   │         "email": "schrute@dundermifflin.com",
  12   │         "balance": 100,
  13   │         "last_transaction": "2025-02-09T14:34:03.932154",
  14   │         "name": "Dwight Schrute",
  15   │         "department": "Sales",
  16   │         "role": "Sales Manager"
  17   │     },
  18   │     {
  19   │         "email": "gabe@dundermifflin.com",
  20   │         "balance": 100,
  21   │         "last_transaction": "2025-02-09T14:34:03.932649",
  22   │         "name": "Gabe Lewis",
  23   │         "department": "Board of Directors",
  24   │         "role": "Director"
  25   │     }
  26   │ ]
───────┴──────────────────────────────────────────────────────────

````

### Update Command

To add and subtract points to an employee, use the `update` command.

```bash
❯ dundie update --help

 Usage: dundie update [OPTIONS] VALUE

 Update the balance of reward points.
 VALUE is the number of points to add.

 Prefix a negative VALUE with '-- ' to subtract points.

            Features

  • Filter by email or department.

╭─ Options ──────────────────────────────────────╮
│ *  VALUE           (INTEGER) [required]        │
│    --email         Filter by employee email    │
│                    (TEXT)                      │
│    --department    Filter by department        │
│                    (TEXT)                      │
│    --help          Show this message and exit. │
╰────────────────────────────────────────────────╯
```

Examples:

```bash

# Add 10 points to all employees

❯ dundie update 10
                                              Dunder Mifflin Rewards Report
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Email                     ┃ Balance ┃ Last_Transaction           ┃ Name           ┃ Department         ┃ Role          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ jim@dundermifflin.com     │ 510     │ 2025-02-09T14:51:29.758408 │ Jim Halpert    │ Sales              │ Salesman      │
│ schrute@dundermifflin.com │ 110     │ 2025-02-09T14:51:29.758416 │ Dwight Schrute │ Sales              │ Sales Manager │
│ gabe@dundermifflin.com    │ 110     │ 2025-02-09T14:51:29.758418 │ Gabe Lewis     │ Board of Directors │ Director      │
└───────────────────────────┴─────────┴────────────────────────────┴────────────────┴────────────────────┴───────────────┘

# Subtract 10 points from all employees

❯ dundie update -- -10
                                              Dunder Mifflin Rewards Report
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Email                     ┃ Balance ┃ Last_Transaction           ┃ Name           ┃ Department         ┃ Role          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ jim@dundermifflin.com     │ 490     │ 2025-02-09T14:52:14.234875 │ Jim Halpert    │ Sales              │ Salesman      │
│ schrute@dundermifflin.com │ 90      │ 2025-02-09T14:52:14.234884 │ Dwight Schrute │ Sales              │ Sales Manager │
│ gabe@dundermifflin.com    │ 90      │ 2025-02-09T14:52:14.234886 │ Gabe Lewis     │ Board of Directors │ Director      │
└───────────────────────────┴─────────┴────────────────────────────┴────────────────┴────────────────────┴───────────────┘

# Add 10 points, filter by email

❯ dundie update --email="jim@dundermifflin.com" 10
                                    Dunder Mifflin Rewards Report
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Email                 ┃ Balance ┃ Last_Transaction           ┃ Name        ┃ Department ┃ Role     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│ jim@dundermifflin.com │ 510     │ 2025-02-09T14:53:10.648823 │ Jim Halpert │ Sales      │ Salesman │
└───────────────────────┴─────────┴────────────────────────────┴─────────────┴────────────┴──────────┘

# Subtract 10 points; filter by email

❯ dundie update --email="gabe@dundermifflin.com" -- -10
                                        Dunder Mifflin Rewards Report
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Email                  ┃ Balance ┃ Last_Transaction           ┃ Name       ┃ Department         ┃ Role     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ gabe@dundermifflin.com │ 90      │ 2025-02-09T14:54:17.850773 │ Gabe Lewis │ Board of Directors │ Director │
└────────────────────────┴─────────┴────────────────────────────┴────────────┴────────────────────┴──────────┘

# Add 10 points, filter by department

❯ dundie update --department="Sales" 10
                                          Dunder Mifflin Rewards Report
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Email                     ┃ Balance ┃ Last_Transaction           ┃ Name           ┃ Department ┃ Role          ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ jim@dundermifflin.com     │ 510     │ 2025-02-09T14:55:28.516834 │ Jim Halpert    │ Sales      │ Salesman      │
│ schrute@dundermifflin.com │ 110     │ 2025-02-09T14:55:28.516842 │ Dwight Schrute │ Sales      │ Sales Manager │
└───────────────────────────┴─────────┴────────────────────────────┴────────────────┴────────────┴───────────────┘

# Subtract 10 points, filter by department

❯ dundie update --department="Board of Directors" -- -10
                                        Dunder Mifflin Rewards Report
┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Email                  ┃ Balance ┃ Last_Transaction           ┃ Name       ┃ Department         ┃ Role     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ gabe@dundermifflin.com │ 90      │ 2025-02-09T14:57:26.524489 │ Gabe Lewis │ Board of Directors │ Director │
└────────────────────────┴─────────┴────────────────────────────┴────────────┴────────────────────┴──────────┘
```
