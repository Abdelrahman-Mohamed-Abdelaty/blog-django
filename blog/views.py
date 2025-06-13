from django.shortcuts import render, get_object_or_404
from datetime import date
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Post
from django.views.generic import ListView, DetailView
from .forms import CommentForm
from django.views import View


class StartingPageView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    ordering = ["-date"]

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set[:3]


class AllPostsView(ListView):
    model = Post
    template_name = "blog/all-posts.html"
    context_object_name = "all_posts"
    ordering = ["-date"]


# authomatically search with slug
class PostDetailView(View):
    model = Post
    template_name = "blog/post-detail.html"
    context_object_name = "post"

    def is_saved_for_later(self, post_id, request):
        stored_posts = request.session.get("stored_posts", [])
        print(f"Stored posts in session: {stored_posts}")
        return post_id in stored_posts

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-created_at"),
            "saved_for_later": self.is_saved_for_later(str(post.id), request),
        }
        print(f"Post ID: {post.id}, Saved for later: {context['saved_for_later']}")
        return render(request, self.template_name, context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = get_object_or_404(Post, slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        return render(
            request,
            self.template_name,
            {
                "post": post,
                "post_tags": post.tags.all(),
                "comment_form": comment_form,
                "saved_for_later": self.is_saved_for_later(str(post.id), request),
            },
        )


class ReadLaterView(View):

    def get(self, request):
        post_ids = request.session.get("stored_posts", [])
        posts = Post.objects.filter(id__in=post_ids).order_by("-date")
        return render(request, "blog/stored-posts.html", {"posts": posts, "has_posts": len(post_ids) > 0})

    def post(self, request):
        post_id = request.POST.get("post_id")
        if not post_id:
            raise Http404("Post ID not provided.")

        post_ids = request.session.get("stored_posts", [])
        if post_id not in post_ids:
            post_ids.append(post_id)
        else:
            post_ids.remove(post_id)
        request.session["stored_posts"] = post_ids
        return HttpResponseRedirect(reverse("read-later"))
