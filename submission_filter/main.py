from submission_fetcher import SubmissionFetcher
from submission_filter import SubmissionFilter

def main():
    subs = SubmissionFetcher().fetch_submissions("askhistorians", 1000)
    SubmissionFilter().filter_submissions(subs)

if  __name__ == "__main__":
    main()