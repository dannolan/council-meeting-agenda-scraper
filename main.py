import os.path

from functions import download_pdf, read_pdf, parse_pdf, write_email, send_email
import database as db
from custom_types import Council
from regexes import RegexResults

# Web scraping
from scrapers import councils

from dotenv import dotenv_values
config = dotenv_values(".env")


def processor(council: Council):  
  print(f'Running {council.name} scraper...')
  download_link = council.scraper()

  if not download_link:
    print(f'No link found for {council.name}.')
    return
  if db.check_link(download_link):
    print(f'Link already scraped for {council.name}.')
    return
  
  print('Link scraped! Downloading PDF...')
  download_pdf(download_link, council.name)
  
  print('PDF downloaded! Reading PDF into memory...')
  text = read_pdf(council.name)
  
  print('PDF read! Parsing PDF...')
  parser_results = parse_pdf(council.regexes, text)  
  
  print('PDF parsed! Inserting into database...')
  db.insert(council.name, download_link, parser_results)
  print('Database updated!')
  
  print('Sending email...')
  
  email_body = write_email(council.name, download_link, parser_results)

  send_email(config['GMAIL_ACCOUNT_RECEIVE'], 
              f'New agenda: {council.name}', 
              email_body)
  
  print(f'Finished with {council.name}.')  
  

def main():
  if not os.path.exists('./agendas.db'):
    db.init()
  
  for council in councils:
    processor(council)
  
  
if __name__ == '__main__':
  main()