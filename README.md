# TO-DO-List-command-line

Simple TO-DO list that runs with a command-line type input, uses sqlite3 to store the data. Shows the date created, the status of the task, and the task itself. Also will show if an item is flagged, which will be displayed at the very top of every list. A good feature would be the ability to create different To-Do lists but I will do this at another time. 

## Features

**LIST ALL**		Lists all to-do's, dates, and status.

**DONE #**			Completes specified task

**DONE ALL**		Completes all tasks in database.

**DELETE #**		Deletes specifed task.

**DELETE ALL**		Deletes all tasks in database.

**DELETE DONE** 	Deletes all completed items.

**TODO ...**		Creates new todo task.

**TODO EDIT #**		Allows you to edit the todo item.

**FLAG #**       Marks task as important, deleting requires
			confirmation and task will display at the
			top of every LIST. Doing this twice will 
			unflag the item.
    
