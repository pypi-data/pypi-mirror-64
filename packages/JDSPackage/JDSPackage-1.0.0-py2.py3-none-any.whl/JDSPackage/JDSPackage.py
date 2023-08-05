"""Main module."""

#Functions for header info in notebooks to automate including your name, date, and version number of a notebook

def Header(name, project_name):
    """
    This is a quick way to create a header for your notebook.
    
    Parameters:
    
    first_name (string): Input your first name
    last_name (string): Input your last name
    project_name (string): Place your project name here

    Returns:

    name: Print out of the first and last name of the notebook creator
    project_name: Print out of the project name
    
    
    
    """
    first_name = 'Jamaal'
    last_name = 'Smith'
    name = (first_name  , last_name)
    project_name = 'Flatiron School Capstone Project'
    print(name[0], name[1])
    print (project_name)
    
    


    