{% if property.type %}
        {{ property.name }} = d.get("{{ property.name }}", [])
{% else %}
        {{ property.name }} = []
        for {{ property.name }}_item in d.get("{{ property.name }}", []):
            {{ property.name }}.append({{ property.reference.class_name }}.from_dict({{ property.name }}_item))
{% endif %}
