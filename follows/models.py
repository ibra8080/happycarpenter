from django.db import models
from django.contrib.auth.models import User

class Follow(models.Model):
    owner = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'followed']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(owner=models.F('followed')),
                name='prevent_self_follow'
            )
        ]

    def __str__(self):
        return f"{self.owner} follows {self.followed}"
