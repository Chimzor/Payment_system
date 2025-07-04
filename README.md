# Highridge Construction Company - Payment System

## What is this?

This is a simple program that helps calculate weekly payments for construction workers. It can handle lots of workers at once and automatically figures out their pay based on their salary and hours worked.

## What does it do?

- Creates fake worker data (names, salaries, departments)
- Calculates how much each worker should be paid
- Saves all the payment information to a file
- Shows a summary of all payments

## How workers are classified

The program puts workers into different groups:

1. **A1 Level**: Workers earning between $10,000 and $20,000 per year
2. **A5-F Level**: Female workers earning between $7,500 and $30,000 per year
3. **Standard Level**: Everyone else

## Files in this project

- `payment_system.py` - The main Python program
- `payment_system.R` - The same program written in R language
- `README.md` - This help file
- `requirements.txt` - List of things Python needs to run the program
- `highridge_payment_slips.json` - The output file with all payment data

## How to run the Python version

### What you need first
- Python installed on your computer
- A terminal or command prompt

### Steps to run
1. Open your terminal
2. Go to the folder with these files
3. Type: `python3 payment_system.py`
4. Press Enter and wait for it to finish

### If you get errors
Try installing the required packages first:
```
pip install -r requirements.txt
```

## How to run the R version

### What you need first
- R installed on your computer

### Steps to run
1. Open your terminal
2. Go to the folder with these files
3. Type: `Rscript payment_system.R`
4. Press Enter and wait for it to finish

### If you get errors
You might need to install some R packages first. Open R and type:
```r
install.packages(c("jsonlite", "dplyr"))
```

## What happens when you run it

1. The program creates 450 fake workers
2. It calculates their weekly pay
3. It saves everything to a JSON file
4. It shows you a summary on screen

## Example of what you'll see

```
Highridge Construction Company - Weekly Payment System
Starting payment processing...

Successfully generated 450 workers
Generating payment slips...
Successfully generated 450 payment slips
Payment slips saved to highridge_payment_slips.json

============================================================
HIGHRIDGE CONSTRUCTION COMPANY - PAYMENT SUMMARY REPORT
============================================================
Total Workers Processed: 450

Employee Level Distribution:
  A1: 89 workers (19.8%)
  A5-F: 156 workers (34.7%)
  Standard: 205 workers (45.6%)

Total Gross Payments: $156,789.45
Total Net Payments: $125,431.56
Total Deductions: $31,357.89
============================================================

Payment processing completed successfully!
```

## Understanding the output file

The program creates a file called `highridge_payment_slips.json` that contains all the payment information. Each worker has:

- Their basic info (name, department, etc.)
- How much they worked
- How much they get paid
- How much is taken out for taxes

## Common problems and solutions

**"Command not found"**
- Make sure Python or R is installed
- Try `python` instead of `python3`

**"Permission denied"**
- Make sure you can write files in this folder
- Try running as administrator

**"Module not found"**
- Install the required packages using pip or R
