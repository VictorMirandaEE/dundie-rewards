# Dundie Tool Usage

The Dundie tool is a command-line interface (CLI) application designed to manage and distribute rewards within your organization. This guide will help you understand how to use the Dundie tool effectively.

## Start SMTP development server

Run in a separate terminal:

```bash
python3 -m aiosmtpd -n
```

Then, export the `EMAIL` and `PASSWORD` of the administrator user. For example:

```bash
export EMPLOYEE_EMAIL="schrute@dundermifflin.com"
export EMPLOYEE_PASSWORD="9bsSYGVl"
```

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
                                                                                                                                                          
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version    Show the version and exit.                                                                                                                │
│ --help       Show this message and exit.                                                                                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ load    Load employees data from a CSV file to the database and display them.                                                                          │
│ show    Show employees data.                                                                                                                           │
│ update  Update the balance of reward points.                                                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
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
                                                                                                                                                          
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  FILEPATH    (PATH) [required]                                                                                                                       │
│    --help      Show this message and exit.                                                                                                             │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Then, initialize the database to the latest version with:

```bash
alembic stamp head
```

Examples:

```bash
❯ dundie load assets/employees.csv
                                          Dunder Mifflin Employees                                          
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
┃ Name           ┃ Email                     ┃ Role              ┃ Department         ┃ Currency ┃ Created ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
│ Jim Halpert    │ jim@dundermifflin.com     │ Salesman          │ Sales              │ USD      │ True    │
│ Dwight Schrute │ schrute@dundermifflin.com │ Sales Manager     │ Sales              │ EUR      │ True    │
│ Gabe Lewis     │ gabe@dundermifflin.com    │ Director          │ Board of Directors │ BRL      │ True    │
│ Michael Scott  │ mike@dd.com               │ Regional Manager  │ Management         │ BRL      │ True    │
│ Pam Beesly     │ pam@dd.com                │ Receptionist      │ Administration     │ EUR      │ True    │
│ Creed Bratton  │ creed@dd.com              │ Quality Assurance │ Quality Assurance  │ EUR      │ True    │
└────────────────┴───────────────────────────┴───────────────────┴────────────────────┴──────────┴─────────┘

❯ alembic stamp head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running stamp_revision  -> 29e650e071c8
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
                                                                                                                                                          
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --email         Filter by employee email                                                                                                               │
│                 (TEXT)                                                                                                                                 │
│ --department    Filter by department                                                                                                                   │
│                 (TEXT)                                                                                                                                 │
│ --file          Output to file                                                                                                                         │
│                 (FILENAME)                                                                                                                             │
│ --format        Output format (txt or json)                                                                                                            │
│                 (txt|json)                                                                                                                             │
│ --help          Show this message and exit.                                                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Examples:

````bash
# Show All Employees

❯ dundie show
                                                      Dunder Mifflin Rewards Report                                                       
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Name           ┃ Email                     ┃ Role              ┃ Department         ┃ Balance ┃ Currency ┃ Total  ┃ Last Transaction    ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ Jim Halpert    │ jim@dundermifflin.com     │ Salesman          │ Sales              │ 500.00  │ USD      │ 500.00 │ 2025-06-09 09:33:20 │
│ Dwight Schrute │ schrute@dundermifflin.com │ Sales Manager     │ Sales              │ 100.00  │ EUR      │ 0.00   │ 2025-06-09 09:33:20 │
│ Gabe Lewis     │ gabe@dundermifflin.com    │ Director          │ Board of Directors │ 100.00  │ BRL      │ 0.00   │ 2025-06-09 09:33:20 │
│ Michael Scott  │ mike@dd.com               │ Regional Manager  │ Management         │ 100.00  │ BRL      │ 0.00   │ 2025-06-09 09:33:20 │
│ Pam Beesly     │ pam@dd.com                │ Receptionist      │ Administration     │ 500.00  │ EUR      │ 0.00   │ 2025-06-09 09:33:20 │
│ Creed Bratton  │ creed@dd.com              │ Quality Assurance │ Quality Assurance  │ 500.00  │ EUR      │ 0.00   │ 2025-06-09 09:33:20 │
└────────────────┴───────────────────────────┴───────────────────┴────────────────────┴─────────┴──────────┴────────┴─────────────────────┘

# Filter by email

❯ dundie show --email="jim@dundermifflin.com"
                                           Dunder Mifflin Rewards Report                                           
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Name        ┃ Email                 ┃ Role     ┃ Department ┃ Balance ┃ Currency ┃ Total  ┃ Last Transaction    ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ Jim Halpert │ jim@dundermifflin.com │ Salesman │ Sales      │ 500.00  │ USD      │ 500.00 │ 2025-06-09 09:33:20 │
└─────────────┴───────────────────────┴──────────┴────────────┴─────────┴──────────┴────────┴─────────────────────┘

# Filter by department

❯ dundie show --department="Sales"
                                                 Dunder Mifflin Rewards Report                                                 
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Name           ┃ Email                     ┃ Role          ┃ Department ┃ Balance ┃ Currency ┃ Total  ┃ Last Transaction    ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ Jim Halpert    │ jim@dundermifflin.com     │ Salesman      │ Sales      │ 500.00  │ USD      │ 500.00 │ 2025-06-09 09:33:20 │
│ Dwight Schrute │ schrute@dundermifflin.com │ Sales Manager │ Sales      │ 100.00  │ EUR      │ 0.00   │ 2025-06-09 09:33:20 │
└────────────────┴───────────────────────────┴───────────────┴────────────┴─────────┴──────────┴────────┴─────────────────────┘

# Output in JSON format

❯ dundie show --format=json
[
    {
        "name": "Jim Halpert",
        "email": "jim@dundermifflin.com",
        "role": "Salesman",
        "department": "Sales",
        "balance": "500.00",
        "currency": "USD",
        "total": "500.00",
        "last_transaction": "2025-06-09 09:33:20"
    },
    {
        "name": "Dwight Schrute",
        "email": "schrute@dundermifflin.com",
        "role": "Sales Manager",
        "department": "Sales",
        "balance": "100.00",
        "currency": "EUR",
        "total": "0.00",
        "last_transaction": "2025-06-09 09:33:20"
    },
    {
        "name": "Gabe Lewis",
        "email": "gabe@dundermifflin.com",
        "role": "Director",
        "department": "Board of Directors",
        "balance": "100.00",
        "currency": "BRL",
        "total": "0.00",
        "last_transaction": "2025-06-09 09:33:20"
    },
    {
        "name": "Michael Scott",
        "email": "mike@dd.com",
        "role": "Regional Manager",
        "department": "Management",
        "balance": "100.00",
        "currency": "BRL",
        "total": "0.00",
        "last_transaction": "2025-06-09 09:33:20"
    },
    {
        "name": "Pam Beesly",
        "email": "pam@dd.com",
        "role": "Receptionist",
        "department": "Administration",
        "balance": "500.00",
        "currency": "EUR",
        "total": "0.00",
        "last_transaction": "2025-06-09 09:33:20"
    },
    {
        "name": "Creed Bratton",
        "email": "creed@dd.com",
        "role": "Quality Assurance",
        "department": "Quality Assurance",
        "balance": "500.00",
        "currency": "EUR",
        "total": "0.00",
        "last_transaction": "2025-06-09 09:33:20"
    }
]
# Output in TXT format to a file

❯ dundie show --format=txt --file=employees.txt
❯ cat employees.txt
───────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: employees.txt
───────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │                                                        Dunder Mifflin Rewards Report                                                       
   2   │ ┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
   3   │ ┃ Name           ┃ Email                     ┃ Role              ┃ Department         ┃ Balance ┃ Currency ┃ Total  ┃ Last Transaction    ┃
   4   │ ┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
   5   │ │ Jim Halpert    │ jim@dundermifflin.com     │ Salesman          │ Sales              │ 500.00  │ USD      │ 500.00 │ 2025-06-09 09:33:20 │
   6   │ │ Dwight Schrute │ schrute@dundermifflin.com │ Sales Manager     │ Sales              │ 100.00  │ EUR      │ 0.00   │ 2025-06-09 09:33:20 │
   7   │ │ Gabe Lewis     │ gabe@dundermifflin.com    │ Director          │ Board of Directors │ 100.00  │ BRL      │ 0.00   │ 2025-06-09 09:33:20 │
   8   │ │ Michael Scott  │ mike@dd.com               │ Regional Manager  │ Management         │ 100.00  │ BRL      │ 0.00   │ 2025-06-09 09:33:20 │
   9   │ │ Pam Beesly     │ pam@dd.com                │ Receptionist      │ Administration     │ 500.00  │ EUR      │ 0.00   │ 2025-06-09 09:33:20 │
  10   │ │ Creed Bratton  │ creed@dd.com              │ Quality Assurance │ Quality Assurance  │ 500.00  │ EUR      │ 0.00   │ 2025-06-09 09:33:20 │
  11   │ └────────────────┴───────────────────────────┴───────────────────┴────────────────────┴─────────┴──────────┴────────┴─────────────────────┘
───────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

# Output in JSON format to a file

❯ dundie show --format=json --file=employees.json
❯ cat employees.json
───────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: employees.json
───────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ [
   2   │     {
   3   │         "name": "Jim Halpert",
   4   │         "email": "jim@dundermifflin.com",
   5   │         "role": "Salesman",
   6   │         "department": "Sales",
   7   │         "balance": "500.00",
   8   │         "currency": "USD",
   9   │         "total": "500.00",
  10   │         "last_transaction": "2025-06-09 09:33:20"
  11   │     },
  12   │     {
  13   │         "name": "Dwight Schrute",
  14   │         "email": "schrute@dundermifflin.com",
  15   │         "role": "Sales Manager",
  16   │         "department": "Sales",
  17   │         "balance": "100.00",
  18   │         "currency": "EUR",
  19   │         "total": "0.00",
  20   │         "last_transaction": "2025-06-09 09:33:20"
  21   │     },
  22   │     {
  23   │         "name": "Gabe Lewis",
  24   │         "email": "gabe@dundermifflin.com",
  25   │         "role": "Director",
  26   │         "department": "Board of Directors",
  27   │         "balance": "100.00",
  28   │         "currency": "BRL",
  29   │         "total": "0.00",
  30   │         "last_transaction": "2025-06-09 09:33:20"
  31   │     },
  32   │     {
  33   │         "name": "Michael Scott",
  34   │         "email": "mike@dd.com",
  35   │         "role": "Regional Manager",
  36   │         "department": "Management",
  37   │         "balance": "100.00",
  38   │         "currency": "BRL",
  39   │         "total": "0.00",
  40   │         "last_transaction": "2025-06-09 09:33:20"
  41   │     },
  42   │     {
  43   │         "name": "Pam Beesly",
  44   │         "email": "pam@dd.com",
  45   │         "role": "Receptionist",
  46   │         "department": "Administration",
  47   │         "balance": "500.00",
  48   │         "currency": "EUR",
  49   │         "total": "0.00",
  50   │         "last_transaction": "2025-06-09 09:33:20"
  51   │     },
  52   │     {
  53   │         "name": "Creed Bratton",
  54   │         "email": "creed@dd.com",
  55   │         "role": "Quality Assurance",
  56   │         "department": "Quality Assurance",
  57   │         "balance": "500.00",
  58   │         "currency": "EUR",
  59   │         "total": "0.00",
  60   │         "last_transaction": "2025-06-09 09:33:20"
  61   │     }
  62   │ ]
───────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
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
                                                                                                                                                                         
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  VALUE           (FLOAT) [required]                                                                                                                                 │
│    --email         Filter by employee email                                                                                                                           │
│                    (TEXT)                                                                                                                                             │
│    --department    Filter by department                                                                                                                               │
│                    (TEXT)                                                                                                                                             │
│    --help          Show this message and exit.                                                                                                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Examples:

```bash

