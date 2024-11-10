from django.urls import path
from .views import index,FAQFeedbackView, FAQListCreateView, FAQCategoryListView,DestroyFAQView,UpdateFAQView,RetrieveFAQView,CategoryListCreateView,DestroyCategoryView,UpdateCategoryView,RetrieveCategoryView,FeedbackListCreateView,DestroyFeedbackView,UpdateFeedbackView


urlpatterns = [
    path('', index, name='index'),
    path('category/',CategoryListCreateView.as_view(), name='category-list-create'),
    path('category/<int:pk>/', RetrieveCategoryView.as_view(), name='category-retrieve'),
    path('category/update/<int:pk>/', UpdateCategoryView.as_view(), name='category-update'),
    path('category/delete/<int:pk>/', DestroyCategoryView.as_view(), name='category-delete'),
    
    
    path('', FAQListCreateView.as_view(), name='faq-list-create'),
    path('<int:pk>/', RetrieveFAQView.as_view(), name='faq-retrieve'),
    path('update/<int:pk>/', UpdateFAQView.as_view(), name='faq-update'),
    path('delete/<int:pk>/', DestroyFAQView.as_view(), name='faq-delete'),
    
    path('category/<str:category>/faqs/', FAQCategoryListView.as_view(), name='faq-category-list'),
    
    path('feedback/', FeedbackListCreateView.as_view(), name='feedback-list-create'),  
    path('<int:pk>/feedbacks/',FAQFeedbackView.as_view(), name='feedback-retrieve'),
    path('feedback/delete/<int:pk>/', DestroyFeedbackView.as_view(), name='feedback-delete'),
    path('feedback/update/<int:pk>/', UpdateFeedbackView.as_view(), name='feedback-update'),
]
