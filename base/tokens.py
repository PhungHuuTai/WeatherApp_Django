from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailConfirmationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, subscription, timestamp):
        return (
            str(subscription.pk) + str(timestamp) + str(subscription.is_confirmed)
        )

token_generator = EmailConfirmationTokenGenerator()