# Add 10 points to all employees

❯ dundie update 10
                                                       Dunder Mifflin Rewards Report                                                       
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Name           ┃ Email                     ┃ Role              ┃ Department         ┃ Balance ┃ Currency ┃ Total  ┃ Last Transaction    ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ Jim Halpert    │ jim@dundermifflin.com     │ Salesman          │ Sales              │ 510.00  │ USD      │ 510.00 │ 2025-06-09 09:41:52 │
│ Dwight Schrute │ schrute@dundermifflin.com │ Sales Manager     │ Sales              │ 100.00  │ EUR      │ 0.00   │ 2025-06-09 09:39:36 │
│ Gabe Lewis     │ gabe@dundermifflin.com    │ Director          │ Board of Directors │ 110.00  │ BRL      │ 0.00   │ 2025-06-09 09:41:52 │
│ Michael Scott  │ mike@dd.com               │ Regional Manager  │ Management         │ 110.00  │ BRL      │ 0.00   │ 2025-06-09 09:41:52 │
│ Pam Beesly     │ pam@dd.com                │ Receptionist      │ Administration     │ 510.00  │ EUR      │ 0.00   │ 2025-06-09 09:41:52 │
│ Creed Bratton  │ creed@dd.com              │ Quality Assurance │ Quality Assurance  │ 510.00  │ EUR      │ 0.00   │ 2025-06-09 09:41:52 │
└────────────────┴───────────────────────────┴───────────────────┴────────────────────┴─────────┴──────────┴────────┴─────────────────────┘

