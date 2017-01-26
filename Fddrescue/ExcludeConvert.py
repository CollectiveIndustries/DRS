




with open(EXCLUDE_FILE) as f:
    for line in f:        # Read line by line and apply case insensitive regex to the line and write it back to a new file.
	for char in line:    # Loop accross each char in line and apply [charCHAR] rules in a new file
		# ignore / + - * in the case matching

