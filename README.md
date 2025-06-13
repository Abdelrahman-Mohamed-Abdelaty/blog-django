# Django Blog App

A simple blogging web application built using **Django**. It supports listing blog posts, viewing individual post details, adding comments, and saving posts for later reading using session-based storage.

---

## Features

* Display the latest 3 posts on the homepage (`StartingPageView`).
* Show all blog posts in descending order by date (`AllPostsView`).
* View detailed blog post pages with comments and tags (`PostDetailView`).
* Submit comments on posts via a form (`CommentForm`).
* Save posts to a "Read Later" list stored in session data (`ReadLaterView`).
* Admin panel to manage posts, authors, tags, and comments (`PostAdmin`).

---

## Views and Routes

### URL Configuration (`blog/urls.py`)

| URL Pattern          | View             | Name               |
| -------------------- | ---------------- | ------------------ |
| `/`                  | StartingPageView | `starting-page`    |
| `/posts/`            | AllPostsView     | `posts-page`       |
| `/post/<slug:slug>/` | PostDetailView   | `post-detail-page` |
| `/read-later/`       | ReadLaterView    | `read-later`       |

### Views Overview

* **StartingPageView**: Lists the 3 latest posts using `ListView`.
* **AllPostsView**: Lists all posts ordered by date.
* **PostDetailView**: Handles both GET (view post + comments) and POST (submit comment) requests. Also checks if a post is saved for later.
* **ReadLaterView**: Allows users to add or remove post IDs to their session-based read-later list and view them.

---

## Author

**Abdelrahman Mohamed**

---
