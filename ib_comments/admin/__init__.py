from ib_comments.models.comments import Comment
from ib_comments.models.user_comment_vote import UserCommentVote
from django.contrib import admin
from ib_comments.models.user_comment_report import UserCommentReport

admin.site.register(Comment)
admin.site.register(UserCommentVote)
admin.site.register(UserCommentReport)