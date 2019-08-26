# 导包
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from indexapp.models import Mycart
from cartapp.car import Car

# 渲染购物车
def cart(request):
    username = request.session.get("login")
    car = None
    if username:
        carts = Mycart.objects.filter(book_status=username)
        car = Car()
        if carts:
            for index in carts:
                car.add_car(index.book_id,index.book_count)
    else:
        car = request.session.get("car")
        if not car:
            car = Car()
    request.session['car'] =car
    return render(request,"car.html",{"car":car,"username":username})

#  添加购物车
def addcart(request):
    username = request.session.get("login")
    bookid = int(request.GET.get("bookid"))
    number = int(request.GET.get("booknumber",1))
    if not username:
        try:
            car = request.session.get("car")
            if car:
                car.add_car(bookid,number)
            else:
                car = Car()
                car.add_car(bookid,number)
            request.session["car"] = car
            return HttpResponse(1)
        except:
            return HttpResponse(0)
    else :
        try:
            cart_item = Mycart.objects.filter(book_id=bookid)
            if cart_item:
                cart_item[0].book_count += number
            else:
                Mycart.objects.create(book_id=bookid,book_count=number,book_status=username)
            return HttpResponse(1)
        except:
            return HttpResponse(0)

# 删除购物车
def deletecart(request):
    username = request.session.get("login")
    bookid = request.GET.get("bookid")
    car = request.session.get("car")
    if username:
        ucar = Mycart.objects.filter(book_status=username,book_id=bookid)[0]
        ucar.delete()
    elif car:
        car.delete_item(bookid)
        request.session["car"] = car
    return redirect("cartapp:cart")

# 改变尚品数量
def change_cart(request):
    username = request.session.get("login")
    bookid = request.GET.get("bookid")
    number = request.GET.get("booknumber")
    car = request.session.get("car")
    if username:
        book = Mycart.objects.filter(book_status=username,book_id=bookid)[0]
        book.book_count = number
        book.save()
        carts =  Mycart.objects.filter(book_status=username)
        car = Car()
        for index in carts:
            car.add_car(index.book_id, index.book_count)
        return JsonResponse({'price_total': car.total_price, 'price_save': car.save_price})
    elif car:
        car.change_item(bookid,number)
        request.session["car"] = car
        return JsonResponse({'price_total':car.total_price,'price_save':car.save_price})