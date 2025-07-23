#!/bin/bash
export $(grep -v '^#' .env | xargs)
uvicorn api.main:app --host $HOST --port $PORT --reload
