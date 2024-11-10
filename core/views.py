from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics,status
from rest_framework.response import Response
from .models import CategoryFAQ, FAQ,Feedback, TagFAQ
from .serializers import CategoryFAQSerializer, FAQSerializer, FeedbackSerializer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from collections import Counter
import string
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render

# Create a view to display the template
def index(request):
    return render(request,'index.html')


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = CategoryFAQ.objects.all()
    serializer_class = CategoryFAQSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RetrieveCategoryView(generics.RetrieveAPIView):
    queryset = CategoryFAQ.objects.all()
    serializer_class = CategoryFAQSerializer
    

class UpdateCategoryView(generics.UpdateAPIView):
    queryset = CategoryFAQ.objects.all()
    serializer_class = CategoryFAQSerializer
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        category = CategoryFAQ.objects.get(id=pk)
        serializer = self.get_serializer(category, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({ "success": True, "message": "updated category" })
        else:
            print(serializer.errors)
            return Response({ "success": False, "message": "error updating category" })
        
class DestroyCategoryView(generics.DestroyAPIView):
    queryset = CategoryFAQ.objects.all()
    serializer_class = CategoryFAQSerializer
    def delete(self, request, *args, **kwargs):
        
        try:
            pk = kwargs.get("pk")
            category = CategoryFAQ.objects.get(id=pk)
            self.perform_destroy(category)
            return Response({ "success": True, "message": "category deleted" })
        except ObjectDoesNotExist:
            return Response({ "success": False, "message": "category does not exist" })

def get_tags(question):
    tokens = word_tokenize(question.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word.lower() not in stop_words]
    tagged_tokens = pos_tag(filtered_tokens)
    tags = [word for word, pos in tagged_tokens if pos.startswith("NN") or pos.startswith("JJ")]
    return tags[:5]

class FAQListCreateView(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        faq = serializer.save()
        self.perform_create(serializer)
        if serializer.validated_data.get('category'):
            category = serializer.validated_data['category']
            category.FAQ_count = category.faqs.count()
            category.save()
            faq = serializer.save()
        question=faq.question
        tags = get_tags(question)
        for tag in tags:
            try:
                tag, created = TagFAQ.objects.get_or_create(Tags=tag)
                faq.Tags.add(tag)
            except IntegrityError:
                tag = TagFAQ.objects.get(Tags=tag)
                faq.tags.add(tag)
        faq.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)          


     

class RetrieveFAQView(generics.RetrieveAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

class UpdateFAQView(generics.UpdateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        faq = FAQ.objects.get(id=pk)
        old_category = faq.category
        serializer = self.get_serializer(faq, data=request.data, partial=True)
        if serializer.is_valid():
            updated_faq=serializer.save()
            new_category = updated_faq.category
        if old_category != new_category:
            if old_category:
                old_category.FAQ_count = max(0, old_category.FAQ_count - 1)  
                old_category.save()
            if new_category:
                new_category.FAQ_count += 1
                new_category.save()
            return Response({ "success": True, "message": "updated FAQ" })
        else:
            print(serializer.errors)
            return Response({ "success": False, "message": "error updating FAQ" })

class DestroyFAQView(generics.DestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    def delete(self, request, *args, **kwargs):
        try:
            pk = kwargs.get("pk")
            faq = FAQ.objects.get(id=pk)
            self.perform_destroy(faq)
            category = faq.category
            category.FAQ_count = max(0, category.FAQ_count - 1)  
            category.save()
            
            return Response({ "success": True, "message": "FAQ deleted" })
        except ObjectDoesNotExist:
            return Response({ "success": False, "message": "FAQ does not exist" })
            



class FAQCategoryListView(generics.ListAPIView):
    serializer_class = FAQSerializer

    def get_queryset(self):
        category = self.kwargs['category']
        self.category = get_object_or_404(CategoryFAQ, category=category)  
        return FAQ.objects.filter(category=self.category)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        faq_count = queryset.count()
        
        response = super().list(request, *args, **kwargs)
        
        response_data = [{
            'category': self.category.category,  
            'faq_count': faq_count,
            'faqs': response.data  
        }]
        
        return Response(response_data, status=status.HTTP_200_OK)

       

    
class FeedbackListCreateView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    def get(self, request, pk):
        try:
            faq = FAQ.objects.get(id=pk)
            feedback = Feedback.objects.filter(faq=faq)
            serializer = self.serializer_class(feedback, many=True)
            return Response({"feedback": serializer.data })
        except FAQ.DoesNotExist:
            return Response({"message": "faq does not exist" })

    def post(self, request, pk):
        try:
            faq = FAQ.objects.get(id=pk)
            serializer = self.serializer_class( data=request.data)
            if serializer.is_valid():
                serializer.save(faq=faq)
                return Response({ "success": True, "message": "feedback added" })
            else:
                print(serializer.errors)
                return Response({ "success": False, "message": "error adding feedback","errors":serializer.errors })
        except ObjectDoesNotExist:
            return Response({ "success": False, "message": "question does not exist" })
class DestroyFeedbackView(generics.DestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer        
    def delete(self, request, *args, **kwargs):
        try:
            pk = kwargs.get("pk")
            feedback = Feedback.objects.get(id=pk)
            self.perform_destroy(feedback)
            return Response({ "success": True, "message": "Feedback deleted" })
        except ObjectDoesNotExist:
            return Response({ "success": False, "message": "Feedback does not exist" })
            
class UpdateFeedbackView(generics.UpdateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        feedback = Feedback.objects.get(id=pk)
        serializer = self.get_serializer(feedback, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({ "success": True, "message": "updated Feedback" })
        else:
            print(serializer.errors)
            return Response({ "success": False, "message": "error updating Feedback" })
        
