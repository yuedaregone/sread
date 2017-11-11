using System;
using System.Collections;
using System.Collections.Generic;
{# datainfo, dataread, filename, datamemberlist(name, type, parse_fun) #}
public class {{ datainfo }}
{ {% for member in datamemberlist %}
    public {{ member[1] }} {{ member[0] }};{% endfor %}
}

public class {{ dataread }} : BinaryTableReader<{{ dataread }}, {{ datainfo }}>
{
    public {{ datainfo }} DeserializeInfo()
    {
        {{ datainfo }} data = new {{ datainfo }}();{% for member in datamemberlist %}
        data.{{ member[0] }} = m_byteBuffer.{{ member[2] }}();{% endfor %}
        return data;
    }

    protected override void Deserialize()
    {
        m_byteBuffer.ReadStringByLen(3);
        int contentOffset = m_byteBuffer.ReadInt();
        m_byteBuffer.SetReadOffset(contentOffset);
        ushort dataSize = m_byteBuffer.ReadUnsignShort();
        for (ushort i = 0; i < dataSize; ++i)
        {
            {{ datainfo }} info = DeserializeInfo();
            m_datas.Add(info.ID, info);
        }
    }

    public override string GetPath()
    {
        return "static_data/{{ filename }}";
    }
}
