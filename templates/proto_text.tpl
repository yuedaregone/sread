{# datalist[list[(type_name, value)]] #}
{% for data in datalist %}
dataList { {% for item in data %}
    {{ item[0] }}: {{ item[1] }}{% endfor %}
}
{% endfor %}


