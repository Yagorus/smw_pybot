TAG ?= latest
REGISTRY_ID ?= 264716044050
REPOSITORY_REGION ?= eu-central-1
APP_NAME ?= bot
ENV_NAME ?= dev

BOT_TOKEN ?= error
API_KEY ?= error

REPO_NAME = $(REGISTRY_ID).dkr.ecr.$(REPOSITORY_REGION).amazonaws.com/${APP_NAME}-${ENV_NAME}

.PHONY: build
build:
	#echo "BOT_TOKEN - $(BOT_TOKEN)"
	#echo "API_KEY - $(API_KEY)"
	#echo "REGISTRY_ID - $(REGISTRY_ID)"
	aws ecr get-login-password --region $(REPOSITORY_REGION) | docker login --username AWS --password-stdin $(REGISTRY_ID).dkr.ecr.$(REPOSITORY_REGION).amazonaws.com
	
	docker build --build-arg token=$(BOT_TOKEN) --build-arg api_key=$(API_KEY) -t $(REPO_NAME):$(TAG) -f ./Dockerfile .
	
	docker push $(REPO_NAME):$(TAG)