# Subtract 10 points from all employees

❯ dundie update -- -10
                                                       Dunder Mifflin Rewards Report                                                       
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Name           ┃ Email                     ┃ Role              ┃ Department         ┃ Balance ┃ Currency ┃ Total  ┃ Last Transaction    ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ Jim Halpert    │ jim@dundermifflin.com     │ Salesman          │ Sales              │ 500.00  │ USD      │ 500.00 │ 2025-06-09 09:42:20 │
│ Dwight Schrute │ schrute@dundermifflin.com │ Sales Manager     │ Sales              │ 100.00  │ EUR      │ 0.00   │ 2025-06-09 09:39:36 │
│ Gabe Lewis     │ gabe@dundermifflin.com    │ Director          │ Board of Directors │ 100.00  │ BRL      │ 0.00   │ 2025-06-09 09:42:20 │
│ Michael Scott  │ mike@dd.com               │ Regional Manager  │ Management         │ 100.00  │ BRL      │ 0.00   │ 2025-06-09 09:42:20 │
│ Pam Beesly     │ pam@dd.com                │ Receptionist      │ Administration     │ 500.00  │ EUR      │ 0.00   │ 2025-06-09 09:42:20 │
│ Creed Bratton  │ creed@dd.com              │ Quality Assurance │ Quality Assurance  │ 500.00  │ EUR      │ 0.00   │ 2025-06-09 09:42:20 │
└────────────────┴───────────────────────────┴───────────────────┴────────────────────┴─────────┴──────────┴────────┴─────────────────────┘

