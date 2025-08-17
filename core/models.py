from django.db import models
from django.contrib.auth.models import User
class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    def __str__(self):
        return f"r/{self.name}"
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
class Post(models.Model):
    def vote(self,username, direction):
        prev_vote = self.votedby.get(username)
        if prev_vote == direction:
            if prev_vote == "up":
                self.votes -= 1
            elif prev_vote == "down":
                self.votes += 1
            self.votedby[username] = None
        else:
            if prev_vote == None:
                if direction == "up":
                    self.votes += 1
                elif direction == "down":
                    self.votes -= 1
            else:
                if direction == "up":
                    self.votes += 2
                elif direction == "down":
                    self.votes -= 2
            self.votedby[username] = direction
        self.save()
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE,related_name="posts" )
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
    votedby = models.JSONField(default=dict)
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('post', 'user', 'content') 
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"