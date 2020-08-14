.PHONEY: clean install uninstall all
all:./src/encrypt_file.c
	gcc -fpic -shared  ./src/encrypt_file.c -o ./src/libencfile.so -lcrypto -lssl	
	@install -m 777 ./src/encry.py ./rayencry

install:
	@echo "info: installing..."
	@install -c ./src/libencfile.so /lib
	@install -m 777 ./src/encry.py /bin/rayencry
	@cp ./src/progress_webray /lib/python2.7 -r
	@echo "info: success!"

uninstall:
	@echo "info: uninstalling..."
	@rm -f /lib/libencfile.so
	@rm -f /bin/rayencry
	@rm -f /lib/python2.7/progress_webray -r
	@echo "info: success!"

clean:
	rm -f ./rayencry
	rm -f ./src/libencfile.so
