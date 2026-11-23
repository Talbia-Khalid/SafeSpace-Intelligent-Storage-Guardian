
CC = gcc

CFLAGS = -Wall -Wextra -std=c11 -D_POSIX_C_SOURCE=200809L -Iinclude -pthread

LIBS = -pthread -lsqlite3 -lcrypto

TARGET = backend/safespace

SOURCES = $(wildcard backend/*.c)

all: $(TARGET)

$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) $(SOURCES) -o $(TARGET) $(LIBS)

clean:
	rm -f $(TARGET)

run: all
	./$(TARGET)

.PHONY: all clean run

