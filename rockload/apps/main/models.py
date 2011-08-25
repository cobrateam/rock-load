#!/usr/bin/python
# -*- coding: utf-8 -*-

from mongoengine import Document, StringField, ReferenceField, URLField, DateTimeField

from rockload.apps.auth.models import User

class Project(Document):
    owner = ReferenceField(User, required=True)
    created_at = DateTimeField(required=True)
    name = StringField(required=True, unique=True)
    git_repo = URLField(verify_exists=True, required=True)

    @classmethod
    def get_projects_for_user(cls, user):
        return cls.objects(owner=user).all()
