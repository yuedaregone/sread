syntax = "proto3";
package data;
{# datainfo, datalist, datamemberlist(name, type, parse_fun) #}
message {{ datainfo }}
{ {% for member in datamemberlist %}
    {{ member[0] }} {{ member[1] }} = {{ loop.index }};{% endfor %}
}

message {{ datalist }}
{
    repeated {{ datainfo }} dataList = 1;
}
