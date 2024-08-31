create:
	docker build -t sastra-cakshuh .
	mkdir -p -- files

run:
	docker run -it -v $(shell pwd)/files:/usr/src/app/files --name sastra-cakshuh-con --rm sastra-cakshuh

stop:
	docker stop sastra-cakshuh-con


delete:
	docker rmi sastra-cakshuh
