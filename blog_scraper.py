from bs4 import BeautifulSoup
import requests
import csv
def scrape_medium_blog(url):
    """
    Scrapes the content of a Medium blog post.

    Args:
        url (str): The URL of the Medium blog post.

    Returns:
        dict: A dictionary containing the title, author, and content of the blog post.
    """
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": f"Failed to fetch the page, status code: {response.status_code}"}

    soup = BeautifulSoup(response.content, "html.parser")

    #the title
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Title not found"

    #the author
    author_tag = soup.find("meta", attrs={"name": "author"})
    author = author_tag["content"] if author_tag else "Author not found"

    #the content
    content_tags = soup.find_all("p")
    content = "\n".join(tag.get_text(strip=True) for tag in content_tags) if content_tags else "Content not found"

    return {
        "title": title,
        "author": author,
        "content": content
    }


if __name__ == "__main__":
    blog_url = "Put Your URL here"  # Replace blog URL
    blog_data = scrape_medium_blog(blog_url)

    if "error" in blog_data:
        print(blog_data["error"])
    else:
        print("Title:", blog_data["title"])
        print("Author:", blog_data["author"])
        print("Content:\n", blog_data["content"])

        # Save the content to a file
        with open("medium_blog_content.csv", "w", encoding="utf-8",newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Title", "Author", "Content"])
            csvwriter.writerow([blog_data["title"], blog_data["author"], blog_data["content"]])      

        print("Blog content has been saved to medium_blog_content.csv.")
