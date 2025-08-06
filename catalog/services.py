def get_all_products():
    cache_key = 'all_products'
    products = cache.get(cache_key)

    if not products:
        products = Product.objects.filter(
            publish_status='published'
        ).select_related('category').prefetch_related('images')
        cache.set(cache_key, products, 60 * 60)  # Кеш на 1 час

    return products