# Add 10 points, filter by email

❯ dundie update --email="jim@dundermifflin.com" 10
                                           Dunder Mifflin Rewards Report                                           
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Name        ┃ Email                 ┃ Role     ┃ Department ┃ Balance ┃ Currency ┃ Total  ┃ Last Transaction    ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ Jim Halpert │ jim@dundermifflin.com │ Salesman │ Sales      │ 510.00  │ USD      │ 510.00 │ 2025-06-09 09:42:38 │
└─────────────┴───────────────────────┴──────────┴────────────┴─────────┴──────────┴────────┴─────────────────────┘

# Subtract 10 points; filter by email

❯ dundie update --email="gabe@dundermifflin.com" -- -10
                                              Dunder Mifflin Rewards Report                                               
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Name       ┃ Email                  ┃ Role     ┃ Department         ┃ Balance ┃ Currency ┃ Total ┃ Last Transaction    ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ Gabe Lewis │ gabe@dundermifflin.com │ Director │ Board of Directors │ 90.00   │ BRL      │ 0.00  │ 2025-06-09 09:42:52 │
└────────────┴────────────────────────┴──────────┴────────────────────┴─────────┴──────────┴───────┴─────────────────────┘

# Add 10 points, filter by department

❯ dundie update --department="Sales" 10
                                                 Dunder Mifflin Rewards Report                                                 
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Name           ┃ Email                     ┃ Role          ┃ Department ┃ Balance ┃ Currency ┃ Total  ┃ Last Transaction    ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ Jim Halpert    │ jim@dundermifflin.com     │ Salesman      │ Sales      │ 520.00  │ USD      │ 520.00 │ 2025-06-09 09:43:12 │
│ Dwight Schrute │ schrute@dundermifflin.com │ Sales Manager │ Sales      │ 100.00  │ EUR      │ 0.00   │ 2025-06-09 09:39:36 │
└────────────────┴───────────────────────────┴───────────────┴────────────┴─────────┴──────────┴────────┴─────────────────────┘

# Subtract 10 points, filter by department

❯ dundie update --department="Board of Directors" -- -10
                                              Dunder Mifflin Rewards Report                                               
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Name       ┃ Email                  ┃ Role     ┃ Department         ┃ Balance ┃ Currency ┃ Total ┃ Last Transaction    ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ Gabe Lewis │ gabe@dundermifflin.com │ Director │ Board of Directors │ 80.00   │ BRL      │ 0.00  │ 2025-06-09 09:43:25 │
└────────────┴────────────────────────┴──────────┴────────────────────┴─────────┴──────────┴───────┴─────────────────────┘
```
