from bs4 import BeautifulSoup, NavigableString
import HTMLParser
#import xml.etree.ElementTree as ET
#tree = ET.parse('D:/LimPosts.xml')
#root = tree.getroot()
#for country in root.findall('row'):
#    type = country.get('PostTypeId')
#    if type != None and '1' in type:
#        tag = country.get('Tags')
#        if tag != None and 'python' in tag:
#            print country.get('Body')


#def remove_tags(text):d
#    return ''.join(ET.fromstring(text).itertext())


text = "&lt;p&gt;How do you expose &pound; &amp; a &lt;strong&gt;LINQ&lt;/strong&gt; query as an &lt;strong&gt;ASMX&lt;/strong&gt; web service? Usually, from the business tier, I can return a typed &lt;code&gt;DataSet&lt;/code&gt; or &lt;code&gt;DataTable&lt;/code&gt; which can be serialized for transport over &lt;strong&gt;ASMX&lt;/strong&gt;.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;How can I do the same for a &lt;strong&gt;LINQ&lt;/strong&gt; query? Is there a way to populate a typed &lt;code&gt;DataSet&lt;/code&gt; or &lt;code&gt;DataTable&lt;/code&gt; via a &lt;strong&gt;LINQ&lt;/strong&gt; query?: &lt;/p&gt;&#xA;&#xA;&lt;pre&gt;&lt;code&gt;public static MyDataTable CallMySproc()    &#xA;{    &#xA;    string conn = ...;&#xA;&#xA;    MyDatabaseDataContext db = new MyDatabaseDataContext(conn);    &#xA;    MyDataTable dt = new MyDataTable();&#xA;&#xA;    // execute a sproc via LINQ&#xA;    var query = from dr in db.MySproc().AsEnumerable&#xA;    select dr;&#xA;&#xA;    // copy LINQ query resultset into a DataTable -this does not work !    &#xA;    dt = query.CopyToDataTable();&#xA;&#xA;    return dt;&#xA;}&#xA;&lt;/code&gt;&lt;/pre&gt;&#xA;&#xA;&lt;p&gt;How can I get the resultset of a &lt;strong&gt;LINQ&lt;/strong&gt; query into a &lt;code&gt;DataSet&lt;/code&gt; or &lt;code&gt;DataTable&lt;/code&gt;? Alternatively, is the &lt;strong&gt;LINQ&lt;/strong&gt; query serializeable so that I can expose it as an &lt;strong&gt;ASMX&lt;/strong&gt; web service?&lt;/p&gt;&#xA;"

bogusCode = "<code><code>somecode</code></code>fdsds<code>otherocde</code><p>text<code>othercode</code>endtext</p>text"





res = texth(unescaped)

print res