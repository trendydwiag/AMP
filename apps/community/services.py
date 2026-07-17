import logging
from typing import Optional, List
from django.db import transaction
from django.db.models import F
from utils.services import BaseService
from .repositories import DiscussionRepository, ReplyRepository
from .models import Discussion, Reply

logger = logging.getLogger('community')


class DiscussionService(BaseService[DiscussionRepository]):
    def __init__(self):
        super().__init__(DiscussionRepository())

    def get_recent_discussions(self, limit: int = 20):
        return DiscussionRepository().get_recent(limit)

    def get_pinned_discussions(self):
        return DiscussionRepository().get_pinned()

    def get_by_category(self, category: str):
        return DiscussionRepository().get_by_category(category)

    def get_by_slug(self, slug: str) -> Optional[Discussion]:
        return DiscussionRepository().get_by_slug(slug)

    def search_discussions(self, query: str):
        return DiscussionRepository().search(query)

    @transaction.atomic
    def create_discussion(self, **kwargs) -> Discussion:
        return self.repository.create(**kwargs)

    @transaction.atomic
    def update_discussion(self, discussion_id, **kwargs) -> Optional[Discussion]:
        discussion = self.repository.get_by_id(discussion_id)
        if discussion:
            return self.repository.update(discussion, **kwargs)
        return None

    @transaction.atomic
    def delete_discussion(self, discussion_id) -> bool:
        discussion = self.repository.get_by_id(discussion_id)
        if discussion:
            return self.repository.delete(discussion)
        return False

    @transaction.atomic
    def toggle_pinned(self, discussion_id) -> Optional[Discussion]:
        discussion = self.repository.get_by_id(discussion_id)
        if discussion:
            discussion.is_pinned = not discussion.is_pinned
            discussion.save(update_fields=['is_pinned'])
            return discussion
        return None

    @transaction.atomic
    def toggle_locked(self, discussion_id) -> Optional[Discussion]:
        discussion = self.repository.get_by_id(discussion_id)
        if discussion:
            discussion.is_locked = not discussion.is_locked
            discussion.save(update_fields=['is_locked'])
            return discussion
        return None

    @transaction.atomic
    def increment_views(self, discussion_id) -> Optional[Discussion]:
        return DiscussionRepository().increment_views(discussion_id)

    @transaction.atomic
    def increment_replies(self, discussion_id) -> Optional[Discussion]:
        return DiscussionRepository().increment_replies(discussion_id)


class ReplyService(BaseService[ReplyRepository]):
    def __init__(self):
        super().__init__(ReplyRepository())

    def get_for_discussion(self, discussion_id):
        return ReplyRepository().get_for_discussion(discussion_id)

    @transaction.atomic
    def create_reply(self, discussion_id, **kwargs) -> Optional[Reply]:
        discussion = Discussion.objects.filter(pk=discussion_id).first()
        if not discussion:
            return None
        if discussion.is_locked:
            return None
        reply = self.repository.create(discussion=discussion, **kwargs)
        Discussion.objects.filter(pk=discussion_id).update(reply_count=F('reply_count') + 1)
        return reply

    @transaction.atomic
    def update_reply(self, reply_id, **kwargs) -> Optional[Reply]:
        reply = self.repository.get_by_id(reply_id)
        if reply:
            return self.repository.update(reply, **kwargs)
        return None

    @transaction.atomic
    def delete_reply(self, reply_id) -> bool:
        reply = self.repository.get_by_id(reply_id)
        if reply:
            discussion_id = reply.discussion_id
            deleted = self.repository.delete(reply)
            if deleted:
                Discussion.objects.filter(pk=discussion_id).update(reply_count=F('reply_count') - 1)
            return deleted
        return False
