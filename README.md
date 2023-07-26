# Japanese-Wikipedia-Scraper
A Python script I used to randomly scrape sentences from Japanese Wikipedia and write them in an output file. I may use this data for some language-learning based project in the future. 

The script uses the selenium library for webscraping

The script works by the following process

1. The script uses wikipedia's "random article" function to visit a random article.
2. The script records every sentence in this article in the file
3. The script finds every link on the article that leads to another article.
4. If the script finds no links that lead to an article it has not yet read, it restarts with another random article.
5. The script selects a maximum of 10 random links from the article that lead to articles it has not yet read.
6. If there are 10 or fewer unvisited links on the article, the script will select all of them.
7. Out of the 10 or fewer selected article links, the script next visits the article with the greatest length.
