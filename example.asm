  # setup initial values
	li $t0, 0
	addi $t0, $t0, 6

	# Multiply A ($t1) and B ($t2)
	li $t1, 4
	li $t2, 6

	# Setup A, B, and -b
	booth-load $t1, $t2

start:

	booth-add
	sra $b0, $b0, 2

	# keep track of the shifts. (This is some do while logic.)
	addi $t0, $t0, 1		# Increment the counter
	slti $a0, $t4, 16		# set if $t4 is less than 16
	bne $a0, $zero, start	# If i = 7 then continue with the rest of the program.


	# Print values added to console
	li $v0, 1
	move $a0, $t1
	syscall


	# exit the program
	li $v0, 10
	syscall
