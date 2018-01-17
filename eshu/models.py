from sqlalchemy.orm import relationship
from . import db


class Activity:
    pass


class Interaction(Activity):
    pass


class Account(db.Model):
    __tablename__ = 'account'

    account_id = db.Column(db.BigInteger(), primary_key=True)
    username = db.Column(db.Unicode(), nullable=False)
    domain = db.Column(db.Unicode(), nullable=True)

    # keypair
    private_key = db.Column(db.Text(), nullable=False)
    public_key = db.Column(db.Text(), nullable=False)

    # websub/ostatus stuff, not yet implemented
    atom_url = db.Column(db.Unicode(), nullable=True)
    salmon_url = db.Column(db.Unicode(), nullable=True)
    websub_secret = db.Column(db.Unicode(), nullable=True)
    websub_hub_url = db.Column(db.Unicode(), nullable=True)
    websub_deadline_ts = db.Column(db.DateTime(True), nullable=True)

    # activitypub endpoints
    inbox_url = db.Column(db.Unicode(), nullable=True)
    shared_inbox_url = db.Column(db.Unicode(), nullable=True)
    outbox_url = db.Column(db.Unicode(), nullable=True)

    # attributes
    display_name = db.Column(db.Unicode(), nullable=True)
    biography = db.Column(db.Text(), nullable=True)
    website_url = db.Column(db.Unicode(), nullable=True)
    avatar_url = db.Column(db.Unicode(), nullable=True)
    header_url = db.Column(db.Unicode(), nullable=True)

    # metrics
    last_webfinger_ts = db.Column(db.DateTime(True), nullable=True)

    @property
    def is_local(self):
        return self.domain == None


class Attachment(db.Model):
    __tablename__ = 'attachment'

    attachment_id = db.Column(db.BigInteger(), primary_key=True)
    attachment_uuid = db.Column(db.Unicode(), unique=True, nullable=False)
    account_id = db.Column(db.BigInteger(), db.ForeignKey('account.account_id'))
    account = relationship("Account", cascade="all, delete-orphan")
    uri = db.Column(db.Unicode(), nullable=False)


class Conversation(db.Model):
    __tablename__ = 'conversation'

    conversation_id = db.Column(db.BigInteger(), primary_key=True)
    creation_ts = db.Column(db.DateTime(True), nullable=False)
    updated_ts = db.Column(db.DateTime(True), nullable=False)


class Follow(Interaction, db.Model):
    __tablename__ = 'follow'
    __parent_verb__ = 'Follow'

    referent_id = db.Column(db.BigInteger(), primary_key=True)
    referent_ts = db.Column(db.DateTime(True), nullable=False)
    account_id = db.Column(db.BigInteger(), db.ForeignKey('account.account_id'), nullable=False)
    target_account_id = db.Column(db.BigInteger(), db.ForeignKey('account.account_id'), nullable=False)

    account = relationship("Account", foreign_keys=[account_id], cascade="all, delete-orphan",
                              back_populates="follows")
    target_account = relationship("Account", foreign_keys=[target_account_id], cascade="all, delete-orphan",
                              back_populates="followers")


class Block(Interaction, db.Model):
    __tablename__ = 'block'
    __parent_verb__ = 'Block'

    referent_id = db.Column(db.BigInteger(), primary_key=True)
    referent_ts = db.Column(db.DateTime(True), nullable=False)
    account_id = db.Column(db.BigInteger(), db.ForeignKey('account.account_id'), nullable=False)
    target_account_id = db.Column(db.BigInteger(), db.ForeignKey('account.account_id'), nullable=False)

    account = relationship("Account", foreign_keys=[account_id], cascade="all, delete-orphan",
                              back_populates="blocks")
    target_account = relationship("Account", foreign_keys=[target_account_id], cascade="all, delete-orphan",
                              back_populates="blocked_by")


class Note(Activity, db.Model):
    __tablename__ = 'note'
    __parent_verb__ = 'Create'
    __child_verb__ = 'Note'

    note_id = db.Column(db.BigInteger(), primary_key=True)
    note_uuid = db.Column(db.Unicode(), unique=True, nullable=False)
    note_ts = db.Column(db.DateTime(), nullable=False)

    account_id = db.Column(db.BigInteger(), db.ForeignKey('account.account_id'), nullable=False)
    summary = db.Column(db.Unicode(), nullable=True)
    content = db.Column(db.Text(), nullable=False)
    sensitive = db.Column(db.Boolean(), default=False, nullable=False)


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.BigInteger(), primary_key=True)
    account_id = db.Column(db.BigInteger(), db.ForeignKey('account.account_id'), nullable=False)
    passphrase = db.Column(db.Unicode(), nullable=False)

    account = relationship("Account")
