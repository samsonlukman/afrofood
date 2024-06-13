def annotate_with_model_name(queryset, model_name):
        for item in queryset:
            item.model_name = model_name
        return queryset