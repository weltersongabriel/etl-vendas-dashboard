from scripts.extract import extract
from scripts.tranform import transform
from scripts.load import load

def run_pipeline():
    df = extract()
    df = transform(df)
    load(df)

if __name__ == "__main__":
    run_pipeline()