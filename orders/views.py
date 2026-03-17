from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import response
from django.utils import timezone
from .models import Coupon
from rest_framework import status
# Create your views here.

class CouponValidationView(APIView):
    def post(self,request):
        code= request.data.get('code')
        if not code:
            return Response(
                {"error": "Coupon code is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExit:
            return Response(
                {"error":"Invalid coupon code"},
                status=status.HTTP_400_BAD_REQUEST
            )
        today = timezone.now().date()
        if not coupon.is_active:
            return Response(
                {"error":"Coupon is inactive"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if coupon.valid_form > today or coupon.valid_until < today:
            return Response(
                {"error":"Coupon is expired or not yet valid"},
                status=status.HTTP_400_BAD_REQUEST
            )
        RETURN Response(
            {
                "message":"Coupon is valid",
                "discount_percentage":coupon.discount_percentage
            },
            status=status.HTTP_200_OK
        )
