# Makefile TP3 INF8775

# Specifies the compiler to be used
CC = g++

# Path to include folder with .hpp files
IDIR = include
# Path to obj folder, where .o files are outputted
ODIR = obj
# Name of file containing cpp main function
OUT = tp3

# List of depencies (.hpp files), append files as needed
_DEPS =  
# Path replacement to access .hpp files to obj include dir
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS)) 

# List of all the object files (.o), append files as needed
_OBJ = $(OUT).o
# Path replacement to output/access .o file to obj dir
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

all: $(OUT)

# Rule to compile main from all the .o files and make it executable
$(OUT): $(OBJ)
	@$(CC) -o $@ $^
	@chmod +x $(OUT)

# General rule to compile .o files from their .cpp equivalents  
$(ODIR)/%.o: %.cpp $(DEPS)
	@$(CC) -c -o $@ $<

# To not mistake clean with a file
.PHONY: clean 

# Removes excess files
clean: 
	@rm -f $(ODIR)/*.o $(OUT)