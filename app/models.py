import stripe
from django.conf import settings
from django.db import models
from django.forms import ValidationError


class Discount(models.Model):
    name = models.CharField(max_length=100)
    percent_off = models.FloatField()
    stripe_coupon_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, currency="usd", **kwargs):
        if not self.stripe_coupon_id:
            stripe.api_key = settings.STRIPE_KEYS[currency]["secret"]
            coupon = stripe.Coupon.create(
                percent_off=self.percent_off,
                duration="once",
                name=self.name
            )
            self.stripe_coupon_id = coupon.id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tax(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.FloatField()
    stripe_tax_rate_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, currency="usd", **kwargs):
        import stripe
        from django.conf import settings

        if not self.stripe_tax_rate_id:
            stripe.api_key = settings.STRIPE_KEYS[currency]["secret"]
            tax_rate = stripe.TaxRate.create(
                display_name=self.name,
                percentage=self.percentage,
                inclusive=False
            )
            self.stripe_tax_rate_id = tax_rate.id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Item(models.Model):
    CURRENCY_CHOICES = (
        ("usd", "USD"),
        ("eur", "EUR"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField(help_text="Price in cents")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="usd")

    def __str__(self):
        return f"{self.name} ({self.currency.upper()})"

class Order(models.Model):
    CURRENCY_CHOICES = Item.CURRENCY_CHOICES

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        null=True,
        blank=True,
        help_text="Фиксируется при добавлении первого Item"
    )
    name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    discount = models.ForeignKey(
        Discount,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    tax = models.ForeignKey(
        Tax,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def total_amount(self):
        return sum(
            oi.item.price * oi.quantity
            for oi in self.items.all()
        )

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.order.currency is None:
            self.order.currency = self.item.currency
            self.order.save(update_fields=["currency"])

        elif self.order.currency != self.item.currency:
            raise ValidationError(
                f"Нельзя добавить товар с валютой {self.item.currency} "
                f"в заказ с валютой {self.order.currency}"
            )

        self.price_at_purchase = self.item.price

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.item.name} × {self.quantity} ({self.price_at_purchase / 100:.2f} {self.order.currency})"
