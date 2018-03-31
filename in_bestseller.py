import re, requests, csv
from bs4 import BeautifulSoup

def spider():
    out_file = open('in_book.csv', 'w')
    csv_writer = csv.writer(out_file, delimiter=',')
    csv_writer.writerow(['Name', 'URL', 'Author', 'Price', 'Number of Ratings', 'Average Rating'])

    for pages in range(1, 6):
        url = 'https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_2?ie=UTF8&pg={}'.format(pages)
        source_code = requests.get(url)
        soup = BeautifulSoup(source_code.text, "html.parser")

        """For each of the Div Wrappers containing each of the books' information"""
        for book in soup.findAll('div', {'class':'zg_itemWrapper'}):
            contents = book.decode_contents(formatter="html")
            soup2 = BeautifulSoup(contents, "html.parser")
            csv_row = list()

            """Book Title"""
            try:
                csv_row.append(soup2.find('div', {'class':'p13n-sc-truncate'}).string.strip())
            except:
                csv_row.append("Not available")

            """Book Link"""
            try:
                csv_row.append('https://www.amazon.in' + soup2.find('a', {'class':'a-link-normal'}).get('href'))
            except:
                csv_row.append("Not available")

            """Author Name"""
            try:
                csv_row.append(soup2.find('a', {'class':'a-size-small a-link-child'}).string)
            except:
                try:
                    csv_row.append(soup2.find('span', {'class':'a-size-small a-color-base'}).string)
                except:
                    csv_row.append("Not available")

            """Price"""
            try:
                csv_row.append(u"\u20B9" + re.search(r'-?\d+\.?\d*', soup2.find('span', {'class':'p13n-sc-price'}).decode_contents(formatter="html")).group(0))
            except:
                csv_row.append("Not available")

            """Number of ratings and Average ratings"""
            try:
                csv_row.append(soup2.find('a', {'class':'a-size-small a-link-normal'}).string)
                csv_row.append(soup2.find('span', {'class':'a-icon-alt'}).string)
            except:
                csv_row.append("Not available")
                csv_row.append("Not available")

            csv_writer.writerow(csv_row)
    out_file.close()

spider()
