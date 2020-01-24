# Enron_Aktia
Python development challenge - Enron Emails

# How to run
We assume that the email dataset has been downloaded and extracted to the project repository.

1. Install dependencies from the Pipfile.lock in the repository via pipenv using the command 'pipenv install --ignore-pipfile'
2. Run the python script main.py in the created virtual environment using the command 'pipenv run python main.py'

# A note on email parsing
In some of the emails, the email parser encountered Unicode errors. For the moment, these bytes are replaced.

# Assumptions on emails
We calculate repeating recipients in the recipient headers as unique emails. Thus it can be that some emails are counted twice.
