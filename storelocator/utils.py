from .models import Shop


def get_near_shops(storelocator, lat, lon, limit, radius, distance, iso=None):

    shops = storelocator.shops.filter(
        latitude__gte=(lat - 0.009 * radius),
        latitude__lte=(lat + 0.009 * radius),
        longitude__gte=(lon - 0.009 * radius),
        longitude__lte=(lon + 0.009 * radius),
    )

    if iso:
        shops = shops.filter(iso=iso)

    if distance:
        for shop in list(shops):
            shop.distance = shop.distance_to(lat, lon).km
        shops = [shop for shop in shops if shop.distance <= radius]
        shops = sorted(shops, key=lambda s: s.distance)
    return shops[:limit]

