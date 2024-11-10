from rest_framework import serializers
from .models import CategoryFAQ, FAQ, Feedback,TagFAQ

class CategoryFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryFAQ
        fields = '__all__'
    
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
    Tags = serializers.SerializerMethodField()
    def get_Tags(self, obj):
        return list(obj.Tags.values_list('Tags', flat=True))
    
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields ='__all__'
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagFAQ
        fields = '__all__'