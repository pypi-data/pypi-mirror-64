import os
import frontmatter
from paka import cmark


class PostMiner:
    def __init__(self, collection_name="posts", model=None, location="collections"):
        self.model = model
        self.collection_name = collection_name
        self.location = location
        self.data = []

    def collect(self):
        for file in os.listdir(os.path.join(self.location, self.collection_name)):
            with open(
                os.path.join(self.location, self.collection_name, file), "r"
            ) as f:
                metadata, content = frontmatter.parse(f.read())
                object = metadata
                object["slug"] = file.split(".")[0]
                object["content"] = cmark.to_html(content)  # speed improvement
                # object["content"] = markdown.markdown(content)
                self.data.append(object)
        self.data.sort(key=lambda x: x["date"])
        self.data.reverse()
        return {self.collection_name: self.data}


class BlogMapper:
    def __init__(self, base_url=""):
        self.urls = {}
        self.base_url = base_url

    def map(self, site):
        self.urls.update(self.posts(site))
        self.urls.update(self.blog_index(site))
        self.urls.update(self.tags(site))

        return self.urls

    def posts(self, site):
        urls = {}
        for post in site["posts"]:
            urls.update(
                {
                    f"posts.{post['slug']}": {
                        "url": self.base_url + f"/posts/{post['slug']}/",
                        "data": post,
                        "default_template": "post.html",
                        "renderer": "main_renderer",
                    }
                }
            )

        return urls

    def blog_index(self, site):
        urls = {}
        posts = site["posts"][1:]

        per_page = 5
        paginated_posts = [
            posts[x * per_page : (x + 1) * per_page]
            for x in range(len(posts) // per_page + 1)
        ]

        for i, posts in enumerate(paginated_posts, 1):
            url = f"/index/{i}/" if i > 1 else "/"
            if i > 2:
                previous_page_url = f"/index/{i-1}/"
            elif i == 2:
                previous_page_url = "/"
            else:
                previous_page_url = ""
            if i < len(posts):
                next_page_url = f"/index/{i+1}/"
            else:
                next_page_url = ""

            paginator = {
                "posts": posts,
                "index": i,
                "next_page_url": self.base_url + next_page_url,
                "previous_page_url": self.base_url + previous_page_url,
            }
            data = {
                "title": "blog",
                "paginator": paginator,
            }
            urls.update(
                {
                    f"blog_index.{i}": {
                        "url": self.base_url + url,
                        "data": data,
                        "default_template": "blog_index.html",
                        "renderer": "main_renderer",
                    }
                }
            )

        return urls

    def tags(self, site):
        urls = {}

        for tag in site["tags"]:

            posts = site["posts"]
            posts = [post for post in posts if tag["name"] in post["tags"]]

            per_page = 5
            paginated_posts = [
                posts[x * per_page : (x + 1) * per_page]
                for x in range(len(posts) // per_page + 1)
            ]

            for i, posts in enumerate(paginated_posts, 1):
                url = f"/tags/{tag['slug']}/{i}/" if i > 1 else f"/tags/{tag['slug']}/"
                if i > 2:
                    previous_page_url = f"/tags/{tag['slug']}/{i-1}/"
                elif i == 2:
                    previous_page_url = f"/tags/{tag['slug']}/"
                else:
                    previous_page_url = ""
                if i < len(posts):
                    next_page_url = f"/tags/{tag['slug']}/{i+1}/"
                else:
                    next_page_url = ""

                paginator = {
                    "posts": posts,
                    "index": i,
                    "next_page_url": self.base_url + next_page_url,
                    "previous_page_url": self.base_url + previous_page_url,
                }
                data = {
                    "title": f"Posts tagged {tag['name']}",
                    "tag_slug": tag["slug"],
                    "paginator": paginator,
                }
                urls.update(
                    {
                        f"tags.{tag['slug']}.{i}": {
                            "url": self.base_url + url,
                            "data": data,
                            "default_template": "tag.html",
                            "renderer": "main_renderer",
                        }
                    }
                )

        return urls
