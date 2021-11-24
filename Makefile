.PHONEY: clean install uninstall all
all:./src/encrypt_file.c
	gcc -fpic -shared  ./src/encrypt_file.c -o ./src/libencfile.so -lcrypto -lssl	
	@install -m 777 ./src/spython-encry.py ./spython-encry

install:
	@echo "info: installing..."
	@install -c ./src/libencfile.so /lib
	@install -m 777 ./src/spython-encry.py /bin/spython-encry
	@echo "info: success!"

uninstall:
	@echo "info: uninstalling..."
	@rm -f /lib/libencfile.so
	@rm -f /bin/spython-encry
	@echo "info: success!"

clean:
	rm -f ./spython-encry
	rm -f ./src/libencfile.so
