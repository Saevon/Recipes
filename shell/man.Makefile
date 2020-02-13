# Debug Mode
	make -n -d all




#
# Normally make removes any intermediate files that were generated
# aka any you didn't explicitly ask for
# You can see this using
	make -n -d all
	"Removing intermediate files..."
	"rm intermediate.o ..."
# You can ask a file to be kept regardless using the following
.PRECIOUS: my_file
my_file:
	@command



# Throwing error messages (and exiting)
target:
	$(error "Oh noes Something broke")
	# Doesn't exit
	$(warning "Sort of bad?")
	$(info "Something you should know")

