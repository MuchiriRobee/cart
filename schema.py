import graphene
from graphene_django import DjangoObjectType
from .models import Product, CartItem

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem

class Query(graphene.ObjectType):
    products = graphene.List(ProductType)
    cart_items = graphene.List(CartItemType)

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_cart_items(self, info):
        return CartItem.objects.all()

class AddToCart(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)

    cart_item = graphene.Field(CartItemType)

    def mutate(self, info, product_id):
        product = Product.objects.get(pk=product_id)
        cart_item = CartItem(product=product)
        cart_item.save()
        return AddToCart(cart_item=cart_item)

class Mutation(graphene.ObjectType):
    add_to_cart = AddToCart.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
