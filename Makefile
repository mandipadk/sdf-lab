IMAGE ?= sdf-lab:dev
TORCH_IMAGE ?= pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime

.PHONY: build up test bash

build:
	docker build --build-arg TORCH_IMAGE=$(TORCH_IMAGE) -t $(IMAGE) .

up:
	TORCH_IMAGE=$(TORCH_IMAGE) docker compose up --build api

test:
	docker compose run --rm test

bash:
	docker run --rm -it --gpus all -p 9000:9000 -v $(PWD):/workspace $(IMAGE) bash
