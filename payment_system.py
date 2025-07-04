# My first Python project!
# This program calculates payments for construction workers


import random
import json
from datetime import datetime



class PaymentSystem:
    def __init__(self):
        # These lists will store my data
        self.workers = []
        self.payment_slips = []
        
    def generate_workers(self, num_workers=450):
        # This function creates fake workers for testing
        # I need at least 400 workers
        try:
            if num_workers < 400:
                print("Error: Need at least 400 workers!")
                raise ValueError("I need at least 400 workers to make this work!")
                
            # I made lists of names to use for fake workers
          
            first_names = [
                "Adebayo", "Aisha", "Chinedu", "Fatima", "Emeka", "Ngozi", "Olumide", "Kemi",
                "Tunde", "Amina", "Chioma", "Ibrahim", "Folake", "Usman", "Adunni",
                "Segun", "Zainab", "Ikechukwu", "Hauwa", "Biodun", "Chiamaka", "Musa",
                "Funmi", "Chukwuma", "Halima", "Babatunde", "Blessing", "Aliyu", "Omotola",
                "Kelechi", "Salamatu", "Obinna", "Ronke", "Yakubu", "Chidinma", "Suleiman", "Bukola",
                "Chidi", "Rashida", "Femi", "Hadiza", "Nnamdi", "Folashade", "Ahmad", "Temitope",
                "Ifeanyi", "Mariam", "Kunle", "Safiya", "Chukwuemeka", "Yetunde", "Abdullahi", "Omolara",
                "Uchenna", "Zara", "Gbenga", "Asmau", "Chineye", "Bashir", "Titilayo", "Garba",
                "Michael", "Grace", "David", "Mary", "John", "Elizabeth", "Peter", "Sarah",
                "James", "Joy", "Daniel", "Faith", "Samuel", "Peace", "Joseph", "Mercy",
                "Emmanuel", "Hope", "Benjamin", "Patience", "Paul", "Comfort", "Stephen", "Precious",
                "Matthew", "Gift", "Andrew", "Favour", "Philip", "Goodness", "Anthony", "Charity"
            ]
            
            # Last names list
            last_names = [
                "Adebayo", "Okafor", "Ibrahim", "Okonkwo", "Musa", "Eze", "Bello", "Okoro",
                "Aliyu", "Nwankwo", "Yusuf", "Okoye", "Garba", "Onyeka", "Suleiman",
                "Chukwu", "Abdullahi", "Okeke", "Usman", "Nwosu", "Yakubu", "Okafor", "Balogun",
                "Nnaji", "Shehu", "Ogunyemi", "Lawal", "Emeka", "Adamu", "Oladele",
                "Nnamdi", "Haruna", "Ogbonna", "Salisu", "Adeyemi", "Chukwuma", "Ismail", "Ogundimu",
                "Onyeama", "Mamman", "Olaniyan", "Danjuma", "Okafor", "Tanko", "Adebisi", "Nwachukwu",
                "Abubakar", "Okonkwo", "Sadiq", "Ogundipe", "Umar", "Chukwuemeka", "Baba", "Oladipo",
                "Nwokolo", "Tijani", "Ogunleye", "Kabir", "Adeyinka", "Chinedu", "Sani"
            ]
            
            # Simple lists for gender and departments
            genders = ["Male", "Female"]
            departments = [
                "Construction", "Engineering", "Safety", "Administration", "Maintenance",
                "Quality Control", "Project Management", "Human Resources", "Finance",
                "Equipment Operations", "Site Supervision", "Logistics"
            ]
            
            # Clear the workers list first
            self.workers = []
            
            # Use a for loop to create workers (I learned this in class!)
            for i in range(num_workers):
                # Create a dictionary for each worker
                worker = {
                    "worker_id": "HC" + str(i+1).zfill(4),  # Makes HC0001, HC0002, etc.
                    "first_name": random.choice(first_names),
                    "last_name": random.choice(last_names),
                    "gender": random.choice(genders),
                    "department": random.choice(departments),
                    "salary": round(random.uniform(5000, 35000), 2),  # Random salary
                    "hours_worked": random.randint(35, 50),  # Hours per week
                    "overtime_hours": random.randint(0, 15),  # Extra hours
                    "employee_level": "Not assigned yet"
                }
                
                # Add this worker to our list
                self.workers.append(worker)
                
            print(f"I created {len(self.workers)} workers!")
            return self.workers
            
        except Exception as e:
            print(f"Something went wrong when making workers: {e}")
            return None
    
    def assign_employee_level(self, worker):
        # This function decides what level each worker is
        # Fixed the logic to handle overlapping conditions properly
        try:
            salary = worker["salary"]
            gender = worker["gender"]
            
            # Rule 2: If salary is between 7,500 and 30,000 AND they are female, they get A5-F level
            # Check this first since it's more specific
            if 7500 <= salary <= 30000 and gender == "Female":
                return "A5-F"
            
            # Rule 1: If salary is between 10,000 and 20,000, they get A1 level
            elif 10000 <= salary <= 20000:
                return "A1"
            
            # Everyone else gets Standard level
            else:
                return "Standard"
                
        except Exception as e:
            print(f"Error: Could not assign level to worker - {e}")
            return "Error"
    
    def calculate_payment(self, worker):
        # This function calculates how much money each worker gets
        # Fixed to use actual hours worked instead of assuming 40 hours
        try:
            base_salary = worker["salary"]
            hours_worked = worker["hours_worked"]
            overtime_hours = worker["overtime_hours"]
            
            # Calculate hourly rate from annual salary (assuming 52 weeks)
            hourly_rate = base_salary / (52 * 40)  # 40 hours is standard full-time
            
            # Calculate base pay for actual hours worked (up to 40 hours)
            regular_hours = min(hours_worked, 40)
            weekly_base = regular_hours * hourly_rate
            
            # Any hours over 40 are overtime (in addition to the overtime_hours field)
            extra_regular_overtime = max(0, hours_worked - 40)
            total_overtime = overtime_hours + extra_regular_overtime
            
            # Calculate overtime pay (they get 1.5 times normal rate)
            overtime_pay = total_overtime * hourly_rate * 1.5
            
            # Add base pay and overtime together
            total_payment = weekly_base + overtime_pay
            
            # Take out 20% for taxes (I don't like taxes but they're required)
            deductions = total_payment * 0.20
            net_payment = total_payment - deductions
            
            # Return all the calculations in a dictionary
            payment_info = {
                "weekly_base": round(weekly_base, 2),
                "overtime_pay": round(overtime_pay, 2),
                "total_gross": round(total_payment, 2),
                "deductions": round(deductions, 2),
                "net_payment": round(net_payment, 2)
            }
            
            return payment_info
            
        except Exception as e:
            print(f"Error: Could not calculate payment - {e}")
            # Return zeros if something goes wrong
            return {
                "weekly_base": 0,
                "overtime_pay": 0,
                "total_gross": 0,
                "deductions": 0,
                "net_payment": 0
            }
    
    def generate_payment_slips(self):
        # This function makes payment slips for all workers
        # I need to use a for loop to go through each worker
        try:
            if len(self.workers) == 0:
                print("Error: No workers found! Make workers first.")
                return None
            
            self.payment_slips = []
            today = datetime.now().strftime("%Y-%m-%d")  # Get today's date
            
            print("Making payment slips...")
            
            # Use for loop to go through each worker (this is required!)
            for worker in self.workers:
                try:
                    # First, figure out what level this worker is
                    level = self.assign_employee_level(worker)
                    worker["employee_level"] = level
                    
                    # Then calculate their payment
                    payment_info = self.calculate_payment(worker)
                    
                    # Create a payment slip (this is like a receipt)
                    slip = {
                        "slip_id": "PS" + worker["worker_id"] + datetime.now().strftime("%Y%m%d"),
                        "date_generated": today,
                        "worker_info": {
                            "worker_id": worker["worker_id"],
                            "name": worker["first_name"] + " " + worker["last_name"],
                            "gender": worker["gender"],
                            "department": worker["department"],
                            "employee_level": level
                        },
                        "work_details": {
                            "annual_salary": worker["salary"],
                            "hours_worked": worker["hours_worked"],
                            "overtime_hours": worker["overtime_hours"]
                        },
                        "payment_details": payment_info
                    }
                    
                    # Add this slip to our list
                    self.payment_slips.append(slip)
                    
                except Exception as e:
                    print(f"Error: Could not process worker {worker.get('worker_id', 'unknown')}: {e}")
                    continue  # Skip this worker and try the next one
            
            print(f"I made {len(self.payment_slips)} payment slips!")
            return self.payment_slips
            
        except Exception as e:
            print(f"Error: Something went wrong making payment slips: {e}")
            return None
    
    def save_payment_slips(self, filename="payment_slips.json"):
        # This function saves all the payment slips to a file
        # JSON files are good for storing data
        try:
            if len(self.payment_slips) == 0:
                print("Error: No payment slips to save! Make payment slips first.")
                return
            
            # Use context manager to properly handle file operations
            with open(filename, 'w') as file:
                json.dump(self.payment_slips, file, indent=2)
            
            print(f"Payment slips saved to {filename}")
            
        except Exception as e:
            print(f"Error: Could not save payment slips to file - {e}")
    
    def print_summary_report(self):
        # This function prints a nice summary of everything
        # I want to show how many workers and how much money
        try:
            if len(self.payment_slips) == 0:
                print("No payment slips to summarize.")
                return
            
            print("\n" + "="*60)
            print("HIGHRIDGE CONSTRUCTION COMPANY - PAYMENT SUMMARY REPORT")
            print("="*60)
            print(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Total Workers Processed: {len(self.payment_slips)}")
            
            # Count how many workers are in each level
            level_counts = {}
            total_gross = 0
            total_net = 0
            
            # Go through each payment slip and count things
            for slip in self.payment_slips:
                level = slip["worker_info"]["employee_level"]
                level_counts[level] = level_counts.get(level, 0) + 1
                
                # Add up all the money
                total_gross += slip["payment_details"]["total_gross"]
                total_net += slip["payment_details"]["net_payment"]
            
            print("\nEmployee Level Distribution:")
            for level in sorted(level_counts.keys()):
                count = level_counts[level]
                percentage = (count / len(self.payment_slips)) * 100
                print(f"  {level}: {count} workers ({percentage:.1f}%)")
            
            print(f"\nTotal Gross Payments: ${total_gross:,.2f}")
            print(f"Total Net Payments: ${total_net:,.2f}")
            print(f"Total Deductions: ${(total_gross - total_net):,.2f}")
            print("="*60)
            
        except Exception as e:
            print(f"Error: Could not make summary report: {e}")

# This is the main function that runs everything
def main():
    try:
        print("Highridge Construction Company - Weekly Payment System")
        print("Starting payment processing...\n")
        
        # Create a new payment system object
        payment_system = PaymentSystem()
        
        # Make 450 workers (more than the required 400)
        workers = payment_system.generate_workers(300)
        if workers is None:
            print("Failed to generate workers. Exiting.")
            return
        
        # Make payment slips for all workers
        payment_slips = payment_system.generate_payment_slips()
        if payment_slips is None:
            print("Failed to generate payment slips. Exiting.")
            return
        
        # Save everything to a file
        payment_system.save_payment_slips("highridge_payment_slips.json")
        
        # Show a nice summary
        payment_system.print_summary_report()
        
        print("\nPayment processing completed successfully!")
        
    except Exception as e:
        print(f"Something went really wrong: {e}")
        print("Maybe ask the teacher for help.")

# This runs the main function when I run the program
if __name__ == "__main__":
    main()