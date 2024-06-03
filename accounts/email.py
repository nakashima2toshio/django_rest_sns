# email.py
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from templated_mail.mail import BaseEmailMessage
from django.conf import settings


class EmailManager(BaseEmailMessage):
    def send(self, to, cc=None, bcc=None, reply_to=None, from_email=None, *args, **kwargs):
        if reply_to is None:
            reply_to = []
        if cc is None:
            cc = []
        if bcc is None:
            bcc = []
        self.render()
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.reply_to = reply_to
        self.from_email = from_email or 'XXXアプリケーション <' + settings.DEFAULT_FROM_EMAIL + '>'
        super(BaseEmailMessage, self).send(*args, **kwargs)


class ActivationEmail(EmailManager):
    template_name = 'accounts/activation.html'

    def get_context_data(self):
        # context = super().get_context_data()
        context = super(ActivationEmail, self).get_context_data()
        user = context.get("user")
        if user:
            context["name"] = user.name
            context["uid"] = utils.encode_uid(user.pk)
            context["token"] = default_token_generator.make_token(user)
            context["url"] = settings.DJOSER["ACTIVATION_URL"].format(**context)
        return context


class ConfirmationEmail(EmailManager):
    template_name = 'accounts/confirmation.html'

    def get_context_data(self):
        # context = super().get_context_data()
        context = super(ConfirmationEmail, self).get_context_data()
        user = context.get("user")
        if user:
            context["name"] = user.name
        return context


class PasswordResetEmail(EmailManager):
    template_name = 'accounts/password_reset.html'

    def get_context_data(self):
        # context = super().get_context_data()
        context = super(PasswordResetEmail, self).get_context_data()
        user = context.get("user")
        if user:
            context["name"] = user.name
            context["uid"] = utils.encode_uid(user.pk)
            context["token"] = default_token_generator.make_token(user)
            context["url"] = settings.DJOSER["PASSWORD_RESET_CONFIRM_URL"].format(**context)
        return context


class PasswordChangedConfirmationEmail(EmailManager):
    template_name = 'accounts/password_changed_confirmation.html'

    def get_context_data(self):
        # context = super().get_context_data()
        context = super(PasswordChangedConfirmationEmail, self).get_context_data()
        user = context.get("user")
        if user:
            context["name"] = user.name
        return context


class UsernameResetEmail(EmailManager):
    template_name = 'accounts/username_reset.html'

    def get_context_data(self):
        # context = super().get_context_data()
        context = super(UsernameResetEmail, self).get_context_data()
        user = context.get("user")
        if user:
            context["name"] = user.name
            context["uid"] = utils.encode_uid(user.pk)
            context["token"] = default_token_generator.make_token(user)
            context["url"] = settings.DJOSER["USERNAME_RESET_CONFIRM_URL"].format(**context)
        return context


class UsernameChangedConfirmationEmail(EmailManager):
    template_name = 'accounts/username_changed_confirmation.html'

    def get_context_data(self):
        context = super(UsernameChangedConfirmationEmail, self).get_context_data()
        user = context.get("user")
        if user:
            context["name"] = user.name
        return context
