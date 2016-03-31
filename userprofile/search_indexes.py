from haystack import indexes
from userprofile.models import CompanyProfile_seekFund, CompanyProfile_sale

class SeekfundIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #goal = indexes.CharField(model_attr='goal')
    # category = indexes.CharField(model_attr='category')
    #company = indexes.CharField(model_attr='company')

    def get_model(self):
        return CompanyProfile_seekFund

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class SaleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    goal = indexes.CharField(model_attr='goal')
    # category = indexes.CharField(model_attr='category')
    #company = indexes.CharField(model_attr='company')

    def get_model(self):
        return CompanyProfile_sale

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()