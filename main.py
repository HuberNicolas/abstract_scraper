import pandas as pd
from pyalex import Works
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import argparse


def process_row(index, row):
    """
    Process a single row: fetch abstract.
    """
    result = {"index": index, "abstract": None}

    # Skip rows where abstract is already present
    if pd.notnull(row.get('abstract', None)):
        print(f"Skip row {index}")
        return result
    

    doi = row.get('doi', None)
    if not doi:
        return result

    doi_url = f"https://doi.org/{doi}"
    try:
        # Fetch work details using Pyalex
        work = Works()[doi_url]

        # Extract abstract
        result["abstract"] = work["abstract"] if work["abstract"] else None

    except Exception as e:
        print(f"Could not extract abstract for DOI {doi}: {e}")

    return result


def main(input_file, output_file, num_workers, save_interval):
    # Read the input CSV
    df = pd.read_csv(input_file)

    # Add 'abstract' column if not already present
    if 'abstract' not in df.columns:
        df['abstract'] = None

    progress_count = 0  # Counter for processed rows

    # Parallel processing
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {
            executor.submit(process_row, index, row): index
            for index, row in df.iterrows()
        }

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing"):
            try:
                # Retrieve the result
                result = future.result()
                index = result["index"]
                abstract = result["abstract"]

                # Update the DataFrame
                if abstract:
                    df.at[index, 'abstract'] = abstract

                # Increment the progress counter
                progress_count += 1

                # Save progress periodically
                if progress_count % save_interval == 0:
                    print(f"Saving progress at {progress_count} processed rows...")
                    df.to_csv(output_file, index=False)

            except Exception as e:
                print(f"Error during processing: {e}")

    # Final save after all rows are processed
    df.to_csv(output_file, index=False)
    print(f"Processing complete. Results saved to '{output_file}'.")


if __name__ == "__main__":
    # Set up CLI arguments
    parser = argparse.ArgumentParser(description="Process DOIs to fetch abstracts and save periodically.")
    parser.add_argument("input_file", type=str, help="Path to the input CSV file.")
    parser.add_argument("output_file", type=str, help="Path to the output CSV file.")
    parser.add_argument("--num_workers", type=int, default=4, help="Number of parallel workers (default: 4).")
    parser.add_argument("--save_interval", type=int, default=50, help="Save progress after this many rows (default: 50).")

    # Parse arguments
    args = parser.parse_args()

    # Run the main function with parsed arguments
    main(args.input_file, args.output_file, args.num_workers, args.save_interval)
