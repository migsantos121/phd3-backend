from ib_comments.models.comments import Comment
from ib_comments.models.user_comment_report import UserCommentReport
from ib_comments.models.user_comment_vote import UserCommentVote

def populate_comments ():
    comment1 = Comment(entity_id=1,entity_type="ib_comments.Comment",user_id=1,comment="This First Comment",multimedia_type='video',
                       multimedia_url='https://s3-ap-southeast-1.amazonaws.com/ibquizappdjango-beta/media/Warcraft+The+Beginning+Movie+Trailer+(2016)+-+Dolby+Digital+True+HD.mp4')
    comment1.save()
    comment2 = Comment(entity_id=1,entity_type="ib_comments.Comment",user_id=1,comment="This Second Comment",multimedia_type='video',
                       multimedia_url='https://s3-ap-southeast-1.amazonaws.com/ibquizappdjango-beta/media/Dolby+Digital+-+HD+Surround+Sound+Test.mp4')
    comment2.save()
    comment3 = Comment(entity_id=1,entity_type="ib_comments.Comment",user_id=1,comment="This Third Comment",multimedia_type='audio',
                       multimedia_url='https://s3-ap-southeast-1.amazonaws.com/ibquizappdjango-beta/media/AWS_Podcast_Epsiode_177.mp3')
    comment3.save()
    comment4 = Comment(entity_id=1,entity_type="ib_comments.Comment",user_id=1,comment="This Fourth Comment",multimedia_type='video',
                       multimedia_url='https://s3-ap-southeast-1.amazonaws.com/ibquizappdjango-beta/media/Warcraft+The+Beginning+Movie+Trailer+(2016)+-+Dolby+Digital+True+HD.mp4')
    comment4.save()
    comment5 = Comment(entity_id=1,entity_type="ib_comments.Comment",user_id=1,comment="This Fifth Comment",multimedia_type='video',
                       multimedia_url='https://s3-ap-southeast-1.amazonaws.com/ibquizappdjango-beta/media/Dolby+Atmos+Demo+2016+Sentimental+Feeling+TrueHD+7.1+Atmos.mp4')
    comment5.save()
    comment6 = Comment(entity_id=2,entity_type="ib_comments.Comment",user_id=1,comment="This 6th Comment",multimedia_type='video',
                       multimedia_url='https://s3-ap-southeast-1.amazonaws.com/ibquizappdjango-beta/media/Dolby+Digital+-+HD+Surround+Sound+Test.mp4')
    comment6.save()
    comment7 = Comment(entity_id=2,entity_type="ib_comments.Comment",user_id=1,comment="This 7th Comment",multimedia_type='audio',
                       multimedia_url='https://s3-ap-southeast-1.amazonaws.com/ibquizappdjango-beta/media/AWS_Podcast_Epsiode_177.mp3')
    comment7.save()
    comment8 = Comment(entity_id=2,entity_type="ib_comments.Comment",user_id=1,comment="This 8th Comment",multimedia_type='video',
                       multimedia_url='https://s3-ap-southeast-1.amazonaws.com/ibquizappdjango-beta/media/Dolby+Atmos+Demo+2016+Sentimental+Feeling+TrueHD+7.1+Atmos.mp4')
    comment8.save()
    comment9 = Comment(entity_id=2,entity_type="ib_comments.Comment",user_id=1,comment="This 9th Comment",multimedia_type='video',
                       multimedia_url='https://s3-ap-southeast-1.amazonaws.com/ibquizappdjango-beta/media/Dolby+Digital+-+HD+Surround+Sound+Test.mp4')
    comment9.save()
    comment10 = Comment(entity_id=2,entity_type="ib_comments.Comment",user_id=1,comment="This 10th Comment",multimedia_type='audio',
                       multimedia_url='https://s3-ap-southeast-1.amazonaws.com/ibquizappdjango-beta/media/AWS_Podcast_Epsiode_177.mp3')
    comment10.save()


def populate_usercommentvote():
    comment1 = Comment.objects.get(id=1)
    user_vote1 = UserCommentVote(comment=comment1,user_id =1, vote="UP_VOTE")
    user_vote1.save()
    comment2 = Comment.objects.get(id=2)
    user_vote2 = UserCommentVote(comment=comment2,user_id =1, vote="UP_VOTE")
    user_vote2.save()
    comment3 = Comment.objects.get(id=3)
    user_vote3 = UserCommentVote(comment=comment3,user_id =1, vote="UP_VOTE")
    user_vote3.save()
    comment4 = Comment.objects.get(id=4)
    user_vote4 = UserCommentVote(comment=comment4,user_id =1, vote="UP_VOTE")
    user_vote4.save()
    comment5 = Comment.objects.get(id=5)
    user_vote5 = UserCommentVote(comment=comment5,user_id =1, vote="UP_VOTE")
    user_vote5.save()
    comment6 = Comment.objects.get(id=6)
    user_vote6 = UserCommentVote(comment=comment6,user_id =1, vote="UP_VOTE")
    user_vote6.save()
    comment7 = Comment.objects.get(id=7)
    user_vote7 = UserCommentVote(comment=comment7,user_id =1, vote="UP_VOTE")
    user_vote7.save()
    comment8 = Comment.objects.get(id=8)
    user_vote8 = UserCommentVote(comment=comment8,user_id =1, vote="UP_VOTE")
    user_vote8.save()
    comment9 = Comment.objects.get(id=9)
    user_vote9 = UserCommentVote(comment=comment9,user_id =1, vote="UP_VOTE")
    user_vote9.save()
    comment10 = Comment.objects.get(id=10)
    user_vote10 = UserCommentVote(comment=comment10,user_id =1, vote="UP_VOTE")
    user_vote10.save()


def populate_comment_report():
    comment1 = Comment.objects.get(id=1)
    comment2 = Comment.objects.get(id=2)
    comment3 = Comment.objects.get(id=3)
    comment4 = Comment.objects.get(id=4)
    comment5 = Comment.objects.get(id=5)
    comment6 = Comment.objects.get(id=6)
    comment7 = Comment.objects.get(id=7)
    comment8 = Comment.objects.get(id=8)
    comment9 = Comment.objects.get(id=9)
    comment10 = Comment.objects.get(id=10)

    comment_report1 = UserCommentReport(comment=comment1,user_id =1)
    comment_report1.save()
    comment_report2 = UserCommentReport(comment=comment2,user_id =1)
    comment_report2.save()
    comment_report3 = UserCommentReport(comment=comment3,user_id =1)
    comment_report3.save()
    comment_report4 = UserCommentReport(comment=comment4,user_id =1)
    comment_report4.save()
    comment_report5 = UserCommentReport(comment=comment5,user_id =1)
    comment_report5.save()
    comment_report6 = UserCommentReport(comment=comment6,user_id =1)
    comment_report6.save()
    comment_report7 = UserCommentReport(comment=comment7,user_id =1)
    comment_report7.save()
    comment_report8 = UserCommentReport(comment=comment8,user_id =1)
    comment_report8.save()
    comment_report9 = UserCommentReport(comment=comment9,user_id =1)
    comment_report9.save()
    comment_report10 = UserCommentReport(comment=comment10,user_id =1)
    comment_report10.save()



