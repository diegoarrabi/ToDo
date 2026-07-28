set reminderTODO to "Variable"
set reminderDATE to current date
tell reminderDATE to set {its hours, its minutes, its seconds} to {8, 0, 0}


(*
tell application "Reminders"
	
	set myList to list "ToDo"
	tell myList
		make new reminder with properties {name:reminderTODO, due date:reminderDATE}
	end tell
	
end tell
*)

display dialog "COW"

