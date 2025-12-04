"""
Simple CLI for fetching UniProt FASTA by gene name.

Usage:
    python uniprot_cli.py

It will prompt for a gene name, search UniProt, download the first result's FASTA,
and save both the FASTA and metadata files.

Requires `requests` (used by uniprot_logic).
"""
from __future__ import annotations

import sys

from uniprot_logic import search_uniprot_by_gene, download_fasta, save_fasta, save_metadata


def main() -> int:
    try:
        gene = input("Enter gene name (e.g. KRAS): ").strip()
        if not gene:
            print("No gene provided. Exiting.")
            return 1

        print(f"Searching UniProt for gene '{gene}'...")
        result = search_uniprot_by_gene(gene)
        if not result:
            print(f"No protein found for this gene. Please check the gene name and try again.")
            return 1

        accession, metadata = result
        
        # Print metadata to console
        print(f"\nFound protein: {metadata.get('protein_name', 'Unknown')}")
        print(f"UniProt ID: {accession}")
        print(f"Organism: {metadata.get('organism_name', 'Unknown')}")
        print(f"Protein length: {metadata.get('protein_length', 0)} amino acids")
        if metadata.get('description'):
            print(f"Description: {metadata['description']}")
        
        print(f"\nDownloading FASTA for {accession}...")
        fasta = download_fasta(accession)

        fasta_file = save_fasta(fasta, gene, accession)
        metadata_file = save_metadata(metadata, gene, accession)
        
        print(f"Saved FASTA to: {fasta_file}")
        print(f"Saved metadata to: {metadata_file}")
        return 0

    except ValueError as ve:
        print(f"Input error: {ve}")
        return 1
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
