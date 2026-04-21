from celery import shared_task


@shared_task
def create_scheduled_post(post_id: int) -> str:
    from social_media.models import Post

    try:
        post = Post.objects.get(id=post_id)
        if not post.is_published:
            post.is_published = True
            post.save()
        return f"Post {post_id} published successfully"
    except Post.DoesNotExist:
        return f"Post {post_id} not found"
