#!/bin/bash
# Script para iniciar el servidor FastAPI con Uvicorn
echo "Iniciando backend FastAPI..."
uvicorn app.main:app --reload
