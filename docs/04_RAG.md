# Retrieval-Augmented Generation

## Purpose

Prevent hallucinations.

All legal answers must be grounded in retrieved documents.

## Sources

GDPR

HIPAA

PCI DSS

CCPA

UK GDPR

## Pipeline

Legal Documents

↓

Chunking

↓

Embedding Generation

↓

Vector Database

↓

Retriever

↓

LLM

## Metadata

Each chunk contains:

- title
- regulation
- article
- category
- source

## Vector DB

- SQLite + NumPy vector store (`vector_chunks` table in `vector_store.db`)
