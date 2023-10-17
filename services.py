def add_m2m(obj, create, extracted, field):
    if not create:
        return

    if extracted:
        for relation in extracted:
            getattr(obj, field).add(relation)
