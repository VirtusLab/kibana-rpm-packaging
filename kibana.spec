Name: kibana
Version: 4.0.2
Release: 1
Summary: open source data visualization platform 
License: see /usr/share/doc/kibana/LICENSE
Distribution: Elastic
Group: Applications/Internet
Requires: nodejs

%define _unpackaged_files_terminate_build 1

%description
Kibana is an open source data visualization platform that allows you to interact with your data through stunning, powerful graphics that can be combined into custom dashboards that help you share insights from your data far and wide.

%build
ver=kibana-%{version}-linux-x64
mkdir -p %{buildroot}
cd %{buildroot}
wget https://download.elasticsearch.org/kibana/kibana/${ver}.tar.gz
tar -xf ${ver}.tar.gz
rm ${ver}.tar.gz
mkdir {etc,usr/share{,/doc}}/kibana -p
mv ${ver}/src/* usr/share/kibana/
mv ${ver}/config/kibana.yml etc/kibana/
mv ${ver}/*.txt usr/share/doc/kibana/
rm -Rf ${ver}
mkdir etc/sysconfig -p
wget https://raw.githubusercontent.com/VirtusLab/kibana-rpm-packaging/master/kibana.sysconfig -O etc/sysconfig/kibana
mkdir usr/lib/systemd/system -p
wget https://raw.githubusercontent.com/VirtusLab/kibana-rpm-packaging/master/kibana.service -O usr/lib/systemd/system/kibana.service


%files
#find etc/kibana/ usr/share/kibana/ -type d | sed 's#^#%dir /#' > filelist.inc
#find etc -type f | sed -e 's#etc/#%config(noreplace) /etc/#' >> filelist.inc
#find usr/share/doc/kibana -type f | sed -e 's#^#%doc /#' >> filelist.inc
#find usr/share/kibana -type f | sed -e 's#^#/#' >> filelist.inc 
#echo "/etc/sysconfig/kibana" >> filelist.inc
#echo "/usr/lib/systemd/system/kibana.service" >> filelist.inc
%include filelist.inc
