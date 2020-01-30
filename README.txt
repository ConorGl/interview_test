This python project is fairly simple to run. It only requires a virtual environment with a python3 installation to work as the packages within are part of the standard library. To run, all you need to do is clone the repo locally and run the json_converter.py file. This should create a new file called active_customers.db which is an open sqlite3 db. Once this is created, run the db_checker.py file to check the rows in the table. They are of the form (date, active_user_count). Once complete, the process will not keep inserting rows as will detect the date has already been loaded.

Interview Question 

2)
In order to create an ETL process automatically, there are a couple of ways to do it but it really depends on the way that the data is received. In its simplest form, if we are given a json dump once a day, we could run a crontab to run the file daily. If we wanted to scale this up, we could change the process to batch up the rows and send them to DynamoDB/S3 so we could get it to run through an AWS Lambda function. Then we could archive the old data in an s3 bucket and leave our work space clean.

3)
The target architecture for something like this would be to have an s3 bucket which the json gets dumped in to with a lambda set up running this in to a Redshift warehouse. We would also want to make considerations for archiving the data so that the s3 bucket is kept in good working order which would also give us the ability to re-use the data if we wanted to extract further info from it.