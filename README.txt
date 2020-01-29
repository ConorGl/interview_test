This python project is fairly simple to run. It only requires a virtual environment with a python3 installation to work as the packages within are part of the standard library.
To run, all you need to do is clone the repo locally and run the json_converter.py file. This should create a new file called active_customers.db.
Once this is created, run the db_checker.py file to check the rows in the table. They are of the form (date, active_user_count).

In order to create an ETL process automatically, there are a couple of ways to do it but it really depends on the way that the data is received. In it's simplest form, if we are given a json dump once a day, we could run a crontab to run the file daily.
If we wanted to scale this up, we could change the process to batch the rows up and process them more effectively, we could think about upgrading the hardware that is running the process or we could get it to run through an AWS Lambda function from an s3 bucket which we could auto-scale.
The target architecture for something like this would be to have an s3 bucket which the json gets dumped in to with a lambda set up running this in to a Redshift warehouse. We would also want to make considerations for archiving the data so that the s3 bucket is kept in good working order.

requirements.txt
