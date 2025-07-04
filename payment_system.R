# My first R project for Highridge Construction Company
# This program makes payment slips for workers


# I need these libraries to work with data
library(jsonlite)  # for saving JSON files
library(dplyr)     # for working with data

# This is my main function that does everything
PaymentSystem <- function() {
  
  # These will store all my data
  workers <- list()        # all the workers go here
  payment_slips <- list()  # all the payment slips go here
  
  # This function makes fake workers for testing
  # I set it to make at least 400 workers
  generate_workers <- function(num_workers = 400) {
   
    tryCatch({
      # Check if we have enough workers
      if (num_workers < 400) {
        stop("We need at least 400 workers!")
      }
      
    
      first_names <- c(
       
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
      )
      
    
      last_names <- c(
        "Adebayo", "Okafor", "Ibrahim", "Okonkwo", "Musa", "Eze", "Bello", "Okoro",
        "Aliyu", "Nwankwo", "Yusuf", "Okoye", "Garba", "Onyeka", "Suleiman",
        "Chukwu", "Abdullahi", "Okeke", "Usman", "Nwosu", "Yakubu", "Okafor", "Balogun",
        "Nnaji", "Shehu", "Ogunyemi", "Lawal", "Emeka", "Adamu", "Oladele",
        "Nnamdi", "Haruna", "Ogbonna", "Salisu", "Adeyemi", "Chukwuma", "Ismail", "Ogundimu",
        "Onyeama", "Mamman", "Olaniyan", "Danjuma", "Okafor", "Tanko", "Adebisi", "Nwachukwu",
        "Abubakar", "Okonkwo", "Sadiq", "Ogundipe", "Umar", "Chukwuemeka", "Baba", "Oladipo",
        "Nwokolo", "Tijani", "Ogunleye", "Kabir", "Adeyinka", "Chinedu", "Sani"
      )
      
      #lists for gender, department, and employee level
      genders <- c("Male", "Female")  # only two options for now
      departments <- c(
        "Construction", "Engineering", "Safety", "Administration", "Maintenance",
        "Quality Control", "Project Management", "Human Resources", "Finance",
        "Equipment Operations", "Site Supervision", "Logistics"
      )
      
      #employee levels
      employee_levels <- c("A1", "A5-F", "Standard")
      
      # Clear the workers list first
      workers <<- list()
      
      # Make workers one by one using a for loop
      for (i in 1:num_workers) {
        # Create one worker with random info
        worker <- list(
          worker_id = paste0("HC", sprintf("%04d", i)),  # HC0001, HC0002, etc.
          first_name = sample(first_names, 1),              # pick random first name
          last_name = sample(last_names, 1),                # pick random last name
          gender = sample(genders, 1),                      # pick Male or Female
          department = sample(departments, 1),              # pick random department
          salary = round(runif(1, min = 5000, max = 35000), 2),  # random salary
          hours_worked = sample(35:50, 1),                  # hours they worked
          overtime_hours = sample(0:15, 1),                 # extra hours
          employee_level = "Unassigned"                     # will figure this out later
        )
        # Add this worker to my list
        workers[[i]] <<- worker
      }
      
      # Tell the user how many workers I made
      cat(sprintf("I made %d workers!\n", length(workers)))
      return(workers)
      
    }, error = function(e) {
      # If something goes wrong, tell the user
      cat(sprintf("Oops! Something went wrong making workers: %s\n", e$message))
      stop(e)
    })
  }
  
  # This function figures out what level each worker should be
  
  assign_employee_level <- function(worker) {
    tryCatch({
      # Get the worker's info
      salary <- worker$salary
      gender <- worker$gender
      
      # Rule 1: If they make between $10,000 and $20,000, they get "A1"
      if (salary > 10000 && salary < 20000) {
        return("A1")
      }
      
      # Rule 2: If they make between $7,500 and $30,000 AND they're female, they get "A5-F"
      else if (salary > 7500 && salary < 30000 && tolower(gender) == "female") {
        return("A5-F")
      }
      
      # If they don't match any rules, they get "Standard"
      else {
        return("Standard")
      }
      
    }, error = function(e) {
      # If something breaks, tell me which worker had the problem
      worker_name <- "Unknown"
      if (!is.null(worker$worker_id)) {
        worker_name <- worker$worker_id
      }
      cat(sprintf("Problem with worker %s: %s\n", worker_name, e$message))
      return("Error")
    })
  }
  
  # This function calculates how much money each worker gets
 
  calculate_payment <- function(worker) {
    tryCatch({
      # Get the worker's basic info
      base_salary <- worker$salary
      hours_worked <- worker$hours_worked
      overtime_hours <- worker$overtime_hours
      
      # Figure out weekly pay (their yearly salary divided by 52 weeks)
      weekly_base <- base_salary / 52
      
      # Calculate overtime pay (they get 1.5 times normal rate for extra hours)
      hourly_rate <- base_salary / (52 * 40)  # 40 hours per week is normal
      overtime_pay <- overtime_hours * hourly_rate * 1.5
      
      # Add everything together
      total_payment <- weekly_base + overtime_pay
      
      # Take out taxes, i used 20%
      deductions <- total_payment * 0.20
      net_payment <- total_payment - deductions
      
      # Return all the numbers (rounded to 2 decimal places)
      return(list(
        weekly_base = round(weekly_base, 2),
        overtime_pay = round(overtime_pay, 2),
        total_gross = round(total_payment, 2),
        deductions = round(deductions, 2),
        net_payment = round(net_payment, 2)
      ))
      
    }, error = function(e) {
      # If the math breaks, give them zeros and tell me about it
      worker_name <- "Unknown"
      if (!is.null(worker$worker_id)) {
        worker_name <- worker$worker_id
      }
      cat(sprintf("Math problem with worker %s: %s\n", worker_name, e$message))
      return(list(
        weekly_base = 0,
        overtime_pay = 0,
        total_gross = 0,
        deductions = 0,
        net_payment = 0
      ))
    })
  }
  
  # This function makes payment slips for all the workers
  # It's like making a receipt for each person
  generate_payment_slips <- function() {
    tryCatch({
      # Check if we have any workers first
      if (length(workers) == 0) {
        stop("I don't have any workers! Make some workers first.")
      }
      
      # Clear the payment slips list and get today's date
      payment_slips <<- list()
      current_date <- Sys.Date()
      
      cat("Making payment slips for everyone...\n")
      
      # Go through each worker one by one
      for (i in 1:length(workers)) {
        tryCatch({
          # Get this worker's info
          worker <- workers[[i]]
          
          # Figure out their employee level
          employee_level <- assign_employee_level(worker)
          worker$employee_level <- employee_level
          workers[[i]] <<- worker
          
          # Calculate how much money they get
          payment_details <- calculate_payment(worker)
          
          # Make a payment slip for this worker
          payment_slip <- list(
            slip_id = paste0("PS", worker$worker_id, format(Sys.Date(), "%Y%m%d")),
            date_generated = as.character(current_date),
            worker_info = list(
              worker_id = worker$worker_id,
              name = paste(worker$first_name, worker$last_name),
              gender = worker$gender,
              department = worker$department,
              employee_level = employee_level
            ),
            work_details = list(
              annual_salary = worker$salary,
              hours_worked = worker$hours_worked,
              overtime_hours = worker$overtime_hours
            ),
            payment_details = payment_details
          )
          
          # Add this payment slip to my list
          payment_slips[[i]] <<- payment_slip
          
        }, error = function(e) {
          # If something goes wrong with one worker, keep going with the others
          worker_name <- "Unknown"
          if (!is.null(workers[[i]]$worker_id)) {
            worker_name <- workers[[i]]$worker_id
          }
          cat(sprintf("Problem with worker %s: %s\n", worker_name, e$message))
        })
      }
      
      # Tell the user how many payment slips I made
      cat(sprintf("I made %d payment slips!\n", length(payment_slips)))
      return(payment_slips)
      
    }, error = function(e) {
      # If the whole thing breaks, tell the user
      cat(sprintf("Big problem making payment slips: %s\n", e$message))
      stop(e)
    })
  }
  
  # This function saves all the payment slips to a file
  # I learned JSON is a good format for storing data
  save_payment_slips <- function(filename = "payment_slips.json") {
    tryCatch({
      # Make sure we have payment slips to save
      if (length(payment_slips) == 0) {
        stop("I don't have any payment slips to save! Make some first.")
      }
      
      # Convert everything to JSON format and save it
      json_data <- toJSON(payment_slips, pretty = TRUE, auto_unbox = TRUE)
      writeLines(json_data, filename)
      
      # Tell the user where I saved the file
      cat(sprintf("I saved all the payment slips to %s\n", filename))
      
    }, error = function(e) {
      # If saving fails, tell the user
      cat(sprintf("Couldn't save the file: %s\n", e$message))
      stop(e)
    })
  }
  
  # This function prints a nice summary of everything
  # I tried to make it look professional like the reports at my dad's work
  print_summary_report <- function() {
    tryCatch({
      # Check if we have any payment slips to summarize
      if (length(payment_slips) == 0) {
        cat("I don't have any payment slips to summarize!\n")
        return()
      }
      
      # Print a fancy header
      cat("\n", paste(rep("=", 60), collapse = ""), "\n")
      cat("HIGHRIDGE CONSTRUCTION COMPANY - PAYMENT SUMMARY REPORT\n")
      cat(paste(rep("=", 60), collapse = ""), "\n")
      cat(sprintf("Report Date: %s\n", Sys.time()))
      cat(sprintf("Total Workers Processed: %d\n", length(payment_slips)))
      
      # Count how many workers are in each level
      level_counts <- table(sapply(payment_slips, function(x) x$worker_info$employee_level))
      # Add up all the money
      total_gross <- sum(sapply(payment_slips, function(x) x$payment_details$total_gross))
      total_net <- sum(sapply(payment_slips, function(x) x$payment_details$net_payment))
      
      cat("\nEmployee Level Distribution:\n")
      for (level in names(level_counts)) {
        count <- level_counts[level]
        percentage <- (count / length(payment_slips)) * 100
        cat(sprintf("  %s: %d workers (%.1f%%)\n", level, count, percentage))
      }
      
      # Show the money totals
      cat(sprintf("\nTotal Gross Payments: $%.2f\n", total_gross))
      cat(sprintf("Total Net Payments: $%.2f\n", total_net))
      cat(sprintf("Total Deductions: $%.2f\n", total_gross - total_net))
      cat(paste(rep("=", 60), collapse = ""), "\n")
      
    }, error = function(e) {
      # If something goes wrong with the summary, tell the user
      cat(sprintf("Problem making the summary: %s\n", e$message))
    })
  }
  
  # Return all my functions so other parts of the program can use them
  # This is like making a toolbox with all my tools in it
  return(list(
    generate_workers = generate_workers,
    assign_employee_level = assign_employee_level,
    calculate_payment = calculate_payment,
    generate_payment_slips = generate_payment_slips,
    save_payment_slips = save_payment_slips,
    print_summary_report = print_summary_report,
    get_workers = function() workers,
    get_payment_slips = function() payment_slips
  ))
}

# This is the main function that runs everything
# I put all the steps here so it's easy to follow
main <- function() {
  tryCatch({
    cat("Highridge Construction Company - Weekly Payment System (R Version)\n")
    cat("Starting my payment program...\n\n")
    
    # Start up my payment system
    payment_system <- PaymentSystem()
    
    # Make 450 workers (the boss said at least 400)
    workers <- payment_system$generate_workers(450)
    
    # Make payment slips for everyone
    payment_slips <- payment_system$generate_payment_slips()
    
    # Save everything to a file
    payment_system$save_payment_slips("highridge_payment_slips_r.json")
    
    # Show a nice summary
    payment_system$print_summary_report()
    
    cat("\nAll done! Everything worked!\n")
    
  }, error = function(e) {
    # If something really bad happens, tell the user
    cat(sprintf("Oh no! Something went really wrong: %s\n", e$message))
    cat("Maybe ask someone who knows more about R to help.\n")
  })
}

# This runs my program when I execute the script
# I learned this from a tutorial online
if (!interactive()) {
  main()
}