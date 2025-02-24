import pipeline as pl

def main() -> int:
    url = "testdata.json"#"https://api-web.nhle.com/v1/schedule/now" #Example url
    p = pl.DataPipeline(url)
    p.run_pipeline()

    return 0

if __name__ == '__main__':
    main()