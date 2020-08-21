import argparse
import extract


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="File of URLs to be analyzed", default="urls/international/urls-phishing.csv")
    parser.add_argument("output", help="Output File", default="dataset/dataset.csv")
    parser.add_argument("phishing", help="True/False", default="True")
    args = parser.parse_args()
    if args.input and args.output:
        # Update phishtank database
        # print('Download and update phishtank database...')
        # update_db()
        # Starts extraction
        print('Starts training features extraction...')
        extract.main(args.input, args.output, args.phishing)
        print('''
                #######################################
                #   Dataset generated successfully!   #
                #######################################
            ''')


if __name__ == "__main__":
    main()
