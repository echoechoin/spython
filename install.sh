@echo "info: installing..."
@install -c ./src/libencfile.so /lib
@install -m 777 ./src/encry.py /bin/rayencry
@cp ./src/progress_webray /lib/python2.7 -r
@echo "info: success!"