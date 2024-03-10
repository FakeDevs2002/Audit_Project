from django.db import models
from django.utils.translation import gettext_lazy as _
# from ckeditor_uploader.fields import RichTextUploadingField
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse



class ProductManager(models.Manager):
    def active_products(self):
        return self.prefetch_related("product_images").filter(is_active=True).order_by('id')


class Product(models.Model):
    CHOICES_STATUS = [
        ("none", _("none")),
        ("size", _("size")),
        ("color", _("color")),
        ("both", _("both")),
    ]
    
    name = models.CharField(_("name"), max_length=255, unique=True)

    slug = models.SlugField(_("slug"), max_length=255, unique=True)
    
    content = CKEditor5Field(_("content"), config_name='extends')
    
    image = models.ImageField(_("image"), upload_to="images/")
    
    colors = models.ManyToManyField('Color', related_name='products', verbose_name=_('colors'), blank=True, null=True)
    
    sizes = models.ManyToManyField('Size', related_name='products', verbose_name=_('sizes'), blank=True, null=True)
    
    datetime_created = models.DateTimeField(_("datetime_created"), auto_now_add=True)
    
    datetime_updated = models.DateTimeField(_("datetime_updated"), auto_now=True)
    
    status = models.CharField(_("status"), max_length=10, choices=CHOICES_STATUS)
    
    is_active = models.BooleanField(_("is_active"), default=True)

    objects = ProductManager()


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def get_absolute_url(self):
        return reverse("product:product_detail", kwargs={"product_id": self.id})
    
    def colors_to_str(self):
        return " - ".join([color.name for color in self.colors.all()])
    colors_to_str.short_description = _('colors')
    
    def sizes_to_str(self):
        return " - ".join([size.name for size in self.sizes.all()])
    sizes_to_str.short_description = _('sizes')




class ProductImages(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE, related_name="product_images")

    number = models.PositiveIntegerField(_("number"),)

    image = models.ImageField(_("image"), upload_to="images/")

    class Meta:
        db_table = ''
        managed = True
        verbose_name = _('productimage')
        verbose_name_plural = _('productimages')


class Color(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = _('color')
        verbose_name_plural = _('colors')


class Size(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = _('size')
        verbose_name_plural = _('sizes')


class Variant(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("product"), related_name="product_variants", on_delete=models.CASCADE)

    color = models.ForeignKey(Color, verbose_name=_("color"), related_name="color_variants", on_delete=models.CASCADE, blank=True, null=True)

    size = models.ForeignKey(Size, verbose_name=_("size"), related_name="size_variants", on_delete=models.CASCADE, blank=True, null=True)

    price = models.PositiveIntegerField(_("price"))

    discount = models.PositiveIntegerField(_("discount"), blank=True, null=True)

    total_price = models.PositiveIntegerField(_("total_price"))

    inventory = models.PositiveIntegerField(_("inventory"), default=0)


    def __str__(self):
        return self.product.name

    def __unicode__(self):
        return 'product id: {}'.format(self.product.id)
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = _('variant')
        verbose_name_plural = _('variants')

    # def get_absolute_url(self):
    #     return reverse("product:product_detail", kwargs={"variant_id": self.id})
    
    @property
    def total_price(self):
        """
            We use this method to calculate the total price if is there any discount for variant.
            and we use this decorator to show this method as attribute for variant and django will fill is in database automatically.
        """
        if not self.discount :
            return self.price
        else:
            discount_price = (self.discount * self.price) / 100
            return int(self.price - discount_price)
        return self.total_price 

