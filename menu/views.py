from django.views.generic import ListView, DetailView
from .models import Dish, MenuCategory
from django.db.models import Q

class DishListView(ListView):
    model = Dish
    template_name = "menu/dish_list.html"
    context_object_name = "dishes"
    paginate_by = 12

    def get_queryset(self):
        qs = Dish.objects.filter(is_available=True).select_related("category")
        q = self.request.GET.get("q")
        cat = self.request.GET.get("category")
        price_min = self.request.GET.get("price_min")
        price_max = self.request.GET.get("price_max")

        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        if cat:
            qs = qs.filter(category__id=cat)
        if price_min:
            try:
                qs = qs.filter(price__gte=float(price_min))
            except ValueError:
                pass
        if price_max:
            try:
                qs = qs.filter(price__lte=float(price_max))
            except ValueError:
                pass
        return qs.order_by("category__name", "name")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = MenuCategory.objects.all()
        ctx["q"] = self.request.GET.get("q", "")
        ctx["selected_category"] = self.request.GET.get("category", "")
        ctx["price_min"] = self.request.GET.get("price_min", "")
        ctx["price_max"] = self.request.GET.get("price_max", "")
        return ctx

class DishDetailView(DetailView):
    model = Dish
    template_name = "menu/dish_detail.html"
    context_object_name = "dish"