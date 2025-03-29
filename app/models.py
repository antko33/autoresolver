from typing import ClassVar

from tortoise import fields, models


class User(models.Model):
    id = fields.IntField(primary_key=True)
    tg_id = fields.CharField(max_length=64, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    domains: ClassVar[fields.ReverseRelation["Domain"]]
    files: ClassVar[fields.ReverseRelation["RoutingFile"]]


class Domain(models.Model):
    id = fields.IntField(primary_key=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="domains"
    )
    domain = fields.CharField(max_length=255)
    added_at = fields.DatetimeField(auto_now_add=True)
    enabled = fields.BooleanField(default=True)

    resolves: ClassVar[fields.ReverseRelation["Resolve"]]


class Resolve(models.Model):
    id = fields.IntField(primary_key=True)
    domain: fields.ForeignKeyRelation[Domain] = fields.ForeignKeyField(
        "models.Domain", related_name="resolves"
    )
    ip = fields.CharField(max_length=64)
    resolved_at = fields.DatetimeField(auto_now_add=True)
    source = fields.CharField(max_length=128, null=True)


class RoutingFile(models.Model):
    id = fields.IntField(primary_key=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="files"
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    filepath = fields.CharField(max_length=255)
    note = fields.TextField(null=True)
