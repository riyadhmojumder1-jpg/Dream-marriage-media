from django.contrib import admin
from .models import Member, Membership


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    list_display = (
        "first_name",
        "gender",
        "age",
        "district",
        "phone",
        "verification_status",
        "created_at",
    )

    list_filter = (
        "verification_status",
        "gender",
    )

    search_fields = (
        "first_name",
        "phone",
        "user__email",
    )

    list_editable = (
        "verification_status",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):

    list_display = (
        "member",
        "amount",
        "payment_method",
        "transaction_id",
        "payment_status",
        "start_date",
        "end_date",
        "created_at",
    )

    list_filter = (
        "payment_status",
        "payment_method",
    )

    search_fields = (
        "member__first_name",
        "member__phone",
        "transaction_id",
    )

    ordering = (
        "-created_at",
    )