from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse



class ProductManager(models.Manager):
    def active_products(self):
        return self.prefetch_related("comments", "product_images").select_related("category").filter(is_active=True)


class Product(models.Model):
    CHOICES_STATUS = [
        ("none", _("none")),
        ("size", _("size")),
        ("color", _("color")),
        ("both", _("both")),
    ]
    
    name = models.CharField(_("name"), max_length=255, unique=True)

    slug = models.SlugField(_("slug"), max_length=255, unique=True)
    
    content = RichTextUploadingField(_("content"))
    
    image = models.ImageField(_("image"), upload_to="images/")
    
    price = models.PositiveIntegerField(_("price"))
    
    discount = models.PositiveIntegerField(_("discount"), blank=True, null=True)
    
    total_price = models.PositiveIntegerField(_("total_price"))
    
    inventory = models.IntegerField(_("inventory"))
    
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
    
    @property
    def total_price(self):
        """
            We use this method to calculate the total price if is there any discount for product.
            and we use this decorator to show this method as attribute for product and django will fill is in database automatically.
        """
        if not self.discount :
            return self.price
        else:
            discount_price = (self.discount * self.price) / 100
            return int(self.price - discount_price)
        return self.total_price 



class ProductImages(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE, related_name="product_images")

    name = models.CharField(_("name"), max_length=200, blank=True, unique=True)

    image = models.ImageField(_("image"), upload_to="images/")

    def __str__(self):
        return self.name



class Color(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)

    def __str__(self):
        return self.name


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

