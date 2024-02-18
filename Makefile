IMAGE_NAME := plex-prefer-non-forced-subs
VERSION := latest
REGISTRY_ADDR := jb6magic

.SILENT:clean
.PHONY: clean

push: tag
	docker push $(REGISTRY_ADDR)/$(IMAGE_NAME):$(VERSION)

tag: build
	docker tag $(IMAGE_NAME):$(VERSION) $(REGISTRY_ADDR)/$(IMAGE_NAME):$(VERSION)

build: Dockerfile
	docker build --no-cache --rm -t $(IMAGE_NAME):$(VERSION) -f Dockerfile .

test: tag
	docker run -e "PLEX_URL=${PLEX_URL}" -e "PLEX_TOKEN=${PLEX_TOKEN}" $(REGISTRY_ADDR)/$(IMAGE_NAME):$(VERSION)

clean:
	docker container prune -f
	docker image prune -f
	docker volume prune -f
