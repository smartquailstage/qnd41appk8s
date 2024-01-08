from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)
    logo = models.ImageField(upload_to='logo/%Y/%m/%d',
                              blank=True,null=True)
    info= models.TextField(blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('sbmshop:product_list_by_category',
                           args=[self.slug])


class SBMProduct(models.Model):
    ICON_CHOICE = (
    ("icofont-legal", "icofont-legal"),
    ("icofont-law-book", "icofont-law-book"),
    ("icofont-ebook", "icofont-ebook"),
    ("icofont-ui-office", "icofont-ui-office"),
    ("icofont-list", "icofont-list"),
    ("icofont-key", "icofont-key"),
    )
  

    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    
    item1 = models.CharField(max_length=200, db_index=True,null=True,blank=True)
    item2 = models.CharField(max_length=200, db_index=True,null=True,blank=True)
    item3 = models.CharField(max_length=200, db_index=True,null=True,blank=True)
    item4 = models.CharField(max_length=200, db_index=True,null=True,blank=True)

    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    conditions = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    icon= models.CharField(choices=ICON_CHOICE, max_length=200, db_index=True,null=True, blank= True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('sbmshop:product_detail',
                           args=[self.id, self.slug])
