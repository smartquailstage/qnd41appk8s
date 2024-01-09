import datetime
from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.functional import cached_property
from django.http import Http404
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from wagtail.admin.panels import ( FieldPanel, FieldRowPanel,InlinePanel,MultiFieldPanel,PageChooserPanel)
from streams import blocks
from wagtail.models import Page,Orderable
from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField, RichTextField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.search import index
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField,FORM_FIELD_CHOICES, AbstractForm
from wagtail.contrib.forms.panels import FormSubmissionsPanel

from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from django.urls import reverse
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.images.fields import WagtailImageField
from wagtail.models import Collection
import json
from os.path import splitext
from django.core.serializers.json import DjangoJSONEncoder
from wagtail.images import get_image_model



class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('shop:product_list_by_category',
                           args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('shop:product_detail',
      
                           args=[self.id, self.slug])
    
class commingsoonform(AbstractFormField):
    page = ParentalKey('commingsoon', on_delete=models.CASCADE, related_name='form_fields')

class commingsoon(AbstractEmailForm):
    template = "webapp/home/commingsoon.html"
    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")
    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [
        FieldPanel('consulta', classname="full"),

        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="consultashome"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
#Panel capo de noticas
        FieldPanel("custom_title"),

    ]


class consultashome(AbstractFormField):
    page = ParentalKey('home', on_delete=models.CASCADE, related_name='form_fields')

class home(AbstractEmailForm):
    # Empieza Barner de Inicio
    template = "webapp/home/home.html"
    titulo = RichTextField(blank=True,verbose_name='titulo')
    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de sliders
    bio = RichTextField(blank=True,verbose_name='reseña bibliografica')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo info')
    info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info')
    banner_title5 = RichTextField(blank=True,verbose_name='Titulo de galeria-2  ')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-2 info')
    info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-2')
    banner_title6 = RichTextField(blank=True,verbose_name='Titulo de galeria-3  ')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-3 info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-3')
    banner_title7 = RichTextField(blank=True,verbose_name='Titulo de galeria-4  ')
    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulot-4 info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-4')
    banner_title8 = RichTextField(blank=True,verbose_name='Titulo de galeria-5  ')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-5 info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-5')
    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de galeria-6  ')
    TS_info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-6 info')
    info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-6')


    # Empieza Banner de callout
    banner_title10 = RichTextField(blank=True,verbose_name='we improve')
    info7 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business analytics')
    info8 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business cloud DevOps')
    info9 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business Media')
    
    # Empieza Banner de Products

  
    product_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-1')
    product_description_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-1')
    product_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-2')
    product_description_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-2')
    product_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-3')
    product_description_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-3')
    product_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-4')
    product_description_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-4')
    product_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-5')
    product_description_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-5')
    product_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-6')
    product_description_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-6')
    # Banner contador
    numero_coffe = models.IntegerField( null=True)
    numero_experiencia =  models.IntegerField( null=True)
    numero_horas = models.IntegerField( null=True)
    numero_wins = models.IntegerField(null=True)


    team_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-1')
    team_descrp_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-1')
    team_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-2')
    team_descrp_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-2')
    team_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-3')
    team_descrp_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-3')
    team_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-4')
    team_descrp_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-4')

    banner_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Call Action Title')
    slogan = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan')
    slogan_descriptcion = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan Description')
    


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [


    #Panel sliders
        FieldPanel('bio', classname="full"),
        FieldPanel('banner_title4', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('info1', classname="full"),
        FieldPanel('banner_title5', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('info2', classname="full"),
        FieldPanel('banner_title6', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('info3', classname="full"),
        FieldPanel('banner_title7', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('info4', classname="full"),
        FieldPanel('banner_title8', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('info5', classname="full"),
        FieldPanel('banner_title9', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('info6', classname="full"),
        FieldPanel('banner_title10', classname="full"),
        FieldPanel('info7', classname="full"),
        FieldPanel('info8', classname="full"),
        FieldPanel('info9', classname="full"),


        FieldPanel('product_1', classname="full"),
        FieldPanel('product_description_1', classname="full"),
        FieldPanel('product_2', classname="full"),
        FieldPanel('product_description_2', classname="full"),
        FieldPanel('product_3', classname="full"),
        FieldPanel('product_description_3', classname="full"),
        FieldPanel('product_4', classname="full"),
        FieldPanel('product_description_4', classname="full"),
        FieldPanel('product_5', classname="full"),
        FieldPanel('product_description_5', classname="full"),
        FieldPanel('product_6', classname="full"),
        FieldPanel('product_description_6', classname="full"),
        FieldPanel('numero_coffe', classname="full"),
        FieldPanel('numero_experiencia', classname="full"),
        FieldPanel('numero_horas', classname="full"),
        FieldPanel('numero_wins', classname="full"),
        FieldPanel('team_1', classname="full"),
        FieldPanel('team_descrp_1', classname="full"),
        FieldPanel('team_2', classname="full"),
        FieldPanel('team_descrp_2', classname="full"),
        FieldPanel('team_3', classname="full"),
        FieldPanel('team_descrp_3', classname="full"),
        FieldPanel('team_4', classname="full"),
        FieldPanel('team_descrp_4', classname="full"),
        FieldPanel('banner_title', classname="full"),
        FieldPanel('slogan', classname="full"),
        FieldPanel('slogan_descriptcion', classname="full"),


#panel 
        FieldPanel('consulta', classname="full"),

        InlinePanel('galleria', label="Imagen de Fondo Barner"),
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="consultashome"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
#Panel capo de noticas
        FieldPanel("custom_title"),
    ]



class GaleriaHome(Orderable):
    page = ParentalKey(home, on_delete=models.CASCADE, related_name='galleria')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo SmartQuail')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 5')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 6')


    panels = [
        FieldPanel('logo'),
        FieldPanel('profile_pic'),
        FieldPanel('image'),
        FieldPanel('image_2'),
        FieldPanel('image_3'),
        FieldPanel('image_4'),
        FieldPanel('image_5'),
        FieldPanel('image_6'),

    ]


# pagina de inicio
class consultas(AbstractFormField):
    page = ParentalKey('smartbusinessmedia', on_delete=models.CASCADE, related_name='form_fields')

class smartbusinessmedia(AbstractEmailForm):
    # Empieza Barner de Inicio
    template = "webapp/products/smartbusinessmedia/index/smartbusinesmedia.html"
    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de sliders
    bio = RichTextField(blank=True,verbose_name='rseña bibliografica')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo info')
    info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info')
    banner_title5 = RichTextField(blank=True,verbose_name='Titulo de galeria-2  ')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-2 info')
    info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-2')
    banner_title6 = RichTextField(blank=True,verbose_name='Titulo de galeria-3  ')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-3 info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-3')
    banner_title7 = RichTextField(blank=True,verbose_name='Titulo de galeria-4  ')
    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulot-4 info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-4')
    banner_title8 = RichTextField(blank=True,verbose_name='Titulo de galeria-5  ')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-5 info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-5')
    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de galeria-6  ')
    TS_info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-6 info')
    info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-6')


    # Empieza Banner de callout
    banner_title10 = RichTextField(blank=True,verbose_name='we improve')
    info7 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business analytics')
    info8 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business cloud DevOps')
    info9 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business Media')
    
    # Empieza Banner de Products

  
    product_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-1')
    product_description_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-1')
    product_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-2')
    product_description_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-2')
    product_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-3')
    product_description_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-3')
    product_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-4')
    product_description_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-4')
    product_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-5')
    product_description_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-5')
    product_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-6')
    product_description_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-6')
    # Banner contador
    numero_coffe = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    numero_experiencia = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    numero_horas = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    numero_wins = models.DecimalField(max_digits=10, decimal_places=2,null=True)


    team_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-1')
    team_descrp_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-1')
    team_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-2')
    team_descrp_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-2')
    team_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-3')
    team_descrp_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-3')
    team_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-4')
    team_descrp_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-4')

    banner_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Call Action Title')
    slogan = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan')
    slogan_descriptcion = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan Description')
    


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [


    #Panel sliders
        FieldPanel('bio', classname="full"),
        FieldPanel('banner_title4', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('info1', classname="full"),
        FieldPanel('banner_title5', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('info2', classname="full"),
        FieldPanel('banner_title6', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('info3', classname="full"),
        FieldPanel('banner_title7', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('info4', classname="full"),
        FieldPanel('banner_title8', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('info5', classname="full"),
        FieldPanel('banner_title9', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('info6', classname="full"),
        FieldPanel('banner_title10', classname="full"),
        FieldPanel('info7', classname="full"),
        FieldPanel('info8', classname="full"),
        FieldPanel('info9', classname="full"),


        FieldPanel('product_1', classname="full"),
        FieldPanel('product_description_1', classname="full"),
        FieldPanel('product_2', classname="full"),
        FieldPanel('product_description_2', classname="full"),
        FieldPanel('product_3', classname="full"),
        FieldPanel('product_description_3', classname="full"),
        FieldPanel('product_4', classname="full"),
        FieldPanel('product_description_4', classname="full"),
        FieldPanel('product_5', classname="full"),
        FieldPanel('product_description_5', classname="full"),
        FieldPanel('product_6', classname="full"),
        FieldPanel('product_description_6', classname="full"),
        FieldPanel('numero_coffe', classname="full"),
        FieldPanel('numero_experiencia', classname="full"),
        FieldPanel('numero_horas', classname="full"),
        FieldPanel('numero_wins', classname="full"),
        FieldPanel('team_1', classname="full"),
        FieldPanel('team_descrp_1', classname="full"),
        FieldPanel('team_2', classname="full"),
        FieldPanel('team_descrp_2', classname="full"),
        FieldPanel('team_3', classname="full"),
        FieldPanel('team_descrp_3', classname="full"),
        FieldPanel('team_4', classname="full"),
        FieldPanel('team_descrp_4', classname="full"),
        FieldPanel('banner_title', classname="full"),
        FieldPanel('slogan', classname="full"),
        FieldPanel('slogan_descriptcion', classname="full"),


#panel 
        FieldPanel('consulta', classname="full"),

        InlinePanel('galleria_2', label="Imagen de Fondo Barner"),
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="consultas"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
#Panel capo de noticas
        FieldPanel("custom_title"),
    ]


class GaleriadeImagenesSBM(Orderable):
    page = ParentalKey(smartbusinessmedia, on_delete=models.CASCADE, related_name='galleria_2')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo SmartQuail')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 5')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 6')
    image_7 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 1')
    image_8 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 2')
    image_9 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 3')
    image_10 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 4')
    image_11 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 5')
    image_12 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 6')
    image_13 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 1')
    image_14 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 2')
    image_15 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 3')
    image_16 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 4')

    panels = [
        FieldPanel('logo'),
        FieldPanel('profile_pic'),
        FieldPanel('image'),
        FieldPanel('image_2'),
        FieldPanel('image_3'),
        FieldPanel('image_4'),
        FieldPanel('image_5'),
        FieldPanel('image_6'),
        FieldPanel('image_7'),
        FieldPanel('image_8'),
        FieldPanel('image_9'),
        FieldPanel('image_10'),
        FieldPanel('image_11'),
        FieldPanel('image_12'),
        FieldPanel('image_13'),
        FieldPanel('image_14'),
        FieldPanel('image_15'),
        FieldPanel('image_16'),
    ]

class consultascreateitbusiness(AbstractFormField):
    page = ParentalKey('createitbusiness', on_delete=models.CASCADE, related_name='form_fields')
class createitbusiness(AbstractEmailForm):

    template = "webapp/createitbusiness/createitbusiness.html"
    bio = RichTextField(blank=True,verbose_name='rseña bibliografica')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo info')
    info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info')
    banner_title5 = RichTextField(blank=True,verbose_name='Titulo de galeria-2  ')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-2 info')
    info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-2')
    banner_title6 = RichTextField(blank=True,verbose_name='Titulo de galeria-3  ')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-3 info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-3')
    banner_title7 = RichTextField(blank=True,verbose_name='Titulo de galeria-4  ')
    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulot-4 info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-4')
    banner_title8 = RichTextField(blank=True,verbose_name='Titulo de galeria-5  ')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-5 info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-5')
    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de galeria-6  ')
    TS_info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-6 info')
    info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-6')


    # Empieza Banner de callout
    banner_title10 = RichTextField(blank=True,verbose_name='we improve')
    info7 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business analytics')
    info8 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business cloud DevOps')
    info9 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business Media')
    
    # Empieza Banner de Products

  
    product_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-1')
    product_description_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-1')
    product_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-2')
    product_description_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-2')
    product_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-3')
    product_description_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-3')
    product_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-4')
    product_description_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-4')
    product_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-5')
    product_description_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-5')
    product_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-6')
    product_description_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-6')
    # Banner contador



    team_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-1')
    team_descrp_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-1')
    team_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-2')
    team_descrp_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-2')
    team_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-3')
    team_descrp_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-3')
    team_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-4')
    team_descrp_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-4')

    banner_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Call Action Title')
    slogan = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan')
    slogan_descriptcion = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan Description')
    


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [
        FieldPanel('bio', classname="full"),
        FieldPanel('banner_title4', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('info1', classname="full"),

        FieldPanel('product_1', classname="full"),
        FieldPanel('product_description_1', classname="full"),
        FieldPanel('product_2', classname="full"),
        FieldPanel('product_description_2', classname="full"),
        FieldPanel('product_3', classname="full"),
        FieldPanel('product_description_3', classname="full"),
        FieldPanel('product_4', classname="full"),
        FieldPanel('product_description_4', classname="full"),

        FieldPanel('slogan', classname="full"),
        FieldPanel('slogan_descriptcion', classname="full"),
        FieldPanel('consulta', classname="full"),
        InlinePanel('galleria_contacus', label="Imagen de Fondo Barner"),
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="consultashome"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
#Panel capo de noticas
        FieldPanel("custom_title"),
    ]
class Galeriacreateitbusiness(Orderable):
    page = ParentalKey(createitbusiness, on_delete=models.CASCADE, related_name='galleria_contacus')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo SmartQuail')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_17 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_18 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_19 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_20 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_21 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_22 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_23 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_24 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_25 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_26 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')

    panels = [
        FieldPanel('logo'),
        FieldPanel('profile_pic'),
        FieldPanel('image'),
        FieldPanel('image_17'),
        FieldPanel('image_18'),
        FieldPanel('image_19'),
        FieldPanel('image_20'),
        FieldPanel('image_21'),
        FieldPanel('image_22'),
        FieldPanel('image_23'),
        FieldPanel('image_24'),
        FieldPanel('image_25'),
        FieldPanel('image_26'),
    ]

class consultascreateprojects(AbstractFormField):
    page = ParentalKey('createprojects', on_delete=models.CASCADE, related_name='form_fields')
class createprojects(AbstractEmailForm):
    # Empieza Barner de Inicio
    template = "webapp/createitbusiness/createprojects.html"
    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de sliders
    bio = RichTextField(blank=True,verbose_name='rseña bibliografica')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo info')
    info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info')
    banner_title5 = RichTextField(blank=True,verbose_name='Titulo de galeria-2  ')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-2 info')
    info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-2')
    banner_title6 = RichTextField(blank=True,verbose_name='Titulo de galeria-3  ')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-3 info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-3')
    banner_title7 = RichTextField(blank=True,verbose_name='Titulo de galeria-4  ')
    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulot-4 info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-4')
    banner_title8 = RichTextField(blank=True,verbose_name='Titulo de galeria-5  ')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-5 info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-5')
    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de galeria-6  ')
    TS_info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-6 info')
    info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-6')


    # Empieza Banner de callout
    banner_title10 = RichTextField(blank=True,verbose_name='we improve')
    info7 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business analytics')
    info8 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business cloud DevOps')
    info9 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business Media')
    
    # Empieza Banner de Products

  
    product_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-1')
    product_description_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-1')
    product_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-2')
    product_description_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-2')
    product_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-3')
    product_description_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-3')
    product_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-4')
    product_description_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-4')
    product_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-5')
    product_description_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-5')
    product_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-6')
    product_description_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-6')
    # Banner contador
    numero_coffe = models.IntegerField( null=True)
    numero_experiencia =  models.IntegerField( null=True)
    numero_horas = models.IntegerField( null=True)
    numero_wins = models.IntegerField(null=True)


    team_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-1')
    team_descrp_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-1')
    team_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-2')
    team_descrp_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-2')
    team_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-3')
    team_descrp_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-3')
    team_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-4')
    team_descrp_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-4')

    banner_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Call Action Title')
    slogan = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan')
    slogan_descriptcion = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan Description')
    


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [


    #Panel sliders
        FieldPanel('bio', classname="full"),
        FieldPanel('banner_title4', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('info1', classname="full"),
        FieldPanel('banner_title5', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('info2', classname="full"),
        FieldPanel('banner_title6', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('info3', classname="full"),
        FieldPanel('banner_title7', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('info4', classname="full"),
        FieldPanel('banner_title8', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('info5', classname="full"),
        FieldPanel('banner_title9', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('info6', classname="full"),
        FieldPanel('banner_title10', classname="full"),
        FieldPanel('info7', classname="full"),
        FieldPanel('info8', classname="full"),
        FieldPanel('info9', classname="full"),


        FieldPanel('product_1', classname="full"),
        FieldPanel('product_description_1', classname="full"),
        FieldPanel('product_2', classname="full"),
        FieldPanel('product_description_2', classname="full"),
        FieldPanel('product_3', classname="full"),
        FieldPanel('product_description_3', classname="full"),
        FieldPanel('product_4', classname="full"),
        FieldPanel('product_description_4', classname="full"),
        FieldPanel('product_5', classname="full"),
        FieldPanel('product_description_5', classname="full"),
        FieldPanel('product_6', classname="full"),
        FieldPanel('product_description_6', classname="full"),
        FieldPanel('numero_coffe', classname="full"),
        FieldPanel('numero_experiencia', classname="full"),
        FieldPanel('numero_horas', classname="full"),
        FieldPanel('numero_wins', classname="full"),
        FieldPanel('team_1', classname="full"),
        FieldPanel('team_descrp_1', classname="full"),
        FieldPanel('team_2', classname="full"),
        FieldPanel('team_descrp_2', classname="full"),
        FieldPanel('team_3', classname="full"),
        FieldPanel('team_descrp_3', classname="full"),
        FieldPanel('team_4', classname="full"),
        FieldPanel('team_descrp_4', classname="full"),
        FieldPanel('banner_title', classname="full"),
        FieldPanel('slogan', classname="full"),
        FieldPanel('slogan_descriptcion', classname="full"),
#panel 
        FieldPanel('consulta', classname="full"),
        InlinePanel('project_descriptions', label="opciones"),

        InlinePanel('galleria_createproject', label="Imagen de Fondo Barner"),
       
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="consultashome"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
#Panel capo de noticas
        FieldPanel("custom_title"),
    ]

class projectoptions(Orderable):
    page = ParentalKey(createprojects, on_delete=models.CASCADE, related_name='project_descriptions')
    project_description = RichTextField(blank=True,verbose_name='Descripcion de proyecto ')
    project_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='titulo de Projecto')

    panels = [
        FieldPanel('project_title'),
        FieldPanel('project_description'),
    ]
    

class Galeriacreateprojectitbusiness(Orderable):
    page = ParentalKey(createprojects, on_delete=models.CASCADE, related_name='galleria_createproject')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo SmartQuail')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 5')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 6')
    image_7 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 1')
    image_8 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 2')
    image_9 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 3')
    image_10 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 4')
    image_11 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 5')
    image_12 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 6')
    image_13 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 1')
    image_14 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 2')
    image_15 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 3')
    image_16 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 4')
    image_17 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_18 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_19 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_20 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_21 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_22 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_23 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_24 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_25 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_26 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')

    panels = [
        FieldPanel('logo'),
        FieldPanel('profile_pic'),
        FieldPanel('image'),
        FieldPanel('image_2'),
        FieldPanel('image_3'),
        FieldPanel('image_4'),
        FieldPanel('image_5'),
        FieldPanel('image_6'),
        FieldPanel('image_7'),
        FieldPanel('image_8'),
        FieldPanel('image_9'),
        FieldPanel('image_10'),
        FieldPanel('image_11'),
        FieldPanel('image_12'),
        FieldPanel('image_13'),
        FieldPanel('image_14'),
        FieldPanel('image_15'),
        FieldPanel('image_16'),
        FieldPanel('image_17'),
        FieldPanel('image_18'),
        FieldPanel('image_19'),
        FieldPanel('image_20'),
        FieldPanel('image_21'),
        FieldPanel('image_22'),
        FieldPanel('image_23'),
        FieldPanel('image_24'),
        FieldPanel('image_25'),
        FieldPanel('image_26'),
    ]


class consultascontact(AbstractFormField):
    page = ParentalKey('contactus', on_delete=models.CASCADE, related_name='form_fields')
class contactus(AbstractEmailForm):

    template = "webapp/home/contactus.html"
    bio = RichTextField(blank=True,verbose_name='rseña bibliografica')
    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")
    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [
        FieldPanel('bio', classname="full"),
        FieldPanel('consulta', classname="full"),
        InlinePanel('galleria_contactus', label="Imagen de Fondo Barner"),
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="consultas_contactus"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
#Panel capo de noticas
        FieldPanel("custom_title"),
    ]

class GaleriaContactus(Orderable):
    page = ParentalKey(contactus, on_delete=models.CASCADE, related_name='galleria_contactus')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')

    panels = [
        FieldPanel('image'),
    ]



class ArticleListingPage(Page):
    template = "webapp/article_listing_page.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = ArticleDetailPage.objects.live().public()
        return context
    
class comments_ArticleDetailPage(AbstractFormField):
    page = ParentalKey('ArticleDetailPage', on_delete=models.CASCADE, related_name='form_fields')

class ArticleDetailPage(AbstractEmailForm):

    category = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text='Article category',
    )

    author = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text='Author Article',
    )

    bio2 = models.CharField(
        max_length=500,
        blank=False,
        null=True,
        help_text='Author bio',
    )

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text='Overwrites article title',
    )
    custom_subtitle = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text='Overwrites article subtitle',
    )
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    date = models.DateTimeField(auto_now=True)
    abstract = RichTextField(blank=True,verbose_name='Abstract')
    comments = RichTextField(blank=True,verbose_name='Mensaje para que nos dejen un comentario')
    thank_you_text = RichTextField(blank=True)

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichtextBlock()),
            ("simple_richtext", blocks.SimpleRichtextBlock()),
            ('image', ImageChooserBlock()),
            ("cards", blocks.CardBlock()),
        ],use_json_field=True,
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("category"),
        FieldPanel("author"),
        FieldPanel("bio2"),
        FieldPanel("custom_title"),
        FieldPanel("custom_subtitle"),
        FieldPanel("blog_image"),
        InlinePanel('galleria_article_Page', label="Imagenes del articulo"),
        FieldPanel("abstract"),
        FieldPanel("content"),
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="comments"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    def get_form_fields(self):
        return self.form_fields.all()

    def get_data_fields(self):
        data_fields = [
            ('name', 'Name'),
        ]
        data_fields += super().get_data_fields()

        return data_fields

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # If you need to show results only on landing page,
        # you may need check request.method

        results = dict()
        # Get information about form fields
        data_fields = [
            (field.clean_name, field.label)
            for field in self.get_form_fields()
        ]

        # Get all submissions for current page
        submissions = self.get_submission_class().objects.filter(page=self)
        for submission in submissions:
            data = submission.get_data()

            # Count results for each question
            for name, label in data_fields:
                answer = data.get(name)
                if answer is None:
                    # Something wrong with data.
                    # Probably you have changed questions
                    # and now we are receiving answers for old questions.
                    # Just skip them.
                    continue

                if type(answer) is list:
                    # Answer is a list if the field type is 'Checkboxes'
                    answer = u', '.join(answer)

                question_stats = results.get(label, {})
                question_stats[answer] = question_stats.get(answer, 0) + 1
                results[label] = question_stats

        context.update({
            'results': results,
        })
        return context
    
class galleria_article_Page(Orderable):
    page = ParentalKey(ArticleDetailPage, on_delete=models.CASCADE, related_name='galleria_article_Page')    
    image_1 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Banner')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Author picture')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='imagen 2')
    
    
    panels = [
        FieldPanel('image_1'),
        FieldPanel('image_2'),
        FieldPanel('image_3')
    ]