from bs4 import BeautifulSoup
import requests
base_url = "https://www.imdb.com/list/ls048276758/"

for page in range(1, 11):
    url = f"{base_url}?st_dt=&mode=detail&page={page}&sort=list_order,asc"
    html_text = requests.get(url).text

    # print(html_text)

    soup = BeautifulSoup(html_text, 'lxml')
    movies = soup.find_all('div', class_= "lister-item-content")
# print(movie)
    # Movie title: 
    movie_data_list = []
    for movie in movies:
       title = movie.find('a').text.strip()
       year = movie.find('span', class_="lister-item-year text-muted unbold").text.strip().replace('(', '').replace(')', '')     #remove ngoặc ở (1972)
       runtime= movie.find('span',class_="runtime" ).text.strip()
       genre_element = movie.find('span', class_="genre")
       genre = genre_element.text.strip() if genre_element else 'N/A'
       rating_star= movie.find('span', class_="ipl-rating-star__rating").text.strip()
       meta_score = soup.find('span', class_='metascore').text.strip() if soup.find('span', class_='metascore') else 'N/A'
       votes = movie.find('span', {'name':'nv'})['data-value']
       gross_element = movie.find('span', {'name': 'nv'})
       gross= gross_element['data-value'].replace('.', '').replace('$', '').replace('M', '') if gross_element and 'data-value' in gross_element.attrs else 'N/A'



       movie_data = { 
           "MovieTitle": title,
           "ReleaseYear": year,
           "Duration": runtime,
           "Genre": genre,
           "Rating": rating_star,
           "Metascore": meta_score,
           "Votes": votes,
           "Gross": gross}
       movie_data_list.append(movie_data)

    # Print data for the first movie on each page
    if movie_data_list:
        print(f"Page {page}, First Movie: {movie_data_list[0]}")      # Using f-string to format the string
    else:
        print(f"Page {page}, No movies found.")
# # Checking 10 first films: 
# for movie in movie_data_list[101:150]:
#     print(movie)

# Save as CSV files: 
import csv
csv_file_path = 'movies_dataset.csv'
fieldnames = movie_data_list[0].keys()     # Because it's in dict   => have to take dict key
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()     #writes the header row to the CSV file
    writer.writerows(movie_data_list)    #This line writes the data rows to the CSV file. The movie_data_list is a list of dictionaries, and each dictionary represents a row of data. The writerows method writes all the rows in one go.

print(f"Movie data saved to {csv_file_path}")

# # Check the location:  
# import os 
# absolute_path = os.path.abspath('movie_dataset.csv')


# print(movie)

# # movie = soup.find('h3', class_= "lister-item-header")  
# # print(movie)
# # Print movie name and year: 
# # movie_names= movie.find('a').text
# # print(movie_names)

# # year= movie.find('span', class_="lister-item-year text-muted unbold").text
# # print(year)

# # movie_details= soup.find('p', class_="text-muted text-small")
# # # print(movie_details)
# # runtime= movie_details.find('span',class_="runtime" ).text
# # genre= movie_details.find('span',class_="genre" ).text
# # print(runtime)
# # print(genre)

# # ratings= soup.find('div', class_="ipl-rating-widget")
# # star= ratings.find('span', class_="ipl-rating-star__rating").text
# # print(star)
# # print(ratings)

# # meta_scores= soup.find('div', class_="inline-block ratings-metascore")
# # print(meta_scores)
# # score = meta_scores.find('span',class_="metascore favorable").text
# # print(score)

# director= soup.find('p', class_="text-muted text-small")
# Vote= director.find('span', name_="nv")
# print(Vote)



