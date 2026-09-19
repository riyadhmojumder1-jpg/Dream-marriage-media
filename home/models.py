from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# =========================================================
# MEMBER MODEL
# =========================================================

class Member(models.Model):

    # -----------------------------------------------------
    # GENDER
    # -----------------------------------------------------

    GENDER_CHOICES = [
        ("male", "পাত্র"),
        ("female", "পাত্রী"),
    ]


    # -----------------------------------------------------
    # VERIFICATION STATUS
    # -----------------------------------------------------

    VERIFICATION_STATUS_CHOICES = [
        ("pending", "যাচাই অপেক্ষমাণ"),
        ("verified", "যাচাইকৃত"),
        ("rejected", "বাতিল"),
        ("blocked", "ব্লক করা হয়েছে"),
    ]


    # -----------------------------------------------------
    # USER ACCOUNT
    # -----------------------------------------------------

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="member_profile"
    )


    # -----------------------------------------------------
    # BASIC INFORMATION
    # -----------------------------------------------------

    first_name = models.CharField(
        max_length=100
    )


    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )


    age = models.PositiveIntegerField()


    district = models.CharField(
        max_length=100
    )


    # -----------------------------------------------------
    # MOBILE NUMBER
    # -----------------------------------------------------

    phone = models.CharField(
        max_length=20,
        unique=True
    )


    # -----------------------------------------------------
    # ADMIN VERIFICATION
    # -----------------------------------------------------

    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default="pending"
    )


    # -----------------------------------------------------
    # CREATED DATE
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    # -----------------------------------------------------
    # DISPLAY NAME
    # -----------------------------------------------------

    def __str__(self):
        return self.first_name


    # -----------------------------------------------------
    # HELPER: VERIFIED?
    # -----------------------------------------------------

    def is_verified(self):
        return self.verification_status == "verified"


    # -----------------------------------------------------
    # HELPER: BLOCKED?
    # -----------------------------------------------------

    def is_blocked(self):
        return self.verification_status == "blocked"


    # -----------------------------------------------------
    # HELPER: PENDING?
    # -----------------------------------------------------

    def is_pending(self):
        return self.verification_status == "pending"


    # -----------------------------------------------------
    # HELPER: REJECTED?
    # -----------------------------------------------------

    def is_rejected(self):
        return self.verification_status == "rejected"



# =========================================================
# MEMBERSHIP MODEL
# =========================================================

class Membership(models.Model):

    # -----------------------------------------------------
    # PAYMENT STATUS
    # -----------------------------------------------------

    PAYMENT_STATUS_CHOICES = [
        ("pending", "অপেক্ষমাণ"),
        ("approved", "অনুমোদিত"),
        ("rejected", "বাতিল"),
    ]


    # -----------------------------------------------------
    # MEMBER
    # -----------------------------------------------------

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="memberships"
    )


    # -----------------------------------------------------
    # PAYMENT AMOUNT
    # -----------------------------------------------------

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=500
    )


    # -----------------------------------------------------
    # PAYMENT METHOD
    # -----------------------------------------------------

    payment_method = models.CharField(
        max_length=20,
        blank=True
    )


    # -----------------------------------------------------
    # TRANSACTION ID
    # -----------------------------------------------------

    transaction_id = models.CharField(
        max_length=100,
        blank=True
    )


    # -----------------------------------------------------
    # PAYMENT STATUS
    # -----------------------------------------------------

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )


    # -----------------------------------------------------
    # MEMBERSHIP START
    # -----------------------------------------------------

    start_date = models.DateTimeField(
        null=True,
        blank=True
    )


    # -----------------------------------------------------
    # MEMBERSHIP END
    # -----------------------------------------------------

    end_date = models.DateTimeField(
        null=True,
        blank=True
    )


    # -----------------------------------------------------
    # CREATED DATE
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    # -----------------------------------------------------
    # CHECK ACTIVE MEMBERSHIP
    # -----------------------------------------------------

    def is_active(self):

        if (
            self.payment_status == "approved"
            and self.start_date
            and self.end_date
            and self.end_date > timezone.now()
        ):
            return True

        return False


    # -----------------------------------------------------
    # APPROVE PAYMENT
    # -----------------------------------------------------

    def approve_payment(self):

        self.payment_status = "approved"

        self.start_date = timezone.now()

        self.end_date = (
            timezone.now()
            + timedelta(days=7)
        )

        self.save(
            update_fields=[
                "payment_status",
                "start_date",
                "end_date",
            ]
        )


    # -----------------------------------------------------
    # REJECT PAYMENT
    # -----------------------------------------------------

    def reject_payment(self):

        self.payment_status = "rejected"

        self.save(
            update_fields=[
                "payment_status",
            ]
        )


    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    def __str__(self):

        return (
            f"{self.member.first_name} - "
            f"{self.amount} টাকা"
        )