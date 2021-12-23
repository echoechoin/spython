.PHONEY: clean install uninstall all
all:./src/encrypt_file.c
	gcc -fpic -shared  ./src/encrypt_file.c -o ./src/libencfile.so -lcrypto -lssl
	@mv ./src/libencfile.so ./libencfile.so
	@install -m 777 ./src/spython-enc.py ./spython-enc

install:
	@echo "info: installing..."
	@install -c ./libencfile.so /lib
	@install -m 777 ./spython-enc /bin/spython-enc
	@echo "info: success!"

uninstall:
	@echo "info: uninstalling..."
	@rm -f /lib/libencfile.so
	@rm -f /bin/spython-enc
	@echo "info: success!"

clean:
	rm -f ./spython-enc
	rm -f ./libencfile.so
