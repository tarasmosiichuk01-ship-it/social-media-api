from rest_framework import serializers

from social_media.models import Post, Comment, Hashtag, Like


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = ("id", "name")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "post", "content", "created_at")
        read_only_fields = ("created_at", "post")


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    likes = serializers.IntegerField(source="likes.count", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    hashtag_names = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "content",
            "image",
            "created_at",
            "likes",
            "comments",
            "hashtags",
            "hashtag_names",
            "scheduled_at",
            "is_published",
        )
        read_only_fields = ("created_at",)

    def create(self, validated_data):
        hashtag_names = validated_data.pop("hashtag_names", [])
        post = Post.objects.create(**validated_data)
        self._set_hashtags(post, hashtag_names)
        return post

    def update(self, instance, validated_data):
        hashtag_names = validated_data.pop("hashtag_names", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if hashtag_names is not None:
            self._set_hashtags(instance, hashtag_names)
        return instance

    def _set_hashtags(self, post, names):
        hashtags = []
        for name in names:
            hashtag, _ = Hashtag.objects.get_or_create(
                name=name.lower().strip()
            )
            hashtags.append(hashtag)
        post.hashtags.set(hashtags)


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    likes = serializers.IntegerField(source="likes.count", read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    comments = serializers.IntegerField(
        source="comments.count",
        read_only=True
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "content",
            "created_at",
            "likes",
            "comments",
            "hashtags",
        )


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ("id", "user", "post")
        read_only_fields = ("id", "user", "post")
