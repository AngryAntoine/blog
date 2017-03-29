from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField
)

from accounts.api.serializers import UserDetailSerializer
from comments.api.serializers import CommentSerializer
from comments.models import Comment
from blog.models import Post


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish'
        ]


post_detail_url = HyperlinkedIdentityField(
        view_name='blog-api:detail',
        lookup_field='slug'
    )


class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)


    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'title',
            'content',
            'publish',
        ]
    #
    # def get_user(self, obj):
    #     return str(obj.user.username)


class PostDetailSerializer(ModelSerializer):
    # url = post_detail_url
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'user',
            'slug',
            'content',
            'html',
            'image',
            'publish',
            'comments'
        ]

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_html(self, obj):
        return obj.get_markdown()
    #
    # def get_user(self, obj):
    #     return str(obj.user.username)

    def get_comments(self, obj):
        content_type = obj.get_content_type
        object_id = obj.id
        c_qs = Comment.objects.filter_by_instance(obj)  # comments_queryset
        comments = CommentSerializer(c_qs, many=True).data
        return comments