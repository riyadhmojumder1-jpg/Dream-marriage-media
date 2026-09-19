from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Member


# =========================================================
# HOME PAGE
# =========================================================

def home(request):

    return render(
        request,
        "home.html"
    )


# =========================================================
# SIGNUP / REGISTRATION
# =========================================================

def signup(request):

    if request.method == "POST":

        # -------------------------------------------------
        # FORM DATA
        # -------------------------------------------------

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        gender = request.POST.get(
            "gender",
            ""
        ).strip()

        age = request.POST.get(
            "age",
            ""
        ).strip()

        district = request.POST.get(
            "district",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        password2 = request.POST.get(
            "password2",
            ""
        )

        terms = request.POST.get(
            "terms"
        )


        # =================================================
        # EMPTY FIELD CHECK
        # =================================================

        if (
            not first_name
            or not gender
            or not age
            or not district
            or not email
            or not phone
            or not password
            or not password2
        ):

            messages.error(
                request,
                "সব প্রয়োজনীয় তথ্য পূরণ করুন।"
            )

            return render(
                request,
                "signup.html"
            )


        # =================================================
        # TERMS CHECK
        # =================================================

        if not terms:

            messages.error(
                request,
                "রেজিস্ট্রেশনের আগে শর্তাবলী মেনে নিতে হবে।"
            )

            return render(
                request,
                "signup.html"
            )


        # =================================================
        # AGE VALIDATION
        # =================================================

        try:

            age = int(age)

        except ValueError:

            messages.error(
                request,
                "বয়স সঠিকভাবে লিখুন।"
            )

            return render(
                request,
                "signup.html"
            )


        if age < 18 or age > 100:

            messages.error(
                request,
                "বয়স অবশ্যই ১৮ থেকে ১০০ বছরের মধ্যে হতে হবে।"
            )

            return render(
                request,
                "signup.html"
            )


        # =================================================
        # GENDER VALIDATION
        # =================================================

        if gender not in ["male", "female"]:

            messages.error(
                request,
                "সঠিক লিঙ্গ নির্বাচন করুন।"
            )

            return render(
                request,
                "signup.html"
            )


        # =================================================
        # PASSWORD MATCH
        # =================================================

        if password != password2:

            messages.error(
                request,
                "দুইটি পাসওয়ার্ড একই নয়।"
            )

            return render(
                request,
                "signup.html"
            )


        # =================================================
        # PASSWORD LENGTH
        # =================================================

        if len(password) < 8:

            messages.error(
                request,
                "পাসওয়ার্ড কমপক্ষে ৮ অক্ষরের হতে হবে।"
            )

            return render(
                request,
                "signup.html"
            )


        # =================================================
        # EMAIL ALREADY EXISTS
        # =================================================

        if User.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                "এই ইমেইল দিয়ে ইতিমধ্যে একটি অ্যাকাউন্ট রয়েছে।"
            )

            return render(
                request,
                "signup.html"
            )


        # =================================================
        # PHONE ALREADY EXISTS
        # =================================================

        if Member.objects.filter(
            phone=phone
        ).exists():

            messages.error(
                request,
                "এই মোবাইল নম্বর দিয়ে ইতিমধ্যে একটি অ্যাকাউন্ট রয়েছে।"
            )

            return render(
                request,
                "signup.html"
            )


        # =================================================
        # CREATE USERNAME
        # =================================================

        username = email


        # =================================================
        # USERNAME CHECK
        # =================================================

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "এই ইমেইল দিয়ে Username ইতিমধ্যে ব্যবহার করা হয়েছে।"
            )

            return render(
                request,
                "signup.html"
            )


        # =================================================
        # CREATE DJANGO USER
        # =================================================

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )


        # =================================================
        # SAVE FIRST NAME
        # =================================================

        user.first_name = first_name

        user.save()


        # =================================================
        # CREATE MEMBER PROFILE
        # =================================================

        Member.objects.create(
            user=user,
            first_name=first_name,
            gender=gender,
            age=age,
            district=district,
            phone=phone,
            verification_status="pending"
        )


        # =================================================
        # SUCCESS MESSAGE
        # =================================================

        messages.success(
            request,
            "আপনার Registration সফল হয়েছে। "
            "Admin আপনার প্রোফাইল যাচাই করার পর "
            "আপনি Login করতে পারবেন।"
        )


        # =================================================
        # REDIRECT LOGIN
        # =================================================

        return redirect("login")


    # =====================================================
    # GET REQUEST
    # =====================================================

    return render(
        request,
        "signup.html"
    )


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.method == "POST":

        # -------------------------------------------------
        # LOGIN INPUT
        # -------------------------------------------------

        login_input = request.POST.get(
            "email",
            ""
        ).strip().lower()

        password = request.POST.get(
            "password",
            ""
        )


        # =================================================
        # EMPTY FIELD CHECK
        # =================================================

        if not login_input or not password:

            messages.error(
                request,
                "ইমেইল / মোবাইল নম্বর এবং পাসওয়ার্ড দিন।"
            )

            return render(
                request,
                "login.html"
            )


        # =================================================
        # 1. USERNAME LOGIN
        # =================================================

        user = authenticate(
            request,
            username=login_input,
            password=password
        )


        # =================================================
        # 2. EMAIL LOGIN
        # =================================================

        if user is None:

            member_user = User.objects.filter(
                email__iexact=login_input
            ).first()

            if member_user:

                user = authenticate(
                    request,
                    username=member_user.username,
                    password=password
                )


        # =================================================
        # 3. MOBILE LOGIN
        # =================================================

        if user is None:

            member = Member.objects.select_related(
                "user"
            ).filter(
                phone=login_input
            ).first()

            if member:

                user = authenticate(
                    request,
                    username=member.user.username,
                    password=password
                )


        # =================================================
        # WRONG LOGIN
        # =================================================

        if user is None:

            messages.error(
                request,
                "ইমেইল / মোবাইল নম্বর অথবা পাসওয়ার্ড সঠিক নয়।"
            )

            return render(
                request,
                "login.html"
            )


        # =================================================
        # ADMIN / SUPERUSER
        # =================================================

        if user.is_superuser:

            login(
                request,
                user
            )

            messages.success(
                request,
                "Admin Panel-এ স্বাগতম।"
            )

            return redirect("/admin/")


        # =================================================
        # MEMBER PROFILE
        # =================================================

        member = Member.objects.filter(
            user=user
        ).first()


        if member is None:

            messages.error(
                request,
                "আপনার Member profile পাওয়া যায়নি।"
            )

            return render(
                request,
                "login.html"
            )


        # =================================================
        # PENDING
        # =================================================

        if member.verification_status == "pending":

            messages.warning(
                request,
                "আপনার প্রোফাইল এখনো Admin যাচাই করেননি। "
                "অনুগ্রহ করে অপেক্ষা করুন।"
            )

            return render(
                request,
                "login.html"
            )


        # =================================================
        # REJECTED
        # =================================================

        if member.verification_status == "rejected":

            messages.error(
                request,
                "আপনার প্রোফাইল Admin কর্তৃক বাতিল করা হয়েছে।"
            )

            return render(
                request,
                "login.html"
            )


        # =================================================
        # BLOCKED
        # =================================================

        if member.verification_status == "blocked":

            messages.error(
                request,
                "আপনার অ্যাকাউন্ট ব্লক করা হয়েছে।"
            )

            return render(
                request,
                "login.html"
            )


        # =================================================
        # VERIFIED
        # =================================================

        if member.verification_status == "verified":

            login(
                request,
                user
            )

            messages.success(
                request,
                f"স্বাগতম, {member.first_name}!"
            )

            return redirect("home")


        # =================================================
        # UNKNOWN STATUS
        # =================================================

        messages.error(
            request,
            "আপনার অ্যাকাউন্টের verification status সঠিক নয়।"
        )

        return render(
            request,
            "login.html"
        )


    # =====================================================
    # GET REQUEST
    # =====================================================

    return render(
        request,
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "আপনি সফলভাবে Logout করেছেন।"
    )

    return redirect("home")