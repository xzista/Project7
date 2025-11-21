from django.views.generic import ListView, CreateView
from .models import Review
from .forms import ReviewForm
from django.urls import reverse_lazy
from django.contrib import messages

class ReviewListView(ListView):
    model = Review
    template_name = "reviews/review_list.html"
    context_object_name = "reviews"
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.filter(is_published=True).order_by("-created_at")

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review_form.html"
    success_url = reverse_lazy("reviews:review_list")

    def form_valid(self, form):
        # по умолчанию отзывы требуют модерации: is_published=False
        response = super().form_valid(form)
        messages.success(self.request, "Спасибо! Ваш отзыв отправлен на модерацию.")
        return response